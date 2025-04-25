from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
from student import StudentClass
from result import ResultClass
from db import get_connection
from report import ReportClass
import timetable
from attendance import AttendanceClass
from tkinter import messagebox
from fees import FeeManagementHOD
from feestudent import FeeManagementStudent
from feesTeacher import FeeManagementTeacher
import os
import sys
import sqlite3
class RMS:
    def __init__(self,root,role) :
        self.root = root
        self.role = role
        self.root.title("College Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Set the geometry of the window
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        #=======content_window======
        self.bg_img=Image.open("images/bg.jpg")
        self.bg_img=self.bg_img.resize((1550,750),Image.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg=Label(self.root,image=self.bg_img).place(x=0,y=15,width=1550,height=750)
        #=====title====
        title=Label(self.root,text="College Management System",padx=10,compound=LEFT,font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)
        #=====Menu======
        self.var_result = StringVar()
        self.var_timetable = StringVar()
        M_Frame = LabelFrame(self.root,text="Menus",highlightbackground="red", font=("times new roman",15,"bold"),bg="#BFE763")
        # Create a custom style for root window comboboxes
        style = ttk.Style()
        style.theme_use("clam")  # Use the 'clam' theme for better styling control

        # Configure the custom style
        style.configure(
            "Root.TCombobox",
            fieldbackground="#0b5377",
            background="#0b5377",
            foreground="white",
            bordercolor="#0b5377",
            arrowcolor="white",  # Color of the dropdown arrow
            selectbackground="#0b5377",
            selectforeground="white",
            padding=5
        )

        # Map states to override default behavior
        style.map(
            "Root.TCombobox",
            fieldbackground=[("readonly", "#0b5377")],
            background=[("readonly", "#0b5377"), ("active", "#0b5377")],
            arrowcolor=[("readonly", "white"), ("active", "white")]
        )

        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                             cursor="hand2", command=self.add_student)
        btn_result = ttk.Combobox(M_Frame,textvariable=self.var_result, values=("Results","Add Results", "View Results"), font=("goudy old style", 15, "bold"),state='readonly',style="Root.TCombobox", justify=CENTER,cursor="hand2")
        btn_result.bind("<<ComboboxSelected>>", self.result)
        btn_result.current(0)
        btn_view = Button(M_Frame, text="View Results", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.view_res)
        btn_logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                            cursor="hand2", command=self.logout)
        btn_exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.exit)
        btn_timetable = Button(M_Frame, text="Timetable", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.time_table2)
        com_timetable = ttk.Combobox(M_Frame,textvariable=self.var_timetable, values=("Timetable","Edit Timetable", "View Timetable"), font=("goudy old style", 15, "bold"),state='readonly',style="Root.TCombobox", justify=CENTER,cursor="hand2")
        com_timetable.bind("<<ComboboxSelected>>", self.time_table)
        com_timetable.current(0)
        btn_attendance = Button(M_Frame, text="Attendance", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.attendance)
        btn_fee_hod = Button(M_Frame, text="Fees Manage", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.fees)
        btn_fee_stud = Button(M_Frame, text="Fees Manage", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.fees)
        btn_fee_tea = Button(M_Frame, text="Fees Manage", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.fees)
        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("goudy old style",20,"bold"),bd=10,relief=RIDGE,bg="#0676ad",fg="white")
        
         # Place buttons based on role
        if self.role == "Admin":
            btn_student.place(relx=0.08, y=5, width=130, height=40)
            btn_result.place(relx=0.22, y=5, width=130, height=40)
            btn_logout.place(relx=0.78, y=5, width=130, height=40)
            btn_exit.place(relx=0.92, y=5, width=130, height=40)
            btn_fee_tea.place(relx=0.64,y=5,width=130,height=40)
            btn_timetable.place(relx=0.5, y=5, width=130, height=40)
            btn_attendance.place(relx=0.36, y=5, width=130, height=40)
            M_Frame.place(x=200,y=140,width=screen_width-400,height=80)
            self.lbl_student.place(relx=0.51,y=460,width=220,height=80,anchor=CENTER)
        elif self.role == "Student":
            # Students can only view results
            M_Frame.place(x=300,y=140,width=screen_width-600,height=80)
            btn_view.place(x=130, y=25, width=180, height=40,anchor=CENTER)
            btn_logout.place(x=550, y=5, width=130, height=40)
            btn_fee_stud.place(x=390,y=5,width=130,height=40)
            btn_timetable.place(x=240, y=5, width=130, height=40)
            btn_exit.place(x=700, y=5, width=130, height=40)
        elif self.role == "HOD":
            btn_student.place(x=50, y=5, width=130, height=40)
            btn_result.place(x=200, y=5, width=130, height=40)
            btn_logout.place(x=820, y=5, width=130, height=40)
            btn_exit.place(x=970, y=5, width=130, height=40)
            com_timetable.place(x=500, y=5, width=130, height=40)
            btn_fee_hod.place(x=650,y=5,width=150,height=40)
            btn_attendance.place(x=350, y=5, width=130, height=40)
            M_Frame.place(x=200,y=140,width=screen_width-400,height=80)
            self.lbl_student.place(relx=0.51,y=460,width=220,height=80,anchor=CENTER)
            
        #=====footer====
        footer=Label(self.root,text="College Management System",font=("goudy old style",12,),bg="#262626",fg="white").pack(side=BOTTOM,fill=X,anchor=CENTER)
        self.update()
    
    def fees(self):
        if self.role == "HOD":
            self.new_win=Toplevel(self.root)
            self.new_obj=FeeManagementHOD(self.new_win)
        elif self.role == "Student":
            conn = get_connection()
            cur = conn.cursor()
            # Get class_id from class_name
            cur.execute("SELECT class_id FROM Classes WHERE class_name=?", (class_name,))
            class_id = cur.fetchone()[0]
            conn.close()
            
            self.new_win = Toplevel(self.root)
            self.new_obj = FeeManagementStudent(self.new_win, class_id)
            
        elif self.role == "Admin":
            
            self.new_win = Toplevel(self.root)
            self.new_obj = FeeManagementTeacher(self.new_win, class_name)

        else:
            messagebox.showerror("Error", "Access denied!", parent=self.root)
        
    def result(self,event):
        result=self.var_result.get()
        if result=="Add Results":
            self.new_win=Toplevel(self.root)
            self.new_obj=ResultClass(self.new_win)
        elif result=="View Results":
            self.new_win=Toplevel(self.root)
            self.new_obj=ReportClass(self.new_win)
    
    def time_table(self,event):
        var=self.var_timetable.get()
        if var=="Edit Timetable":
            self.new_win=timetable.edit_timetable_window(self.root)
        elif var=="View Timetable":
            self.new_win=timetable.view_timetable_window(class_name,self.root)
    def time_table2(self):
        self.new_win=timetable.view_timetable_window(class_name,self.root)
    
    def view_res(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ReportClass(self.new_win)
    
    def add_student(self):    
        self.new_win=Toplevel(self.root)
        self.new_obj=StudentClass(self.new_win)    
        
    def attendance(self):    
        self.new_win=Toplevel(self.root)
        self.new_obj=AttendanceClass(self.new_win,class_name)  
        
    def logout(self):
        op=messagebox.askyesno("Confirm","Do you want to logout?",parent=self.root)
        if op:  #True
            self.root.destroy()
            os.system("python login.py") #To import the login file after destroying the dashboard window
    
    def exit(self):
        op=messagebox.askyesno("Confirm","Do you want to exit?",parent=self.root)
        if op: #True
            self.root.destroy() 
        
    def update(self):
        con=get_connection()
        cur=con.cursor()
        try:
            cur.execute("select * from students ")
            cr=cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[{str(len(cr))}]")
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}") 
    
if __name__=="__main__":
    root=Tk()
    role = sys.argv[1]
    class_name = sys.argv[2]
    obj = RMS(root,role)
    root.mainloop()