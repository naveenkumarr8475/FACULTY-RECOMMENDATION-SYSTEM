from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import ttkthemes
from tkinter import ttk
import student
import faculty
import admin
import pymysql

window=Tk()
window.title("LOGIN")
window.geometry('1520x780+0+0')
window.resizable(False,False)

def connect():
    try:
        con=pymysql.connect(host="localhost",user="root",password="1726")
        mycursor=con.cursor()
        query='use faculty_recommendation_system'
        mycursor.execute(query)
        messagebox.showinfo("success","CONNECTED@root")
    except:
        messagebox.showerror('Error','couldnt connect @root')

def stdlogin():
    try:
        con=pymysql.connect(host="localhost",user="STUDENT",password="1726")
        mycursor=con.cursor()
        query='use faculty_recommendation_system'
        mycursor.execute(query)
        messagebox.showinfo("success","CONNECTED @student")
        window.destroy()
        student.show_student_page()
    except:
        messagebox.showerror('Error', 'couldnt connect @student')
        
def faclogin():
    try:
        con=pymysql.connect(host="localhost",user="ADMIN",password="1726")
        mycursor=con.cursor()
        query='use faculty_recommendation_system'
        mycursor.execute(query)
        messagebox.showinfo("success","CONNECTED @teacher")
        #y = faculty_id_entry.get()
        window.destroy()
        faculty.show_faculty_page()
    except:
        messagebox.showerror('Error', 'couldnt connect @teacher')
        
def adminlogin():
    try:
        con=pymysql.connect(host="localhost",user="ADMIN",password="1726")
        mycursor=con.cursor()
        query='use faculty_recommendation_system'
        mycursor.execute(query)
        messagebox.showinfo("success","CONNECTED@admin")
        window.destroy()
        admin.show_admin_page()
    except:
        messagebox.showerror('Error', 'couldnt connect @ADMIN')

def start():
    connect()
    #Background Image
    bg1=Image.open('bg1.jpg')
    bg1 = bg1.resize((1520, 780), Image.LANCZOS)
    bgImage=ImageTk.PhotoImage(bg1) #png -only PhotoImage
    bgLabel=Label(window,image=bgImage)
    bgLabel.place(x=-5,y=-5)

    #Student_Login
    stdlogin_frame=Frame(window, bg='white')
    stdlogin_frame.place(x=150,y=350)
    stdlogin_image = Image.open('studentlogin.png')
    stdlogin_image = stdlogin_image.resize((100, 100), Image.LANCZOS)
    stdlogin_photo = ImageTk.PhotoImage(stdlogin_image)
    stdlogin_label=Label(stdlogin_frame,image=stdlogin_photo,bg='white')
    stdlogin_label.grid(row=0,column=0,columnspan=2,pady=10)
    srn_label=Label(stdlogin_frame,text="SRN",compound=LEFT,font=('times new roman',20,'bold'),bg='white')
    srn_label.grid(row=2,column=0,pady=10,padx=20)
    srn_entry=Entry(stdlogin_frame,font=('times new roman',18,'bold'),bd=3,fg='royalblue',state='normal')
    srn_entry.grid(row=2,column=1,pady=10,padx=20)
    password_label=Label(stdlogin_frame,text="PASSWORD",compound=LEFT,font=('times new roman',20,'bold'),bg='white')
    password_label.grid(row=3,column=0,pady=10,padx=20)
    password_entry = Entry(stdlogin_frame, font=('times new roman', 18, 'bold'), bd=3, show='*',state='normal')
    password_entry.grid(row=3, column=1, pady=10, padx=20)
    login_button = Button(stdlogin_frame, text="LOGIN", font=('times new roman', 18, 'bold'), bd=3, bg='royalblue',fg='white',cursor='hand2',command=stdlogin)
    login_button.grid(row=4, column=0, columnspan=2, pady=10)

    #Faculty_login
    faclogin_frame = Frame(window, bg='white')
    faclogin_frame.place(x=950, y=350)
    faclogin_image = Image.open('faclogin.png')
    faclogin_image = faclogin_image.resize((100, 100), Image.LANCZOS)
    faclogin_photo = ImageTk.PhotoImage(faclogin_image)
    faclogin_label = Label(faclogin_frame, image=faclogin_photo,bg='white')
    faclogin_label.grid(row=0, column=0, columnspan=2, pady=10)
    faculty_id_label = Label(faclogin_frame, text="FACULTY ID", compound=LEFT, font=('times new roman', 20, 'bold'), bg='white')
    faculty_id_label.grid(row=2, column=0, pady=10, padx=20)
    faculty_id_entry = Entry(faclogin_frame, font=('times new roman', 18, 'bold'), bd=3, fg='royalblue')
    faculty_id_entry.grid(row=2, column=1, pady=10, padx=20)
    faculty_password_label = Label(faclogin_frame, text="PASSWORD", compound=LEFT, font=('times new roman', 20, 'bold'), bg='white')
    faculty_password_label.grid(row=3, column=0, pady=10, padx=20)
    faculty_password_entry = Entry(faclogin_frame, font=('times new roman', 18, 'bold'), bd=3, show='*')
    faculty_password_entry.grid(row=3, column=1, pady=10, padx=20)
    faculty_login_button = Button(faclogin_frame, text="LOGIN", font=('times new roman', 18, 'bold'), bd=3, bg='royalblue',fg='white',cursor='hand2')
    faculty_login_button.grid(row=4, column=0, columnspan=2, pady=10)

    #Admin_login
    adminlogin_frame = Frame(window, bg='white')
    adminlogin_frame.place(x=1200, y=25)
    admin_image = Image.open('admin.png')
    admin_image = admin_image.resize((50, 50), Image.LANCZOS)
    admin_photo = ImageTk.PhotoImage(admin_image)
    admin_label = Label(adminlogin_frame, image=admin_photo, bg='silver')
    admin_label.grid(row=0, column=0,pady=10 ,padx=10)
    admin_login_button = Button(adminlogin_frame, text="ADMIN LOGIN", font=('times new roman', 18, 'bold'), bd=3, bg='royalblue',fg='white',cursor='hand2',command=adminlogin)
    admin_login_button.grid(row=0, column=1,pady=10 ,padx=10)

    window.mainloop()

start()
