from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import ttkthemes
from tkinter import ttk
import pymysql

table=None

con=pymysql.connect(host="localhost",user="STUDENT",password="1726")
mycursor=con.cursor()
query='use faculty_recommendation_system'
mycursor.execute(query)

def exit_func():
    student.destroy()

def fil_teacher_func():
    global search_window
    search_window = Toplevel()
    search_window.title("SEARCH TEACHER")
    search_window.grab_set()
    search_window.resizable(False, False)

    dept_name_label = ttk.Label(search_window, text="Department Name", font=('times new roman', 18, 'bold'))
    dept_name_label.grid(row=1, column=0, padx=15, pady=10, sticky=W)
    dept_name_entry = Entry(search_window, font=('times new roman', 10))
    dept_name_entry.grid(row=1, column=1, padx=15, pady=10)

    more_than_x_no_of_exp_label = ttk.Label(search_window, text="More than X years of experience", font=('times new roman', 18, 'bold'))
    more_than_x_no_of_exp_label.grid(row=2, column=0, padx=15, pady=10, sticky=W)
    more_than_x_no_of_exp_entry = Entry(search_window, font=('times new roman', 10))
    more_than_x_no_of_exp_entry.grid(row=2, column=1, padx=15, pady=10)

    project_title_label = ttk.Label(search_window, text="Project Title", font=('times new roman', 18, 'bold'))
    project_title_label.grid(row=3, column=0, padx=15, pady=10, sticky=W)
    project_title_entry = Entry(search_window, font=('times new roman', 10))
    project_title_entry.grid(row=3, column=1, padx=15, pady=10)

    paper_title_label = ttk.Label(search_window, text="Paper Title", font=('times new roman', 18, 'bold'))
    paper_title_label.grid(row=4, column=0, padx=15, pady=10, sticky=W)
    paper_title_entry = Entry(search_window, font=('times new roman', 10))
    paper_title_entry.grid(row=4, column=1, padx=15, pady=10)

    def search_button_callback():
        entry_values = [
            dept_name_entry.get(),
            more_than_x_no_of_exp_entry.get(),
            project_title_entry.get(),
            paper_title_entry.get()
        ]
        find_teacher_func(entry_values)

    search_button = ttk.Button(search_window, text="SEARCH", command=search_button_callback)
    search_button.grid(row=5, columnspan=2, padx=15, pady=10)

def find_teacher_func(entry_values):
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('TEACHER_ID', 'TEACHER_NAME','DEPT_NAME','TEACHER_MOBILE_NO', 'TEACHER_EMAIL', 'YEARS_OF_EXPERTISE', 'GRADUATION'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('TEACHER_ID', text='ID', anchor=CENTER)
    table.heading('TEACHER_NAME', text='NAME', anchor=CENTER)
    table.heading('DEPT_NAME', text='DEPT_NAME', anchor=CENTER)
    table.heading('TEACHER_MOBILE_NO', text='PHONE', anchor=CENTER)
    table.heading('TEACHER_EMAIL', text='MAIL', anchor=CENTER)
    table.heading('YEARS_OF_EXPERTISE', text='EXPERIENCE', anchor=CENTER)
    table.heading('GRADUATION', text='GRADUATION', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)

    query = '''
    SELECT DISTINCT 
        TEACHER.TEACHER_ID, 
        TEACHER.TEACHER_NAME, 
        DEPARTMENT.DEPT_NAME, 
        TEACHER.TEACHER_MOBILE_NO, 
        TEACHER.TEACHER_EMAIL,
        TEACHER.YEARS_OF_EXPERTISE, 
        TEACHER.GRADUATION
    FROM TEACHER
    LEFT JOIN DEPARTMENT ON TEACHER.DEPT_ID = DEPARTMENT.DEPT_ID
    LEFT JOIN PAPER ON TEACHER.TEACHER_ID = PAPER.PUBLISHED_BY
    LEFT JOIN PROJECT ON TEACHER.TEACHER_ID = PROJECT.TEACHER_ID
    WHERE
        TEACHER.DEPT_ID IN (SELECT DEPT_ID FROM DEPARTMENT WHERE DEPT_NAME = %s) OR
        TEACHER.YEARS_OF_EXPERTISE > %s OR
        PROJECT.PROJECT_TITLE = %s OR
        PAPER.PAPER_TITLE = %s
'''


    try:
        mycursor.execute(query,[value if value else None for value in entry_values])
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def fil_team_func():
    global search_window
    search_window = Toplevel()
    search_window.title("SEARCH TEAM")
    search_window.grab_set()
    search_window.resizable(False, False)

    teacher_id_label = ttk.Label(search_window, text="TEACHER ID", font=('times new roman', 18, 'bold'))
    teacher_id_label.grid(row=1, column=0, padx=15, pady=10, sticky=W)
    teacher_id_entry = Entry(search_window, font=('times new roman', 10))
    teacher_id_entry.grid(row=1, column=1, padx=15, pady=10)

    domain_label = ttk.Label(search_window, text="INTEREST", font=('times new roman', 18, 'bold'))
    domain_label.grid(row=4, column=0, padx=15, pady=10, sticky=W)
    domain_entry = Entry(search_window, font=('times new roman', 10))
    domain_entry.grid(row=4, column=1, padx=15, pady=10)

    def search_button_callback():
        entry_values = [
            teacher_id_entry.get(),
            teacher_id_entry.get(),
            domain_entry.get(),
        ]
        find_team_func(entry_values)

    search_button = ttk.Button(search_window, text="SEARCH", command=search_button_callback)
    search_button.grid(row=5, columnspan=2, padx=15, pady=10)

def find_team_func(entry_values):
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('TEAM_ID', 'PROJECT_TITLE', 'TEAM_HEAD', 'STATUS', 'TEACHER_NAME', 'DOMAIN_NAME'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('TEAM_ID', text='Team ID', anchor=CENTER)
    table.heading('PROJECT_TITLE', text='Project Title', anchor=CENTER)
    table.heading('TEAM_HEAD', text='Team Head', anchor=CENTER)
    table.heading('STATUS', text='Status', anchor=CENTER)
    table.heading('TEACHER_NAME', text='Teacher Name', anchor=CENTER)
    table.heading('DOMAIN_NAME', text='Domain Name', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)


    query = ''' 
    SELECT 
        TEAM.TEAM_ID, 
        PROJECT.PROJECT_TITLE, 
        TEAM.TEAM_HEAD, 
        TEAM.STATUS, 
        TEACHER.TEACHER_NAME, 
        PROJECT.DOMAIN_NAME
    FROM TEAM
    LEFT JOIN TEAM_PROJECT_RELATION ON TEAM.TEAM_ID = TEAM_PROJECT_RELATION.TEAM_ID
    LEFT JOIN PROJECT ON TEAM_PROJECT_RELATION.PROJECT_ID = PROJECT.PROJECT_ID
    LEFT JOIN TEACHER ON PROJECT.TEACHER_ID = TEACHER.TEACHER_ID
    WHERE
        (TEAM.TEAM_ID IN (
            SELECT TPR.TEAM_ID 
            FROM TEAM_PROJECT_RELATION TPR
            JOIN PROJECT P ON TPR.PROJECT_ID = P.PROJECT_ID
            WHERE P.TEACHER_ID = %s
        ) AND PROJECT.TEACHER_ID = %s)
        OR PROJECT.DOMAIN_NAME = %s;
'''    



    try:
        mycursor.execute(query,[value if value else None for value in entry_values])
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def fil_project_func():
    global search_window
    search_window = Toplevel()
    search_window.title("SEARCH PROJECT")
    search_window.grab_set()
    search_window.resizable(False, False)

    teacher_id_label = ttk.Label(search_window, text="TEACHER ID", font=('times new roman', 18, 'bold'))
    teacher_id_label.grid(row=1, column=0, padx=15, pady=10, sticky=W)
    teacher_id_entry = Entry(search_window, font=('times new roman', 10))
    teacher_id_entry.grid(row=1, column=1, padx=15, pady=10)

    domain_label = ttk.Label(search_window, text="INTEREST", font=('times new roman', 18, 'bold'))
    domain_label.grid(row=4, column=0, padx=15, pady=10, sticky=W)
    domain_entry = Entry(search_window, font=('times new roman', 10))
    domain_entry.grid(row=4, column=1, padx=15, pady=10)

    def search_button_callback():
        entry_values = [
            teacher_id_entry.get(),
            domain_entry.get(),
        ]
        find_project_func(entry_values)

    search_button = ttk.Button(search_window, text="SEARCH", command=search_button_callback)
    search_button.grid(row=5, columnspan=2, padx=15, pady=10)

def find_project_func(entry_values):
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('PROJECT_ID','PROJECT_TITLE', 'TEACHER_NAME', 'DOMAIN_NAME','PROBLEM_STATEMENT'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('PROJECT_ID', text='Project ID', anchor=CENTER)
    table.heading('PROJECT_TITLE', text='Project Title', anchor=CENTER)
    table.heading('TEACHER_NAME', text='Teacher Name', anchor=CENTER)
    table.heading('DOMAIN_NAME', text='Domain Name', anchor=CENTER)
    table.heading('PROBLEM_STATEMENT', text='Problem Statement', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)


    query = '''
    SELECT 
        PROJECT.PROJECT_ID, 
        PROJECT.PROJECT_TITLE,
        TEACHER.TEACHER_NAME, 
        PROJECT.DOMAIN_NAME,
        PROJECT.PROBLEM_STATEMENT
    FROM PROJECT
    LEFT JOIN TEACHER ON PROJECT.TEACHER_ID=TEACHER.TEACHER_ID
    WHERE
        PROJECT.TEACHER_ID = %s OR
        PROJECT.DOMAIN_NAME = %s
'''  



    try:
        mycursor.execute(query,[value if value else None for value in entry_values])
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def fil_mem_func():
    global search_window
    search_window = Toplevel()
    search_window.title("SEARCH FRIENDS")
    search_window.grab_set()
    search_window.resizable(False, False)

    domain_label = ttk.Label(search_window, text="INTEREST", font=('times new roman', 18, 'bold'))
    domain_label.grid(row=4, column=0, padx=15, pady=10, sticky=W)
    domain_entry = Entry(search_window, font=('times new roman', 10))
    domain_entry.grid(row=4, column=1, padx=15, pady=10)

    def search_button_callback():
        entry_values = [
            domain_entry.get(),
        ]
        find_mem_func(entry_values)

    search_button = ttk.Button(search_window, text="SEARCH", command=search_button_callback)
    search_button.grid(row=5, columnspan=2, padx=15, pady=10)

def find_mem_func(entry_values):
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('SRN','STUDENT_NAME','DEPT_NAME','STUDENT_MAIL','STUDENT_PHONE','CGPA'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('SRN', text='SRN', anchor=CENTER)
    table.heading('STUDENT_NAME', text='Student Name', anchor=CENTER)
    table.heading('DEPT_NAME', text='Department Name', anchor=CENTER)
    table.heading('STUDENT_MAIL', text='Student Mail', anchor=CENTER)
    table.heading('STUDENT_PHONE', text='Student Phone', anchor=CENTER)
    table.heading('CGPA', text='CGPA', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)


    query = '''
    SELECT
        STUDENT.SRN,
        STUDENT.STUDENT_NAME,
        DEPARTMENT.DEPT_NAME,
        STUDENT.STUDENT_MAIL,
        STUDENT.STUDENT_PHONE,
        STUDENT.CGPA
    FROM STUDENT
    LEFT JOIN DEPARTMENT ON DEPARTMENT.DEPT_ID = STUDENT.DEPT_ID
    LEFT JOIN INTERESTED_IN ON STUDENT.SRN = INTERESTED_IN.SRN
    WHERE
        INTERESTED_IN.DOMAIN_NAME = %s;

'''  

    try:
        mycursor.execute(query,[value if value else None for value in entry_values])
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def fil_paper_func():
    global search_window
    search_window = Toplevel()
    search_window.title("SEARCH PAPERS")
    search_window.grab_set()
    search_window.resizable(False, False)

    teacher_label = ttk.Label(search_window, text="TEACHER ID", font=('times new roman', 18, 'bold'))
    teacher_label.grid(row=0, column=0, padx=15, pady=10, sticky=W)
    teacher_entry = Entry(search_window, font=('times new roman', 10))
    teacher_entry.grid(row=0, column=1, padx=15, pady=10)

    def search_button_callback():
        entry_values=teacher_entry.get()
        find_paper_func(entry_values)

    search_button = ttk.Button(search_window, text="SEARCH", command=search_button_callback)
    search_button.grid(row=1, columnspan=2, padx=15, pady=10)

def find_paper_func(entry_values):
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('PAPER_TITLE','PUBLICATION_NAME','DATE_OF_PUBLICATION'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('PAPER_TITLE', text='PAPER', anchor=CENTER)
    table.heading('PUBLICATION_NAME', text='PUBLICATION', anchor=CENTER)
    table.heading('DATE_OF_PUBLICATION', text='PUBLISHED ON', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)


    query = '''
    SELECT
        PAPER.PAPER_TITLE,
        PAPER.PUBLICATION_NAME,
        PAPER.DATE_OF_PUBLICATION
    FROM PAPER
    WHERE
        PAPER.PUBLISHED_BY = %s;
'''  

    try:
        mycursor.execute(query,entry_values)
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def fil_teacher_by_interest_func():
    global search_window
    search_window = Toplevel()
    search_window.title("SEARCH TEACHERS BY INTEREST")
    search_window.grab_set()
    search_window.resizable(False, False)

    interest_label = ttk.Label(search_window, text="YOUR INTEREST", font=('times new roman', 18, 'bold'))
    interest_label.grid(row=4, column=0, padx=15, pady=10, sticky=W)
    interest_entry = Entry(search_window, font=('times new roman', 10))
    interest_entry.grid(row=4, column=1, padx=15, pady=10)

    def search_button_callback():
        entry_values = [
            interest_entry.get(),
        ]
        find_teacher_by_interest(entry_values)

    search_button = ttk.Button(search_window, text="SEARCH", command=search_button_callback)
    search_button.grid(row=5, columnspan=2, padx=15, pady=10)

def find_teacher_by_interest(entry_values):
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('TEACHER_ID', 'TEACHER_NAME','DEPT_NAME','TEACHER_MOBILE_NO', 'TEACHER_EMAIL', 'YEARS_OF_EXPERTISE', 'GRADUATION'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('TEACHER_ID', text='ID', anchor=CENTER)
    table.heading('TEACHER_NAME', text='NAME', anchor=CENTER)
    table.heading('DEPT_NAME', text='DEPT_NAME', anchor=CENTER)
    table.heading('TEACHER_MOBILE_NO', text='PHONE', anchor=CENTER)
    table.heading('TEACHER_EMAIL', text='MAIL', anchor=CENTER)
    table.heading('YEARS_OF_EXPERTISE', text='EXPERIENCE', anchor=CENTER)
    table.heading('GRADUATION', text='GRADUATION', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)


    query = '''
    SELECT DISTINCT 
        TEACHER.TEACHER_ID, 
        TEACHER.TEACHER_NAME, 
        DEPARTMENT.DEPT_NAME, 
        TEACHER.TEACHER_MOBILE_NO, 
        TEACHER.TEACHER_EMAIL,
        TEACHER.YEARS_OF_EXPERTISE, 
        TEACHER.GRADUATION
    FROM TEACHER
    LEFT JOIN HAS_EXPERTISE_IN ON HAS_EXPERTISE_IN.TEACHER_ID=TEACHER.TEACHER_ID
    LEFT JOIN DEPARTMENT ON TEACHER.DEPT_ID = DEPARTMENT.DEPT_ID
    WHERE
        HAS_EXPERTISE_IN.DOMAIN_NAME= %s
''' 

    try:
        mycursor.execute(query,[value if value else None for value in entry_values])
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def display_func():
    global table
    if table is not None:
        table.destroy()

    table = ttk.Treeview(detail_frame, columns=('TEACHER_ID', 'PAPERS','PROJECTS'), show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set, selectmode='browse')

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    table.heading('TEACHER_ID', text='TEACHER NAME', anchor=CENTER)
    table.heading('PAPERS', text='NO OF PAPERS', anchor=CENTER)
    table.heading('PROJECTS', text='NO OF PROJECTS', anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)
    query='''
    SELECT
        COALESCE(TEACHER.TEACHER_NAME, 'Total') AS TEACHER_NAME,
        COUNT(DISTINCT PAPER.PAPER_TITLE) AS NO_OF_PAPERS,
        COUNT(DISTINCT PROJECT.PROJECT_ID) AS NO_OF_PROJECTS
    FROM
        TEACHER
    LEFT JOIN
        PAPER ON TEACHER.TEACHER_ID = PAPER.PUBLISHED_BY
    LEFT JOIN
        PROJECT ON TEACHER.TEACHER_ID = PROJECT.TEACHER_ID
    GROUP BY
        TEACHER.TEACHER_NAME WITH ROLLUP;

'''

    try:
        mycursor.execute(query)
        show_data = mycursor.fetchall()
        table.delete(*table.get_children())
        for data in show_data:
            datalist = list(data)
            table.insert('', END, values=datalist)
    except Exception as e:
        print("Error executing query:", e)

def show_student_page():
    global student,ScrollbarX,ScrollbarY,detail_frame
    def clock():
        date=time.strftime('%d/%m/%y')
        currtime=time.strftime('%H:%M:%S')
        datetimeLabel.config(text=f'DATE:{date}\nTIME:{currtime}')
        datetimeLabel.after(1000,clock)

    student = ttkthemes.ThemedTk()
    student.get_themes()
    student.set_theme('itft1')
    student.title("STUDENT")
    student.geometry('1520x780+0+0')
    student.resizable(False, False)

    datetimeLabel=ttk.Label(student,text="",font=('times new roman',18,'bold'))
    datetimeLabel.place(x=5,y=5)
    clock()

    leftFrame = ttk.Frame(student)
    leftFrame.place(x=50, y=80, width=250, height=650)
    leftFrame_title=ttk.Label(leftFrame,text="STUDENT DETAIL",font=('times new roman', 18, 'bold'))
    leftFrame_title.grid(row=0,column=0,padx=17,pady=30)
    COMING=ttk.Label(leftFrame,text="COMING \nSOON!",anchor=CENTER,font=('times new roman', 18, 'bold'))
    COMING.grid(row=1,column=0,columnspan=2,padx=(20,0),pady=100)
    edit_details = ttk.Button(leftFrame, text='EDIT DETAILS', width=25, command=fil_teacher_func)
    edit_details.grid(row=2, column=0, pady=230)
    

    rightFrame = ttk.Frame(student)
    rightFrame.place(x=370, y=50, width=830, height=150)
    find_teacher = ttk.Button(rightFrame, text='FIND TEACHER', width=25, command=fil_teacher_func)
    find_teacher.grid(row=0, column=1, pady=16)
    find_team = ttk.Button(rightFrame, text='FIND TEAM', width=25,command=fil_team_func)
    find_team.grid(row=0, column=2, pady=16)
    find_project = ttk.Button(rightFrame, text='FIND PROJECT', width=25,command=fil_project_func)
    find_project.grid(row=0, column=3, pady=16)
    find_paper = ttk.Button(rightFrame, text='FIND PAPER', width=25,command=fil_paper_func)
    find_paper.grid(row=0, column=4, pady=16)
    teacher_by_interst = ttk.Button(rightFrame, text='FIND TEACHER BY INTEREST', width=25,command=fil_teacher_by_interest_func)
    teacher_by_interst.grid(row=1, column=1, pady=16)
    find_members = ttk.Button(rightFrame, text='FIND FRIENDS', width=25,command=fil_mem_func)
    find_members.grid(row=1, column=2, pady=16)
    display = ttk.Button(rightFrame, text='DISPLAY', width=25,command=display_func)
    display.grid(row=1, column=3, pady=16)
    exit_but = Button(rightFrame, text='EXIT', bg='red', width=25,command=exit_func)
    exit_but.grid(row=1, column=4, pady=16)

    middleFrame=ttk.Frame(student)
    middleFrame.place(x=1250,y=50,width=250,height=650)
    team_title=ttk.Label(middleFrame,text="TEAMS",anchor=CENTER,font=('times new roman', 18, 'bold'))
    team_title.grid(row=0,column=0,columnspan=2,padx=(20,0),pady=10)
    project_title=ttk.Label(middleFrame,text="PROJECTS",anchor=CENTER,font=('times new roman', 18, 'bold'))
    project_title.grid(row=1,column=0,columnspan=2,padx=(20,0))
    interest_title=ttk.Label(middleFrame,text="INTERESTS",anchor=CENTER,font=('times new roman', 18, 'bold'))
    interest_title.grid(row=2,column=0,columnspan=2,padx=(20,0),pady=10)
    COMING=ttk.Label(middleFrame,text="COMING \nSOON!",anchor=CENTER,font=('times new roman', 18, 'bold'))
    COMING.grid(row=3,column=0,columnspan=2,padx=(20,0),pady=100)
    add_interests = ttk.Button(middleFrame, text='ADD INTERESTS', width=25)
    add_interests.grid(row=4, column=0,columnspan=2, padx=20,pady=180)

    detail_frame=ttk.Frame(student)
    detail_frame.place(x=370,y=250,width=830,height=500)

    ScrollbarX = Scrollbar(detail_frame, orient=HORIZONTAL)
    ScrollbarY = Scrollbar(detail_frame, orient=VERTICAL)

    student.mainloop()
