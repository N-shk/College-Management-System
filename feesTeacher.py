from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from db import get_connection

class FeeManagementTeacher:
    def __init__(self, root, class_name):
        self.root = root
        self.root.title("Fee Management - Teacher View")
        self.class_name = class_name
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="#f0f2f5")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure custom styles
        self.style.configure("Modern.TFrame", background="#ffffff", relief=RAISED, borderwidth=2)
        self.style.configure("Treeview.Heading", font=("Arial", 16, "bold"), foreground="white", background="#033054")
        self.style.configure("Treeview", font=("Arial", 15), rowheight=40)
        self.style.map("Treeview", background=[("selected", "#0078D4")])
        
        # Add protocol for window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Title Frame
        title_frame = Frame(self.root, bg="#033054")
        title_frame.place(x=0, y=0, relwidth=1, height=70)
        
        # Title
        title = Label(title_frame, text=f"Fee Analysis Dashboard - {class_name}", 
                     font=("Arial", 20, "bold"), bg="#033054", fg="white")
        title.pack(pady=15)
        
        # Main Content Frame
        main_frame = Frame(self.root, bg="#f0f2f5")
        main_frame.place(x=20, y=80, width=screen_width-40, height=screen_height-160)
        
        chart_width = int((screen_width-40) * 0.30)
        details_width = int((screen_width-40) * 0.65)
        # Frame for Chart
        self.chart_frame = ttk.Frame(main_frame, style="Modern.TFrame",width=chart_width)
        self.chart_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        
        # Frame for Student Details
        self.details_frame = ttk.Frame(main_frame, style="Modern.TFrame",width=details_width)
        self.details_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10, ipadx=20)
        
        # Initialize Treeview
        self.tree = ttk.Treeview(self.details_frame)
        
        self.tree.column("#0", width=0, stretch=NO) 
        # Add horizontal scrollbar
        self.hscroll = ttk.Scrollbar(self.details_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hscroll.set)
        self.scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.update_visualization()
        
    def on_closing(self):
        """Handle window closing properly"""
        plt.close('all')  # Close all matplotlib figures
        self.root.quit()
        self.root.destroy()

    def show_student_details(self, status):
        # Clear previous details
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get class_id
        cursor.execute("SELECT class_id FROM Classes WHERE class_name = ?", (self.class_name,))
        class_id = cursor.fetchone()[0]
        
        if status == 'paid':
            cursor.execute("""
                SELECT roll, student_name, 
                (SELECT class_name FROM classes WHERE class_id=?), 
                contact
                FROM Students 
                WHERE student_class=? AND fee_status='Paid'
            """, (class_id, class_id))
            
            columns = ('Roll', 'Name', 'Class', 'Contact')
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=210, anchor=CENTER)
            
            for student in cursor.fetchall():
                self.tree.insert("", END, values=student)
                
        else:  # pending
            cursor.execute("""
                SELECT DISTINCT s.roll, s.student_name,
                       COALESCE((SELECT SUM(f2.amount) 
                        FROM Fees f2 
                        WHERE f2.roll = s.roll 
                        AND f2.class_id = ?), 0) as pending_amount,
                       s.contact
                FROM Students s
                WHERE student_class=?
                AND fee_status='Pending'
            """, (class_id, class_id))
            
            columns = ('Roll', 'Name', 'Pending Fees', 'Contact')
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=210, anchor=CENTER)
            
            for student in cursor.fetchall():
                formatted_student = (*student[:2], f"₹{student[2]:,}", student[3])
                self.tree.insert("", END, values=formatted_student)
        
        # Pack treeview and scrollbar
        self.hscroll.pack(side=BOTTOM, fill=X)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True)
        
        # Add alternating row colors
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='white')
        for i, child in enumerate(self.tree.get_children()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.item(child, tags=(tag,))
        
        conn.close()

    def on_bar_click(self, event):
        if event.inaxes == self.ax:
            if event.xdata is not None:
                if abs(event.xdata - 0) < 0.5:  # Clicked on 'Paid' bar
                    self.show_student_details('paid')
                elif abs(event.xdata - 1) < 0.5:  # Clicked on 'Pending' bar
                    self.show_student_details('pending')
                    
    def on_hover(self, event):
        if event.inaxes == self.ax:
            for bar in self.bars:
                if bar.contains(event)[0]:
                    self.root.config(cursor="hand2")
                    return
        self.root.config(cursor="") 

    def update_visualization(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT class_id FROM Classes WHERE class_name = ?", (self.class_name,))
        class_id = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT fee_status, COUNT(*) as count
            FROM Students s
            JOIN Classes c ON s.student_class = c.class_id
            WHERE c.class_name = ?
            GROUP BY fee_status
        """, (self.class_name,))
        
        data = dict(cursor.fetchall())
        paid_count = data.get('Paid', 0)
        pending_count = data.get('Pending', 0)
        
        conn.close()
            
        # Create visualization
        fig = plt.figure(figsize=(8, 6), facecolor='#f8f9fa')
        self.ax = plt.gca()
        self.ax.set_facecolor('#f8f9fa')
        
        # Custom bar styling
        self.bars = plt.bar(['Paid', 'Pending'], [paid_count, pending_count],
                      color=['#2ecc71', '#e74c3c'], width=0.6,
                      edgecolor='black', linewidth=1.5)
        
        # Add value labels with shadow effect
        for bar in self.bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)} Students\n',
                    ha='center', va='bottom', fontsize=13,
                    bbox=dict(facecolor='white', edgecolor='#333', boxstyle='round,pad=0.2'))
        
        # Styling
        plt.title('Students Fee Status Distribution\n', fontsize=16, fontweight='bold', color='#333')
        plt.ylabel('Number of Students', fontsize=13)
        plt.xticks(fontsize=12, color='#333')
        plt.yticks(fontsize=12, color='#333')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#ccc')
        self.ax.spines['bottom'].set_color('#ccc')
        
        # Add grid
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Connect events
        fig.canvas.mpl_connect('button_press_event', self.on_bar_click)
        fig.canvas.mpl_connect('motion_notify_event', self.on_hover)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True, padx=20, pady=20)

if __name__ == "__main__":
    root = Tk()
    obj = FeeManagementTeacher(root, "TYBCA")
    root.mainloop()