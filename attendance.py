from tkinter import *
# Add these imports at the top
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Scrollbar, Frame, Label, Entry, Checkbutton, IntVar, Button, VERTICAL
from datetime import date
from db import get_connection  # Custom module for database connection
import sqlite3
import os
import sys
from datetime import date
class AttendanceClass:
    def __init__(self, root, class_name):
        self.root = root
        self.class_name = class_name
        self.root.title("College Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.fixed_date = date.today().strftime('%d %m')
        months = [0,'January', 'February','March','April','May','June','July','August','September','October','November','December']
        self.fixed_date=self.fixed_date[:2]+" "+months[int(self.fixed_date[-2:])]
        # Title
        title = Label(self.root, text="Attendance Submission", font=("georgia", 20, "bold"), bg="orange", fg="#262626")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Display Class Name (Centered at the top)
        class_label = Label(self.root, text=f"Class :  {class_name}\nDate  :  {self.fixed_date}", font=("georgia", 19, "bold"),foreground="purple", bg="white")
        class_label.place(relx=0.18, y=140, anchor=tk.CENTER)

        # Column Headers ("Roll No.", "Name", "Status", "Remark")
        header_frame = Frame(self.root, bg="lightblue")
        header_frame.place(x=530, y=120, width=screen_width - 700, height=30)
        header_frame2 = Frame(self.root, bg="white")
        header_frame2.place(x=875, y=165, width=screen_width - 40, height=30)
        Label(header_frame, text="  Roll No.", font=("arial", 14 , "bold"), bg="lightblue", width=8, anchor="w").grid(row=0, column=0, padx=10)
        Label(header_frame, text="Student Name", font=("arial", 14, "bold"), bg="lightblue", width=15, anchor="w").grid(row=0, column=1, padx=25)
        Label(header_frame, text="Status", font=("arial", 14, "bold"), bg="lightblue", width=18, anchor="w").grid(row=0, column=2, padx=(34))
        Label(header_frame2, text="Present      Absent", font=("arial", 13,"bold"), bg="white", width=18, anchor="w").grid(row=0, column=0)
        Label(header_frame, text="Remark", font=("arial", 14, "bold"), bg="lightblue", width=20, anchor="w").grid(row=0, column=3, padx=(25))

        # Frame for Attendance UI
        container = Frame(self.root, bg="white")
        container.place(x=540, y=190, width=screen_width - 550, height=screen_height - 300)
        
        canvas = Canvas(container, bg="white")
        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        self.student_container = Frame(canvas, bg="white")

        self.student_container.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.student_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Fetch Data and Populate UI
        self.student_data = []
        self.populate_attendance(self.class_name)

         # Chart Frame
        self.chart_frame = Frame(self.root, bg="white")
        self.chart_frame.place(x=15, y=190, width=480, height=400)  # Adjust position as needed
        
        # Initialize Matplotlib figure and canvas
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial chart update
        self.update_chart()

     # Add the update_chart method
    def update_chart(self):
        present = 0
        absent = 0
        for student in self.student_data:
            if student["present_var"].get() == 1:
                present += 1
            elif student["absent_var"].get() == 1:
                absent += 1

        self.ax.clear()
        sizes = [present, absent]

        if sum(sizes) == 0:
            # Clean "No data" state (no borders)
            self.ax.axis('off')  # Disable axis
        else:
            # Custom autopct to show counts directly
            def autopct_format(pct):
                total = sum(sizes)
                count = int(round(pct * total / 100))
                return f'{count}' if count > 0 else ''

            # Plot pie with counts
            self.ax.pie(
                sizes,
                labels=['Presents', 'Absents'],
                autopct=autopct_format,  # Show counts instead of %
                colors=['#4CAF50', '#FF5722'],  # Green/Orange
                textprops={'fontsize': 14, 'color': 'black'},
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                startangle=90
            )
            self.ax.axis('equal')  # Perfect circle

        self.chart_canvas.draw()
        
    def get_students(self, class_name):
        """Fetch students belonging to a specific class, sorted by roll number."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT s.roll, s.student_name, c.class_id
                FROM students s
                JOIN Classes c ON s.student_class = c.class_id
                WHERE c.class_name = ?
                ORDER BY s.roll ASC
            """
            cursor.execute(query, (class_name,))
            students = cursor.fetchall()
            conn.close()
            return students
        except Exception as ex:
            messagebox.showerror("Database Error", f"Error while fetching students: {ex}",parent=self.root)
            return []

    # Populate attendance
    def populate_attendance(self, class_name):
        """Dynamically generate the UI for attendance."""
        students = self.get_students(class_name)
        if not students:
            Label(self.student_container, text="No students found for the assigned class.", font=("arial", 14), bg="white", fg="red").pack()
            return

        for idx, (roll_no, student_name, _) in enumerate(students):
            student_frame = Frame(self.student_container, bg="white")
            student_frame.grid(row=idx, column=0, pady=5, padx=10, sticky="w")

            # Roll Number
            Label(student_frame, text=roll_no, font=("arial", 12,"bold"), bg="white", width=10, anchor="w").grid(row=idx, column=0, padx=5, pady=5)

            # Student Name
            Label(student_frame, text=student_name, font=("arial", 12,"bold"), bg="white", width=20, anchor="w").grid(row=idx, column=1, padx=(20,0), pady=5)

            # Present Checkbox
            present_var = IntVar()
            present_cb = Checkbutton(student_frame,  variable=present_var,fg="Green",activebackground="Green", font=("arial", 12), bg="white")
            present_cb.grid(row=idx, column=2, padx=(5,0))

            # Absent Checkbox
            absent_var = IntVar()
            absent_cb = Checkbutton(student_frame,  variable=absent_var,fg="Red",activebackground="Red", font=("arial", 12), bg="white")
            absent_cb.grid(row=idx, column=3, padx=(45))

            # Link Present and Absent Checkboxes
            def toggle_checkboxes(selected_var, other_var):
                if selected_var.get():
                    other_var.set(0)
            present_var.trace_add('write', lambda *args: self.update_chart())
            absent_var.trace_add('write', lambda *args: self.update_chart())

            present_cb.config(command=lambda pv=present_var, av=absent_var: toggle_checkboxes(pv, av))
            absent_cb.config(command=lambda av=absent_var, pv=present_var: toggle_checkboxes(av, pv))

            # Remark Text Box
            remark_entry = Entry(student_frame, font=("arial", 12), width=30, bd=1, relief=SOLID)
            remark_entry.grid(row=idx, column=4, padx=(70,0))

            # Add student data to the list
            self.student_data.append({"roll": roll_no, "present_var": present_var, "absent_var": absent_var})
        button_frame = Frame(self.student_container, bg="white")
        button_frame.grid(row=len(students) + 1, column=0, pady=10, sticky="se")

        mark_absent_button = Button(
            button_frame,
            text="Mark All Unselected as Absent",
            font=("arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.mark_all_absent,
        )
        mark_absent_button.pack(side=RIGHT, padx=10, pady=10)
        submit_button = Button(
            self.student_container,
            text="Submit Attendance",
            font=("arial", 14, "bold"),
            bg="green",
            fg="white",
            command=self.submit_attendance,
        )
        submit_button.grid(row=len(self.student_data) + 2, column=0, columnspan=4, pady=10, sticky="e")

    def submit_attendance(self):
        """Save attendance data to the database."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Fetch class_id based on class_name
            query = "SELECT class_id FROM Classes WHERE class_name = ?"
            cursor.execute(query, (self.class_name,))
            result = cursor.fetchone()
            class_id = result[0]
            
            # Check if attendance for the specific date and class already exists
            query = "SELECT 1 FROM Attendance WHERE class_id = ? AND date = ?"
            cursor.execute(query, (class_id, self.fixed_date))
            result=cursor.fetchone()
            if result:
                messagebox.showerror(
                    "Duplicate Submission Error",
                    f"Attendance for {self.class_name} on {self.fixed_date} has already been submitted.",parent=self.root
                    )
                return

            # Validate that attendance for all students is marked
            for student in self.student_data:
                if student["present_var"].get() == 0 and student["absent_var"].get() == 0:
                    messagebox.showerror(
                        "Validation Error",
                        f"Attendance for Roll No. {student['roll']} is incomplete. Please mark it as Present or Absent.",parent=self.root)
                    return
                    

            # Insert data into the Attendance table
            for student in self.student_data:
                status = "Present" if student["present_var"].get() == 1 else "Absent"
                cursor.execute(
                    "INSERT INTO Attendance (class_id, roll, date, status) VALUES (?, ?, ?, ?)",
                    (class_id, student["roll"], self.fixed_date, status) 
                )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Attendance data has been saved successfully!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Database Error", f"Error saving attendance data: {ex}",parent=self.root)

            
    # Mark All Unselected as Absent
    def mark_all_absent(self):
        """Mark all unselected checkboxes as Absent."""
        for data in self.student_data:
            if data["present_var"].get() == 0:  # If Present checkbox is not selected
                data["absent_var"].set(1)  # Mark Absent

if __name__ == "__main__":
    root = Tk()
    class_name = sys.argv[1]
    obj = AttendanceClass(root,class_name)
    root.mainloop()
