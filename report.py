from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from db import get_connection
from PIL import Image, ImageTk

class ReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("College Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="#f2f2f2")
        self.root.focus_force()

        # ===== Title =====
        title = Label(self.root, text="View Results", font=("georgia", 25, "bold"), bg="#ff9800", fg="Blue")
        title.place(x=0, y=0, relwidth=1, height=50)

        # ===== Search =====
        self.var_search = StringVar()
        self.var_class = StringVar()

        Label(self.root, text="Select Class", font=("goudy old style", 19, "bold"), bg="#f2f2f2").place(x=270, y=100)
        Label(self.root, text="Enter Roll No.", font=("goudy old style", 18, "bold"), bg="#f2f2f2").place(x=260, y=160)

        self.txt_class = ttk.Combobox(self.root, textvariable=self.var_class, font=("goudy old style", 15, "bold"), state='readonly', justify=CENTER)
        self.txt_class.place(x=450, y=100, width=180)
        self.fetch_classes()

        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 18, "bold"), bg="lightyellow").place(x=450, y=160, width=180)

        # Search button
        Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", command=self.search).place(x=640, y=160, width=120, height=30)

        # ===== Result Display Area =====
        self.result_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.result_frame.place(x=260, y=250, width=1020, height=400)

        scroll_x = Scrollbar(self.result_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.result_frame, orient=VERTICAL)
        
        style = ttk.Style()
        style.theme_use("clam")  # Global theme
        style.configure("Treeview.Heading", font=("goudy old style", 17, "bold"))
        style.configure("Treeview", font=(16), rowheight=40)
        
        # Add the "overall_percentage" column for the overall percentage
        self.result_table = ttk.Treeview(self.result_frame, columns=("roll", "name", "subject", "marks_obtained", "max_marks", "percentage", "overall_percentage"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x.config(command=self.result_table.xview)
        scroll_y.config(command=self.result_table.yview)

        # Set column headings
        self.result_table.heading("roll", text="Roll No.", anchor=CENTER)
        self.result_table.heading("name", text="Name", anchor=CENTER)
        self.result_table.heading("subject", text="Subject", anchor=CENTER)
        self.result_table.heading("marks_obtained", text="Marks Obtained", anchor=CENTER)
        self.result_table.heading("max_marks", text="Total Marks", anchor=CENTER)
        self.result_table.heading("percentage", text="Percentage", anchor=CENTER)
        self.result_table.heading("overall_percentage", text="Overall", anchor=CENTER)

        self.result_table["show"] = "headings"
        self.result_table.column("roll", anchor=CENTER, width=100)
        self.result_table.column("name", anchor=CENTER, width=130)
        self.result_table.column("subject", anchor=CENTER, width=130)
        self.result_table.column("marks_obtained", anchor=CENTER, width=155)
        self.result_table.column("max_marks", anchor=CENTER, width=120)
        self.result_table.column("percentage", anchor=CENTER, width=120)
        self.result_table.column("overall_percentage", anchor=CENTER, width=150)  # Added this column for overall percentage
        self.result_table.pack(fill=BOTH, expand=1)

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

    def search(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_search.get() == "" or self.var_class.get() == "":
                messagebox.showerror("Error", "Class and Roll no. are required", parent=self.root)
                return

            # Check if the roll number exists for the selected class
            cur.execute("SELECT roll, student_name FROM Students WHERE roll=? AND student_class=(SELECT class_id FROM Classes WHERE class_name=?)",
                        (self.var_search.get(), self.var_class.get()))
            student = cur.fetchone()

            if student:
                self.result_table.delete(*self.result_table.get_children())  # Clear existing data

                # Fetch subjects and marks for the student in the selected class
                cur.execute('''SELECT Subjects.subject_name, Results.marks_obtained, Results.max_marks
                               FROM Results
                               JOIN Subjects ON Results.subject_id = Subjects.subject_id
                               WHERE Results.roll=? AND Subjects.class_id=(SELECT class_id FROM Classes WHERE class_name=?)''',
                            (self.var_search.get(), self.var_class.get()))
                rows = cur.fetchall()

                if rows:
                    total_obtained = 0
                    total_marks = 0
                    for row in rows:
                        subject, marks_obtained, max_marks = row
                        percentage = (marks_obtained / max_marks) * 100
                        self.result_table.insert('', END, values=(student[0], student[1], subject, marks_obtained, max_marks, f"{percentage:.2f}%"))
                        total_obtained += marks_obtained
                        total_marks += max_marks
                    
                    # Calculate overall percentage
                    if total_marks > 0:
                        overall_percentage = (total_obtained / total_marks) * 100
                        self.result_table.insert('', END, values=("", "", "", "", "", "", f"{overall_percentage:.2f}%"))
                else:
                    messagebox.showinfo("Info", "No results found for the selected student.", parent=self.root)
            else:
                messagebox.showerror("Error", "No record found for the provided roll number in this class", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching results: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = ReportClass(root)
    root.mainloop()
