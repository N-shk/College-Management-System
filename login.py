from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox,font
from db import get_connection

#import pymysql
import os
import sqlite3
class Login_system:
    def __init__(self,root) :
        self.root = root
        self.root.title("Student Result Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Set the geometry of the window
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.config(bg="white")
        self.root.config(bg="white")
        #====images====
        self.bg_img=Image.open("login.jpg")
        self.bg_img = self.bg_img.resize((self.root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg=Label(self.root,image=self.bg_img).place(relwidth=1,relheight=1)
        #====login frame====
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.values = ["Select","Nick name ?","Favourite color ?","First School name ?"]
        
        title=Label(self.root,text="Login",font=("georgia",33,"bold"),bg="#142D41",fg="white").place(relx=0.5,rely=0.17, anchor='center')
        
        self.email = Entry(root,textvariable=self.var_email, font=("goudy old style",20,"bold"),bg="#142D41",width=26,foreground="gray",highlightcolor="#2ACC72",justify=CENTER)
        self.email.insert(0, " Email address")
        self.email.bind("<FocusIn>", lambda event: (self.email.delete(0, END),self.email.configure(highlightthickness=1,bg="#142D41",highlightcolor="#2ACC72",foreground="#2ACC72")) if self.email.get() == " Email address" else None)
        self.email.bind("<FocusOut>", lambda event: (self.email.insert(0, " Email address"), self.email.configure(bg="#142D41",foreground="gray")) if self.email.get() == "" else None)
        self.email.place(relx=0.5,rely=0.31, anchor='center')
        
        self.passw=Label(self.root,text="Password :",font=("goudy old style",20,"bold"),bg="#142D41",fg="white").place(relx=0.375,rely=0.39)
        underline_font = font.Font(self.root,underline=True,size=12)
        
        self.password = Entry(root,textvariable=self.var_pass,font=("goudy old style",20,"bold"),foreground="#2ACC72",show="*", bg="#142D41",width=16)
        self.password.place(relx=0.47,rely=0.39)
        btn_reg=Button(self.root,text="New User? Register here",font=underline_font,bd=0,bg="#112636",fg="white",activeforeground="white",activebackground="#112636",cursor="hand2",command=self.register_window).place(relx=0.56,rely=0.652)
        btn_forget=Button(self.root,text="Forget password !",font=underline_font,bd=0,bg="#112636",fg="white",activeforeground="white",activebackground="#112636",cursor="hand2",command=self.forget_pass_window).place(relx=0.324,rely=0.652)
        btn=Button(self.root,text="Login",font=("times new roman",17,"bold"),bg="white",foreground="black",cursor="hand2",command=self.login).place(relx=0.5,rely=0.60,width=300,height=40, anchor='center')
    
    def login(self):
        if self.email.get()=="" or self.password.get()=="" :
            messagebox.showerror("Error","All Fields are Required",parent=self.root)
        else:
            try:
                con=get_connection()#for connection
                cur=con.cursor()
                cur.execute("select * from users where email=? and password=?",(self.email.get(),self.password.get()))
                row=cur.fetchone()
                if row is None:  #row==None
                    messagebox.showerror("Error","Invalid username or password",parent=self.root)
                else:
                    role = row[7]
                    messagebox.showinfo("Success",f"Welcome {self.email.get()}",parent=self.root)
                    self.root.destroy()
                    os.system(f"python dashboard.py {role}")
                 
                con.close()
            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)
   
    def forget_pass(self):
        if self.question.get()=="Select" or self.answer1.get()=="" or self.new_password.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root2)
        else:
            try:
                con=get_connection() #for connection
                cur=con.cursor()
                cur.execute("select * from users where email=? and security_question=? and security_answer=?",(self.email.get(),self.question.get(),self.answer1.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, Please enter correct combination of security question and password",parent=self.root2)
                else:
                    cur.execute("update users set password=? where email=?",(self.new_password.get(),self.email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Password changed successfully, login with new pasword.",parent=self.root2)
                    self.root2.destroy()
                    self.email.delete(0, END)  #deleting the field from 0 to end
                    self.email.insert(0," Email address")  #inserting on 0
                    
            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)
    def forget_pass_window(self):
        if self.email.get()==" Email address" or self.email.get()=="":
            messagebox.showerror("Error","Error ! Email field is empty",parent=self.root)
        else:
            try:
                con=get_connection() #for connection
                cur=con.cursor()  #create cursor
                cur.execute("select * from users where email=? ",(self.email.get(),))
                row=cur.fetchone()  #for fetching
                if row is None:
                    messagebox.showerror("Error","Invalid email address",parent=self.root)
                else:
                    self.root2=Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("392x430+310+95")  #width x height + x-axis + y-axis
                    self.root2.focus_force()
                    self.root2.config(bg="white")
                    self.root2.grab_set()
                    self.title_forget=Label(self.root2,text="Set New Password",font=("times new roman",21,"bold"),bg="#142D41",fg="white").place(x=0,relwidth=1,y=1)
                    
                    self.ques=Label(self.root2,text="Security Question",font=("times new roman",18,"bold"),bg="white",fg="black").place(relx=0.5,y=70,anchor='center')
                    self.question=ttk.Combobox(self.root2,foreground="gray",font=("times new roman",16,"bold"), style="TCombobox",width=19,values=self.values,state='readonly',cursor="hand2")
                    self.question.place(relx=0.5,y=100,anchor='center')
                    self.question.current(0)
                    self.answer=Label(self.root2,text="Answer :",font=("times new roman",18,"bold"),bg="white",fg="black").place(relx=0.5,y=165,anchor='center')
                    self.answer1=Entry(self.root2,font=("times new roman",17,"bold"),bg="lightyellow")
                    self.answer1.place(relx=0.5,y=195,width=200,anchor='center')
                    
                    self.new_pass=Label(self.root2,text="New Password : ",font=("times new roman",18,"bold"),bg="white",fg="black").place(relx=0.5,y=260,anchor='center')
                    self.new_password=Entry(self.root2,font=("times new roman",17,"bold"),bg="lightyellow")
                    self.new_password.place(relx=0.5,y=290,width=200,anchor='center')
                    
                    btn_forget=Button(self.root2,text="Change Password",font=("times new roman",19,"bold"),bg="red",foreground="white",cursor="hand2",command=self.forget_pass).place(relx=0.5,y=390,width=260,height=40,anchor='center')
                  
            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)
    
        

            
    def register_window(self):
        self.root.destroy()
        os.system("python register.py") #To import the register file after destroying the login window
root=Tk()
obj = Login_system(root)
root.mainloop()