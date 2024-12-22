from tkinter import *
from PIL import Image,ImageTk
from student import StudentClass
from result import ResultClass
from db import get_connection
from report import ReportClass
from tkinter import messagebox
import os
import sys
import sqlite3
class RMS:
    def __init__(self,root,role) :
        self.root = root
        self.role = role
        self.root.title("Student Result Management System")
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
        title=Label(self.root,text="Students Result Management System",padx=10,compound=LEFT,font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)
        #=====Menu======
        M_Frame = LabelFrame(self.root,text="Menus",highlightbackground="red", font=("times new roman",15,"bold"),bg="#BFE763")
        
        
        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                             cursor="hand2", command=self.add_student)
        btn_result = Button(M_Frame, text="Add Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                            cursor="hand2", command=self.add_result)
        btn_view = Button(M_Frame, text="View Results", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.add_report)
        btn_logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                            cursor="hand2", command=self.logout)
        btn_exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.exit)
        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("goudy old style",20,"bold"),bd=10,relief=RIDGE,bg="#0676ad",fg="white")
        
         # Place buttons based on role
        if self.role == "Admin":
            btn_student.place(relx=0.1, y=5, width=130, height=40)
            btn_result.place(relx=0.26, y=5, width=130, height=40)
            btn_view.place(relx=0.5, y=25, width=180, height=40,anchor=CENTER)
            btn_logout.place(relx=0.625, y=5, width=130, height=40)
            btn_exit.place(relx=0.79, y=5, width=130, height=40)
            M_Frame.place(x=200,y=140,width=screen_width-400,height=80)
            self.lbl_student.place(relx=0.51,y=460,width=220,height=80,anchor=CENTER)
        elif self.role == "Student":
            # Students can only view results
            M_Frame.place(x=300,y=140,width=screen_width-600,height=80)
            btn_view.place(relx=0.51, y=25, width=180, height=40,anchor=CENTER)
            btn_logout.place(relx=0.21, y=5, width=130, height=40)
            btn_exit.place(relx=0.67, y=5, width=130, height=40)
            
        #=====footer====
        footer=Label(self.root,text="SRMS-Student Result Management System",font=("goudy old style",12,),bg="#262626",fg="white").pack(side=BOTTOM,fill=X,anchor=CENTER)
        self.update()
        
    def add_student(self):    
        self.new_win=Toplevel(self.root)
        self.new_obj=StudentClass(self.new_win)
    
    def add_result(self):    
        self.new_win=Toplevel(self.root)
        self.new_obj=ResultClass(self.new_win)
        
    def add_report(self):    
        self.new_win=Toplevel(self.root)
        self.new_obj=ReportClass(self.new_win)
        
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
    obj = RMS(root,role)
    root.mainloop()