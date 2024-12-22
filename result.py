from tkinter import *
from tkinter import ttk, messagebox
from db import get_connection
import sqlite3
from PIL import Image, ImageTk

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        # Title
        title = Label(self.root, text="Add Student Result", font=("georgia", 23, "bold"), bg="orange", fg="#262626")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Variables
        self.var_class = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_subject = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()

        # Widgets
        Label(self.root, text="Select Class", font=("goudy old style", 18, "bold"), bg="white").place(x=320, y=100)
        Label(self.root, text="Select Roll no.", font=("goudy old style", 18, "bold"), bg="white").place(x=320, y=160)
        Label(self.root, text="Subject", font=("goudy old style", 18, "bold"), bg="white").place(x=320, y=220)
        Label(self.root, text="Name", font=("goudy old style", 18, "bold"), bg="white").place(x=320, y=280)
        Label(self.root, text="Marks Obtained", font=("goudy old style", 18, "bold"), bg="white").place(x=320, y=340)
        Label(self.root, text="Full Marks", font=("goudy old style", 18, "bold"), bg="white").place(x=320, y=400)

        self.txt_class = ttk.Combobox(self.root, textvariable=self.var_class, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_class.place(x=545, y=100, width=180)
        self.txt_class.bind("<<ComboboxSelected>>", self.update_rolls)  # Fetch roll numbers when class is selected
        self.fetch_classes()

        self.txt_roll = ttk.Combobox(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_roll.place(x=545, y=160, width=180)
        self.txt_roll.bind("<<ComboboxSelected>>", self.fetch_student_name)

        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 20, "bold"), bg="lightyellow", state='readonly').place(x=545, y=280, width=200)

        self.txt_subject = ttk.Combobox(self.root, textvariable=self.var_subject, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_subject.place(x=545, y=220, width=180)

        Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 20, "bold"), bg="lightyellow").place(x=545, y=340, width=200)
        Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 20, "bold"), bg="lightyellow").place(x=545, y=400, width=200)

        # Buttons
        self.btn_add = Button(self.root, text="Submit", font=("times new roman", 15), bg="lightgreen", command=self.add)
        self.btn_add.place(x=420, y=490, width=100, height=35)
        self.btn_clear = Button(self.root, text="Clear", font=("times new roman", 15), bg="lightgray", command=self.clear)
        self.btn_clear.place(x=560, y=490, width=100, height=35)

    # Fetch available classes from the database
    def fetch_classes(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT class_name FROM Classes")
            rows = cur.fetchall()
            if rows:
                self.txt_class['values'] = [row[0] for row in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching classes: {str(ex)}")
        finally:
            con.close()

    # Fetch roll numbers based on selected class
    def update_rolls(self, event):
        con = get_connection()
        cur = con.cursor()
        try:
            class_name = self.var_class.get()
            # Fetch roll numbers based on class_id
            cur.execute("""
                SELECT roll 
                FROM Students 
                WHERE student_class=?""", (class_name,))
            rolls = cur.fetchall()
            if rolls:
                self.txt_roll['values'] = [roll[0] for roll in rolls]
            else:
                messagebox.showerror("error", "No students found for this class.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching roll numbers: {str(ex)}")
        finally:
            con.close()

    # Fetch student name based on selected roll number
    def fetch_student_name(self, event):
        con = get_connection()
        cur = con.cursor()
        try:
            roll_no = self.var_roll.get()
            student_class = self.var_class.get() 
            cur.execute("SELECT student_name FROM Students WHERE roll=? AND student_class=?", (roll_no, student_class))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.fetch_subjects()  # Fetch subjects for the student's class
            else:
                messagebox.showerror("Error", "Student not found!")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching student name: {str(ex)}")
        finally:
            con.close()

    # Fetch subjects based on selected class
    def fetch_subjects(self):
        con = get_connection()
        cur = con.cursor()
        try:
            class_name = self.var_class.get()
            cur.execute("""
                SELECT subject_name 
                FROM Subjects 
                WHERE class_id=(SELECT class_id FROM Classes WHERE class_name=?)""", (class_name,))
            subjects = cur.fetchall()
            if subjects:
                self.txt_subject['values'] = [sub[0] for sub in subjects]
            else:
                self.txt_subject['values'] = []
                messagebox.showinfo("Info", "No subjects found for this class.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching subjects: {str(ex)}")
        finally:
            con.close()

    # Insert result into the Results table
    def add(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_name.get() == "" or self.var_marks.get() == "" or self.var_full_marks.get() == "" or self.var_subject.get()=="":
                messagebox.showerror("Error", "All fields are required!", parent=self.root)
                return

            cur.execute(
                """
                INSERT INTO Results (roll ,class_id,subject_id, marks_obtained, max_marks) 
                VALUES (?,(SELECT class_id FROM classes WHERE class_name=?) ,(SELECT subject_id FROM Subjects WHERE subject_name=?), ?, ?)""",
                (self.var_roll.get(), self.var_class.get(),self.var_subject.get(), self.var_marks.get(), self.var_full_marks.get())
            )
            con.commit()
            messagebox.showinfo("Success", "Result added successfully!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding result: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_class.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_subject.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()
