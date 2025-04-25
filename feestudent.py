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

class FeeManagementStudent:
    def __init__(self, root, student_roll,class_id):
        self.root = root
        self.student_roll = student_roll
        self.class_id = class_id
        self.root.title("Fee Payment Portal")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        
        # Title
        title = Label(self.root, text="Student Fee Payment Portal", font=("georgia", 20, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=0, relwidth=1, height=50)
        
        # Left Frame - Fee Details
        left_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        left_frame.place(x=20, y=70, width=600, height=screen_height-100)
        
        # Student Info
        self.load_student_info()
        
        info_frame = Frame(left_frame, bg="white")
        info_frame.place(x=20, y=20, width=560, height=150)
        
        Label(info_frame, text=f"Name: {self.student_name}", font=("times new roman", 15, "bold"), bg="white").pack(anchor=W, pady=5)
        Label(info_frame, text=f"Roll No: {self.student_roll}", font=("times new roman", 15), bg="white").pack(anchor=W, pady=5)
        Label(info_frame, text=f"Class: {self.class_name}", font=("times new roman", 15), bg="white").pack(anchor=W, pady=5)
        
        # Pending Fees Table
        table_frame = Frame(left_frame, bg="white")
        table_frame.place(x=20, y=180, width=560, height=400)
        
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        
        self.fee_table = ttk.Treeview(table_frame, columns=("type", "amount", "date"),
                                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        scroll_y.config(command=self.fee_table.yview)
        scroll_x.config(command=self.fee_table.xview)
        
        self.fee_table.heading("type", text="Fee Type")
        self.fee_table.heading("amount", text="Amount")
        self.fee_table.heading("date", text="Date")
        
        self.fee_table["show"] = "headings"
        
        self.fee_table.column("type", width=150)
        self.fee_table.column("amount", width=100)
        self.fee_table.column("date", width=100)
        
        self.fee_table.pack(fill=BOTH, expand=1)
        
        self.load_fee_details()
        
        # Right Frame - Payment
        right_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        right_frame.place(x=640, y=70, width=screen_width-680, height=screen_height-100)
        
        # Payment Frame
        payment_frame = Frame(right_frame, bg="white")
        payment_frame.place(x=20, y=20, width=screen_width-720, height=screen_height-140)
        
        Label(payment_frame, text="Make Payment", font=("times new roman", 20, "bold"), bg="white").pack(pady=20)
        
        # Select Fee
        Label(payment_frame, text="Select Fee to Pay:", font=("times new roman", 15), bg="white").pack(pady=10)
        self.fee_id_var = StringVar()
        self.fee_combo = ttk.Combobox(payment_frame, textvariable=self.fee_id_var, font=("times new roman", 13),
                                     state="readonly", width=30)
        self.update_fee_combo()
        self.fee_combo.pack(pady=5)
        
        # Payment Method
        Label(payment_frame, text="Select Payment Method:", font=("times new roman", 15), bg="white").pack(pady=10)
        self.payment_method = StringVar()
        methods = ['UPI', 'Net Banking']
        for method in methods:
            Radiobutton(payment_frame, text=method, variable=self.payment_method, value=method,
                       font=("times new roman", 12), bg="white").pack(padx=5)
        
        # QR Code Frame
        self.qr_frame = Frame(payment_frame, bg="white")
        self.qr_frame.pack(pady=20)
        
        # Generate QR Button
        Button(payment_frame, text="Generate Payment QR", command=self.generate_qr,
               font=("times new roman", 15, "bold"), bg="#033054", fg="white").pack(pady=20)
        
        self.fee_combo.bind('<<ComboboxSelected>>', self.on_fee_select)

    def load_student_info(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT student_name, (SELECT class_name FROM classes WHERE class_id =?)
                FROM students
                WHERE roll = ? AND student_class=?
            """, (self.class_id,self.student_roll,self.class_id))
            
            self.student_name, self.class_name = cursor.fetchone()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading student info: {str(e)}", parent=self.root)

    def load_fee_details(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fee_type, amount, payment_date
                FROM Fees
                WHERE roll = ? AND class_id=?
            """, (self.student_roll,self.class_id))
            
            self.fee_table.delete(*self.fee_table.get_children())
            
            for row in cursor.fetchall():
                self.fee_table.insert('', END, values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading fee details: {str(e)}", parent=self.root)

    def update_fee_combo(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT total_fees
                FROM classfees
                WHERE class_id = ? 
            """, (self.class_id,))
            fees = cursor.fetchall()
            a=fees[0][0]/4
            self.fee_combo['values']=[f"₹ {a*i}" for i in range(1,5)]
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating fee selection: {str(e)}", parent=self.root)

    def on_fee_select(self, event=None):
        if not self.payment_method.get():
            messagebox.showwarning("Warning", "Please select a payment method first!", parent=self.root)
            self.fee_combo.set('')
            return

    def generate_qr(self):
        if not self.fee_id_var.get() or not self.payment_method.get():
            messagebox.showwarning("Warning", "Please select both fee and payment method!", parent=self.root)
            return
        
        try:
            # Clear previous QR code
            for widget in self.qr_frame.winfo_children():
                widget.destroy()
            
            fee_id = self.fee_id_var.get().split('-')[0].replace('ID: ', '').strip()
            
            # Get fee details
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT amount FROM Fees WHERE fee_id = ?", (fee_id,))
            amount = cursor.fetchone()[0]
            
            # Generate payment info
            payment_info = {
                "fee_id": fee_id,
                "amount": amount,
                "roll": self.student_roll,
                "payment_method": self.payment_method.get(),
                "timestamp": datetime.now().strftime("%Y%m%d%H%M%S")
            }
            
            # Create QR code
            qr = qrcode.QRCode(version=1, box_size=2, border=3)
            qr.add_data(str(payment_info))
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to PhotoImage
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Display QR
            qr_label = Label(self.qr_frame, image=qr_photo, bg="white")
            qr_label.image = qr_photo
            qr_label.pack()
            
            # Add amount label
            Label(self.qr_frame, text=f"Amount to Pay: ₹{amount:,.2f}", 
                  font=("times new roman", 15, "bold"), bg="white").pack(pady=10)
            
            # Add payment button
            Button(self.qr_frame, text="Confirm Payment", command=lambda: self.process_payment(fee_id),
                   font=("times new roman", 15, "bold"), bg="#27ae60", fg="white").pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating QR code: {str(e)}", parent=self.root)

    def process_payment(self, fee_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Update fee status
            cursor.execute("""
                UPDATE Fees 
                SET 
                    payment_date = CURRENT_DATE
                WHERE fee_id = ?
            """, (fee_id,))
            
            # Add transaction record
            cursor.execute("""
                INSERT INTO Fee_Transactions 
                (roll, fee_id, payment_mode, transaction_date, transaction_amount, transaction_status)
                SELECT roll, fee_id, ?, CURRENT_DATE, amount, 'Successful'
                FROM Fees
                WHERE fee_id = ?
            """, (self.payment_method.get(), fee_id))
            
            conn.commit()
            
            messagebox.showinfo("Success", "Payment processed successfully!", parent=self.root)
            
            # Refresh displays
            self.load_fee_details()
            self.update_fee_combo()
            
            # Clear QR frame
            for widget in self.qr_frame.winfo_children():
                widget.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing payment: {str(e)}", parent=self.root)
        finally:
            conn.close()
if __name__ == "__main__":
    root = Tk()
    # Choose which class to run based on role
    #obj = FeeManagementHOD(root)  # For HOD
    #obj = FeeManagementTeacher(root)  # For Teacher
    obj = FeeManagementStudent(root, "102",3)  # For Student
    root.mainloop()