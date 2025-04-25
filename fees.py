from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import qrcode
from io import BytesIO
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from db import get_connection

class FeeManagementHOD:
    def __init__(self, root):
        self.root = root
        self.root.title("Fee Management - HOD")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        
        # Add protocol for window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Title
        title = Label(self.root, text="Fee Management System", font=("georgia", 20, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)
        self.var_roll = StringVar()
        
        # Left Frame - Fee Input
        left_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_frame.place(relx=0.18, y=80, width=500, height=screen_height-100)
        
        # Input Frame Title
        input_title = Label(left_frame, text="Fee Details Input", font=("times new roman", 20), bg="#033054", fg="white")
        input_title.place(x=0, y=0, relwidth=1, height=40)
        
        # Input Fields
        lbl_roll = Label(left_frame, text="Roll No:", font=("times new roman", 19), bg="white")
        lbl_roll.place(x=20, y=140)
        self.roll_combo = ttk.Combobox(left_frame, textvariable=self.var_roll, font=("goudy old style", 17, "bold"), state='readonly', justify=CENTER)
        self.roll_combo.place(x=150, y=140, width=200)
        
        lbl_class = Label(left_frame, text="Class:", font=("times new roman", 19), bg="white")
        lbl_class.place(x=20, y=60)
        self.class_combo = ttk.Combobox(left_frame, font=("times new roman", 17), state="readonly")
        self.class_combo['values'] = self.fetch_classes()
        self.class_combo.place(x=150, y=60, width=200)
        self.class_combo.bind("<<ComboboxSelected>>",self.update_rolls)
        
        lbl_dept = Label(left_frame, text="Department:", font=("times new roman", 19), bg="white")
        lbl_dept.place(x=20, y=220)
        self.dept_combo = ttk.Combobox(left_frame, font=("times new roman", 17), state="readonly")
        self.dept_combo['values'] = ("CSE", "IT", "ECE", "EEE", "MECH")
        self.dept_combo.place(x=150, y=220, width=200)
        
        lbl_type = Label(left_frame, text="Fee Type:", font=("times new roman", 19), bg="white")
        lbl_type.place(x=20, y=300)
        self.type_combo = ttk.Combobox(left_frame, font=("times new roman", 17), state="readonly")
        self.type_combo['values'] = ("Tuition Fee", "Exam Fee", "Laboratory Fee", "Library Fee", "Other")
        self.type_combo.place(x=150, y=300, width=200)
        
        lbl_amount = Label(left_frame, text="Amount:", font=("times new roman", 19), bg="white")
        lbl_amount.place(x=20, y=380)
        self.txt_amount = Entry(left_frame, font=("times new roman", 18), bg="lightyellow")
        self.txt_amount.place(x=150, y=380, width=200)
        
        # Buttons
        btn_add = Button(left_frame, text="Add Fee", font=("times new roman", 21, "bold"), bg="#033054", fg="white",
                        cursor="hand2", command=self.add_fee)
        btn_add.place(x=150, y=480, width=150, height=35)
        
        # Right Frame - Visualizations
        right_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        right_frame.place(relx=0.5, y=80, width=800, height=900)
        
        # Visualization Title
        viz_title = Label(right_frame, text="Fee Analysis", font=("times new roman", 20), bg="#033054", fg="white")
        viz_title.place(x=0, y=0, relwidth=1, height=40)
        
        # Visualization Options
        self.view_by = StringVar()
        self.filter_label = Label(right_frame, font=("times new roman", 19),bg="white")
        self.filter_label.place(x=325,y=95)
        
        rb_class = Radiobutton(right_frame, text="Class-wise", variable=self.view_by, value="class",
                              font=("times new roman", 19), bg="white", command=self.update_filter_combo)
        rb_class.place(x=225, y=50)
        
        rb_dept = Radiobutton(right_frame, text="Department-wise", variable=self.view_by, value="department",
                             font=("times new roman", 19), bg="white", command=self.update_filter_combo)
        rb_dept.place(x=425, y=50)
        self.filter_combo = ttk.Combobox(right_frame, font=("times new roman",17,"bold"),width=11,state='readonly')
        self.filter_combo.bind('<<ComboboxSelected>>', lambda e: self.update_visualization())
        self.filter_combo.place(x=325,y=135)
        self.view_by.set('student')
        # Canvas for Matplotlib
        self.fig_frame = Frame(right_frame, bg="white")
        self.fig_frame.place(x=145, y=180, width=500, height=screen_height-250)
        self.update_visualization()
    
        # Fetch roll numbers based on selected class
    def update_rolls(self, event):
        con = get_connection()
        cur = con.cursor()
        try:
            class_name = self.class_combo.get()
            # Fetch roll numbers based on class_id
            cur.execute("""
                SELECT roll 
                FROM Students 
                WHERE student_class=(SELECT class_id FROM Classes WHERE class_name=?)""", (class_name,))
            rolls = cur.fetchall()
            if rolls:
                self.roll_combo['values'] = [roll[0] for roll in rolls]
            else:
                messagebox.showerror("error", "No students found for this class.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching roll numbers: {str(ex)}")
        finally:
            con.close()
    
    def update_filter_combo(self):
        """Update filter combobox values based on selected view type"""
        if self.view_by.get() == "class":
            # Get class names from database
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT class_name FROM Classes")
            class_names = [row[0] for row in cursor.fetchall()]
            conn.close()
            self.filter_combo['values'] = class_names
            self.filter_combo.set('')  # Clear current selection
            self.filter_label.config(text="Select Class:")
        elif self.view_by.get() == "department": # department view
            departments = ['IT', 'Medical', 'Mechanical']
            self.filter_combo['values'] = departments
            self.filter_combo.set('')  # Clear current selection
            self.filter_label.config(text="Select Department:")
        else:
            self.filter_combo['values'] = []
            
    def on_closing(self):
        """Handle window closing properly"""
        plt.close('all')  # Close all matplotlib figures
        self.root.quit()
        self.root.destroy()
    
    def clear_fields(self):
        self.roll_combo.set('')
        self.class_combo.set('')
        self.dept_combo.set('')
        self.type_combo.set('')
        self.txt_amount.delete(0, END)

    def fetch_classes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT class_name FROM Classes")
        classes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return classes

    def add_fee(self):
        if not all([self.var_roll.get(), self.class_combo.get(), self.dept_combo.get(),
                   self.type_combo.get(), self.txt_amount.get()]):
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Get class_id
            cursor.execute("SELECT class_id FROM Classes WHERE class_name=?", (self.class_combo.get(),))
            class_id = cursor.fetchone()[0]

            # Insert fee record
            cursor.execute("""
                INSERT INTO Fees (roll, class_id, department, fee_type, amount, payment_date)
                VALUES (?, ?, ?, ?, ?, DATE('now'))
            """, (
                self.var_roll.get(),
                class_id,
                self.dept_combo.get(),
                self.type_combo.get(),
                float(self.txt_amount.get())
            ))

            # Calculate total paid fees for this student
            cursor.execute("""
                SELECT SUM(f.amount) as total_paid, cf.total_fees
                FROM Fees f
                JOIN ClassFees cf ON f.class_id = cf.class_id
                WHERE f.roll = ? AND f.class_id = ?
                GROUP BY f.roll, cf.class_id, cf.total_fees     
            """, (self.var_roll.get(),class_id))

            result = cursor.fetchone()
            if result:
                total_paid, total_fees = result

                # Update student's fee status
                new_status = 'Paid' if total_paid >= total_fees else 'Pending'
                cursor.execute("""
                    UPDATE Students 
                    SET fee_status = ?
                    WHERE roll = ? AND student_class = ?
                """, (new_status, self.var_roll.get(),class_id))

            conn.commit()
            messagebox.showinfo("Success", "Fee added successfully!", parent=self.root)
            self.clear_fields()
            self.update_visualization()

        except Exception as e:
            messagebox.showerror("Error", f"Error adding fee: {str(e)}", parent=self.root)
        finally:
            conn.close()

    def update_visualization(self):
        # Clear previous visualization
        for widget in self.fig_frame.winfo_children():
            widget.destroy()

        conn = get_connection()
        cursor = conn.cursor()

        if self.filter_combo.get():  # If a class is selected
            cursor.execute("""
                SELECT fee_status, COUNT(*) as count
                FROM Students s
                JOIN Classes c ON s.student_class = c.class_id
                WHERE c.class_name = ?
                GROUP BY fee_status
            """, (self.filter_combo.get(),))

        elif self.filter_combo.get():  # If a department is selected
            cursor.execute("""
                SELECT fee_status, COUNT(*) as count
                FROM Students
                WHERE department = ?
                GROUP BY fee_status
            """, (self.filter_combo.get(),))
        else:
            cursor.execute("""
                SELECT fee_status, COUNT(*) as count
                FROM Students
                GROUP BY fee_status
            """)
        
        data = dict(cursor.fetchall())
        paid_count = data.get('Paid', 0)
        pending_count = data.get('Pending', 0)
        
        conn.close()

        if not data:
            Label(self.fig_frame, text="No data available", font=("times new roman", 15), bg="white").pack(expand=True)
            return
            
        # Create visualization
        fig = plt.figure(figsize=(6,4))
        fig.patch.set_facecolor('white')
        
        self.ax = plt.gca()
        self.bars = plt.bar(['Paid', 'Pending'], [paid_count, pending_count],
                      color=['#2ecc71', '#e74c3c'])
        
        plt.ylabel('Number of Students',fontsize = 12)
        plt.title('Fee Status Distribution',fontsize = 15)
        
        # Add value labels on top of bars
        for bar in self.bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom',fontsize = 14)
    
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    # Choose which class to run based on role
    obj = FeeManagementHOD(root)  # For HOD
    root.mainloop()