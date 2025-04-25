from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from db import get_connection
from PIL import Image, ImageTk

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("College Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Set the geometry of the window
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        #=====title====
        title = Label(self.root, text="Manage Student details", font=("georgia", 20, "bold"), bg="#033054", fg="white").place(x=0, y=0, relwidth=1, height=50)

        #=====variables====
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_city = StringVar()
        self.var_class = StringVar()
        self.var_search = StringVar()  # Add search variable here

        #=====column 1====
        Label(self.root, text="Roll no.", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=80)
        Label(self.root, text="Name", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=130)
        Label(self.root, text="Class", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=180)
        Label(self.root, text="Email", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=230)
        Label(self.root, text="D.O.B", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=280)
        Label(self.root, text="Gender", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=330)
        Label(self.root, text="City", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=430)
        Label(self.root, text="Contact", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=380)
        Label(self.root, text="Address", font=("goudy old style", 18, "bold"), bg="white").place(x=120, y=480)

        #=====Entry fields 1====
        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 16, "bold"), bg="lightyellow")
        self.txt_roll.place(x=230, y=80, width=170)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 16, "bold"), bg="lightyellow").place(x=230, y=130, width=170)
        self.txt_class = ttk.Combobox(self.root, textvariable=self.var_class, values=("Select", "FYBCA", "SYBCA", "TYBCA","FYBSC","SYBSC","TYBSC"), font=("goudy old style", 16, "bold"), state='readonly', justify=CENTER)
        self.txt_class.place(x=230, y=180, width=130)
        self.txt_class.current(0)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 16, "bold"), bg="lightyellow").place(x=230, y=230, width=170)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 16, "bold"), bg="lightyellow").place(x=230, y=280, width=180)
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female"), font=("goudy old style", 16, "bold"), state='readonly', justify=CENTER)
        self.txt_gender.place(x=230, y=330, width=170)
        self.txt_gender.current(0)
        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 16, "bold"), bg="lightyellow").place(x=230, y=380, width=180)
        Entry(self.root, textvariable=self.var_city, font=("goudy old style", 16, "bold"), bg="lightyellow").place(x=230, y=430, width=180)
        self.txt_address = Text(self.root, font=("goudy old style", 16, "bold"), bg="lightyellow")
        self.txt_address.place(x=230, y=480, width=350, height=100)

        #========Buttons===================
        Button(self.root, text="Save", font=("goudy old style", 18, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add).place(x=100, y=620, width=95, height=40)
        Button(self.root, text="Update", font=("goudy old style", 18, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.update).place(x=230, y=620, width=95, height=40)
        Button(self.root, text="Delete", font=("goudy old style", 18, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete).place(x=360, y=620, width=95, height=40)
        Button(self.root, text="Clear", font=("goudy old style", 18, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear).place(x=490, y=620, width=95, height=40)

        #=====Search Panel====
        Label(self.root, text="Select Class", font=("goudy old style", 18, "bold"), bg="white").place(x=720, y=100)
        self.txt_search_class = ttk.Combobox(self.root, textvariable=self.var_search, values=("Select", "FYBCA", "SYBCA", "TYBCA","FYBSC","SYBSC","TYBSC"), font=("goudy old style", 16, "bold"), state='readonly', justify=CENTER)
        self.txt_search_class.place(x=855, y=100, width=180)
        self.txt_search_class.current(0)
        Button(self.root, text="Search", font=("goudy old style", 18, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search).place(x=1090, y=100, width=110, height=28)

        #=====Content====
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=685, y=150, width=810, height=600)

        scroll_y = Scrollbar(self.C_Frame, orient=VERTICAL)
        scroll_x = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        style = ttk.Style()
        style.theme_use("clam")  #Global theme 
        style.configure("Treeview.Heading", background="lightblue", foreground="black", font=("Segoe UI", 15, "bold"))
        style.configure("Treeview",foreground="black", font=("Segoe UI", 13,"bold"), rowheight=35)
        self.subjectTable = ttk.Treeview(self.C_Frame, columns=("class", "roll", "name", "email", "gender", "dob", "contact", "city", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.subjectTable.xview)
        scroll_y.config(command=self.subjectTable.yview)

        self.subjectTable.heading("class", text="Class")
        self.subjectTable.heading("roll", text="Roll no.")
        self.subjectTable.heading("name", text="Name")
        self.subjectTable.heading("email", text="Email")
        self.subjectTable.heading("gender", text="Gender")
        self.subjectTable.heading("dob", text="D.O.B")
        self.subjectTable.heading("contact", text="Contact")
        self.subjectTable.heading("city", text="City")
        self.subjectTable.heading("address", text="Address")
        self.subjectTable["show"] = "headings"
        self.subjectTable.pack(fill=BOTH, expand=1)
        self.subjectTable.bind("<<TreeviewSelect>>", self.get_data)
        self.subjectTable.column("class",anchor=CENTER, width=90)
        self.subjectTable.column("roll",anchor=CENTER, width=80)
        self.subjectTable.column("name",anchor=CENTER, width=190)
        self.subjectTable.column("email",anchor=CENTER, width=180)
        self.subjectTable.column("gender",anchor=CENTER, width=90)
        self.subjectTable.column("dob",anchor=CENTER, width=130)
        self.subjectTable.column("contact",anchor=CENTER, width=100)
        self.subjectTable.column("city",anchor=CENTER, width=85)
        self.subjectTable.column("address",anchor=CENTER, width=170)
        self.show()  # Fetch all records on startup

    def add(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_roll.get() == "" or self.var_class.get() == "Select":
                messagebox.showerror("Error", "Roll no. and class are required", parent=self.root)
            else:
                # Check if the roll number already exists for the selected class
                cur.execute("SELECT * FROM students WHERE roll=? AND student_class=?", (self.var_roll.get(), self.var_class.get()))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Roll no. already present in this class", parent=self.root)
                else:
                    # Insert the student into the database
                    cur.execute("INSERT INTO students (roll, student_name, student_class, email, dob, gender, contact, city, address) VALUES (?, ?, (Select class_id from Classes where class_name=?), ?, ?, ?, ?, ?, ?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_class.get(),
                        self.var_email.get(),
                        self.var_dob.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_city.get(),
                        self.txt_address.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


    def show(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT (Select class_name from Classes where class_id = students.student_class), roll, student_name, email, gender, dob, contact, city, address FROM students")
            rows = cur.fetchall()
            self.subjectTable.delete(*self.subjectTable.get_children())
            for row in rows:
                self.subjectTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll no. should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM students WHERE roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select a student from the list", parent=self.root)
                else:
                    cur.execute("UPDATE students SET student_name=?, student_class=(SELECT class_id FROM Classes WHERE class_name=?), email=?, dob=?, gender=?, contact=?, city=?, address=? WHERE roll=? AND student_class=(SELECT class_id FROM Classes WHERE class_name=?)", (
                        self.var_name.get(),
                        self.var_class.get(),
                        self.var_email.get(),
                        self.var_dob.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_city.get(),
                        self.txt_address.get("1.0", END),
                        self.var_roll.get(),
                        self.var_class.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Select a student record.", parent=self.root)
            else:
                cur.execute("SELECT * FROM students WHERE roll=? ", (self.var_roll.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid student roll no.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete this record?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM students WHERE roll=? AND student_class=(SELECT class_id FROM Classes WHERE class_name=?)", (self.var_roll.get(), self.var_class.get()))
                        con.commit()
                        cur.execute("DELETE FROM results WHERE roll=? AND class_id=(SELECT class_id FROM classes WHERE class_name=?)", (self.var_roll.get(),self.var_class.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_class.set("Select")
        self.var_email.set("")
        self.var_dob.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_city.set("")
        self.txt_address.delete("1.0", END)
        self.var_search.set("")

    def get_data(self, ev):
        # Get the selected item in Treeview
        f = self.subjectTable.focus()
        content = self.subjectTable.item(f)
        row = content.get('values')
        # Check if row is not empty and has the expected number of columns
        if row and len(row) >= 9:
        # Map the correct data fields
            self.var_class.set(row[0])  # Class
            self.var_roll.set(row[1])   # Roll no.
            self.var_name.set(row[2])   # Student name
            self.var_email.set(row[3])  # Email
            self.var_gender.set(row[4]) # Gender
            self.var_dob.set(row[5])    # Date of Birth
            self.var_contact.set(row[6])# Contact
            self.var_city.set(row[7])   # City
                # Address needs special handling since it's a Text widget
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[8]) # Address

    def search(self):
        con = get_connection()
        cur = con.cursor()
        try:
            if self.var_search.get() == "Select":
                messagebox.showerror("Error", "Select class to search", parent=self.root)
            else:
                cur.execute("SELECT (Select class_name from Classes where class_name=?), roll, student_name, email, gender, dob, contact, city, address FROM students where student_class=(Select class_id from Classes where class_name=?)",(self.var_search.get(),self.var_search.get()))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.subjectTable.delete(*self.subjectTable.get_children())
                    for row in rows:
                        self.subjectTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()
