from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox,font
from db import get_connection
#import pymysql
import os
import sqlite3
class log:
    def __init__(self,root) :
        self.root = root
        self.root.title("Student Result Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Set the geometry of the window
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        
        self.bg_img=Image.open("images/register.jpg")
        self.bg_img = self.bg_img.resize((self.root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg=Label(self.root,image=self.bg_img).place(relwidth=1,relheight=1)
        
        #======Variables==========
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_question=StringVar()
        self.var_email=StringVar()
        self.var_setPass=StringVar()
        self.var_answer=StringVar()
        self.var_classname=StringVar()
        self.roll_list=[]
        self.var_role = StringVar()
        self.var_terms=IntVar()
        values = ["Security Question","Nick name ?","Favourite color ?","First School name ?"]
        roles = ["Select Role","HOD", "Admin", "Student"]
        
        title=Label(self.root,text="Register",font=("georgia",28,"bold"),bg="#0E05A0",fg="white").place(relx=0.5,rely=0.14, anchor='center')

        self.entry1 = Entry(root,textvariable=self.var_fname, font=("goudy old style",19,"bold"),bg="grey",width=15,foreground="white",highlightcolor="white",justify=CENTER)
        self.entry1.insert(0, "First Name")
        self.entry1.bind("<FocusIn>", lambda event: (self.entry1.delete(0, END),self.entry1.configure(highlightthickness=1,bg="grey",highlightcolor="white",foreground="white")) if self.entry1.get() == "First Name" else None)
        self.entry1.bind("<FocusOut>", lambda event: (self.entry1.insert(0, "First Name"), self.entry1.configure(bg="grey",foreground="white")) if self.entry1.get() == "" else None)
        self.entry1.place(relx=0.32,rely=0.187)
        
        self.entry2 = Entry(root, textvariable=self.var_lname,font=("goudy old style",19,"bold"),width=15,bg="grey",foreground="white",highlightcolor="white",justify=CENTER)
        self.entry2.insert(0, "Last Name")
        self.entry2.bind("<FocusIn>", lambda event: (self.entry2.delete(0, END),self.entry2.configure(highlightthickness=1,bg="grey",highlightcolor="white",foreground="white")) if self.entry2.get() == "Last Name" else None)
        self.entry2.bind("<FocusOut>", lambda event: (self.entry2.insert(0, "Last Name"), self.entry2.configure(bg="grey",foreground="white")) if self.entry2.get() == "" else None)
        self.entry2.place(relx=0.544,rely=0.187)
        
        self.entry3 = Entry(root, textvariable=self.var_email,font=("goudy old style",19,"bold"),width=15,bg="grey",foreground="white",highlightcolor="white",justify=CENTER)
        self.entry3.insert(0, "Email")
        self.entry3.bind("<FocusIn>", lambda event: (self.entry3.delete(0, END),self.entry3.configure(highlightthickness=1,bg="grey",highlightcolor="white",foreground="white")) if self.entry3.get() == "Email" else None)
        self.entry3.bind("<FocusOut>", lambda event: (self.entry3.insert(0, "Email"), self.entry3.configure(bg="grey",foreground="white")) if self.entry3.get() == "" else None)
        self.entry3.place(relx=0.32,rely=0.28)

        # Role selection combobox
        self.role = ttk.Combobox(self.root, textvariable=self.var_role,foreground="white", font=("goudy old style", 19, "bold"), style="TCombobox", width=14, values=roles, state='readonly', cursor="hand2")
        self.role.place(relx=0.544, rely=0.28)
        self.role.set("Select Role")
        
        style= ttk.Style()
        style.theme_use('default')
        
        style.map("TCombobox", fieldbackground= [("readonly","grey")], background=[('readonly', 'grey')])
        
        self.question=ttk.Combobox(self.root,textvariable=self.var_question,foreground="white",font=("goudy old style",19,"bold"), style="TCombobox",width=14,values=values,state='readonly',cursor="hand2")
        self.question.place(relx=0.32,rely=0.373)
        self.question.set("Security Question")
        
        
        self.entry4 = Entry(root, textvariable=self.var_answer,font=("goudy old style",19,"bold"),width=15,bg="grey",foreground="white",highlightcolor="white",justify=CENTER)
        self.entry4.insert(0, "Security Answer")
        self.entry4.bind("<FocusIn>", lambda event: (self.entry4.delete(0, END),self.entry4.configure(highlightthickness=1,bg="grey",highlightcolor="white",foreground="white")) if self.entry4.get() == "Security Answer" else None)
        self.entry4.bind("<FocusOut>", lambda event: (self.entry4.insert(0, "Security Answer"), self.entry4.configure(bg="grey",foreground="white")) if self.entry4.get() == "" else None)
        self.entry4.place(relx=0.544,rely=0.373)
        
        self.entry5 = Entry(root,textvariable=self.var_setPass, font=("goudy old style",19,"bold"),width=15,bg="grey",foreground="white",highlightcolor="white",justify=CENTER)
        self.entry5.insert(0, "Set Password")
        self.entry5.bind("<FocusIn>", lambda event: (self.entry5.delete(0, END),self.entry5.configure(highlightthickness=1,highlightcolor="white",foreground="white",bg="grey")) if self.entry5.get() == "Set Password" else None)
        self.entry5.bind("<FocusOut>", lambda event: (self.entry5.insert(0, "Set Password"), self.entry5.configure(foreground="white",bg="grey")) if self.entry5.get() == "" else None)
        self.entry5.place(relx=0.32,rely=0.466)
        
        self.entry6 = Entry(root,textvariable=self.var_classname, font=("goudy old style",19,"bold"),width=15,bg="grey",foreground="white",highlightcolor="white",justify=CENTER)
        self.entry6.insert(0, "Enter Class")
        self.entry6.bind("<FocusIn>", lambda event: (self.entry6.delete(0, END),self.entry6.configure(highlightthickness=1,highlightcolor="white",foreground="white",bg="grey")) if self.entry6.get() == "Enter Class" else None)
        self.entry6.bind("<FocusOut>", lambda event: (self.entry6.insert(0, "Enter Class"), self.entry6.configure(foreground="white",bg="grey")) if self.entry6.get() == "" else None)
        self.entry6.place(relx=0.544,rely=0.466)
        underline_font = font.Font(self.root,size=14,underline=True)
        btn_reg=Button(self.root,text="Login here !!",font=underline_font,bd=0,bg="black",fg="white",activeforeground="white",activebackground="black",cursor="hand2",command=self.login_window).place(relx=0.61,rely=0.74)
        self.terms=Checkbutton(self.root,text="I Agree The Terms",variable=self.var_terms,onvalue=1,offvalue=0,bg="#522FE3",fg="#39FF14",font=("times new roman",13)).place(relx=0.31,rely=0.559)
        btn=Button(self.root,text="Register",font=("times new roman",17,"bold"),bg="white",foreground="black",cursor="hand2",command=self.register_data).place(relx=0.5,rely=0.67,width=300,height=40, anchor='center')

    def clear(self):
        self.entry1.delete(0,END)
        self.entry2.delete(0,END)
        self.entry3.delete(0,END)
        self.entry4.delete(0,END)
        self.entry5.delete(0,END)
        self.entry6.delete(0,END)
        self.role.set("Select Role")
        self.question.set("Security Question")
        
    def login_window(self):
        self.root.destroy()
        os.system("python login.py")  #To import the login file after destroying the register window
    
    def register_data(self):
        if self.entry1.get()=="" or self.entry2.get()=="" or self.entry3.get()=="" or self.entry4.get()=="" or self.entry6.get()=="" or self.question.get()=="Security Question" or self.var_role.get() == "Select Role":
            messagebox.showerror("Error","All Fields are Required",parent=self.root)
        elif self.var_terms.get()==0:
            messagebox.showerror("Error","Please agree the terms and conditions.",parent=self.root)
        else:
            try:
                con=get_connection()
                cur=con.cursor()
                cur.execute("select * from users where email=?",(self.entry3.get(),))
                row=cur.fetchone()
                if row is not None:  #row!=None
                    messagebox.showerror("Error","User already exist, try with another email.",parent=self.root)
                else:        
                    cur.execute("insert into users (first_name,last_name,email,security_question,security_answer,password,role,class_name) values(?,?,?,?,?,?,?,?)",
                                (self.var_fname.get(),
                                 self.var_lname.get(),
                                 self.var_email.get(),
                                 self.var_question.get(),
                                 self.var_answer.get(),
                                 self.var_setPass.get(),
                                 self.var_role.get(),
                                 self.var_classname.get()
                                 ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Registered Successfully",parent=self.root)
                    self.clear()
                    self.login_window()
            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)
                
                
root=Tk()
obj = log(root)
root.mainloop()