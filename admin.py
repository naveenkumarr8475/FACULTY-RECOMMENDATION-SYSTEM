from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import ttkthemes
from tkinter import ttk
import pymysql

con=pymysql.connect(host="localhost",user="ADMIN",password="1726")
mycursor=con.cursor()
query='use faculty_recommendation_system'
mycursor.execute(query)

selected_table=''
column_names=[]
table=None

def set_selected_table(table_name):
    global selected_table,column_names
    selected_table = table_name
    query = f"SHOW COLUMNS FROM {selected_table}"
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    column_names = [column[0] for column in fetched_data]
    update_table_columns(selected_table)

def clear_entries(entries):
    for entry in entries:
        entry.delete(0, 'end')

def add_func():
    global column_names
    
    if selected_table:
        add_window=Toplevel()
        add_window.title("ADD DETAILS")
        add_window.grab_set()
        add_window.resizable(False,False)
        row_no=0

        entry_values = []
        entry_widgets = []

        for column_name in column_names:
            label = ttk.Label(add_window, text=column_name, font=('times new roman', 18, 'bold'))
            label.grid(row=row_no,column=0,padx=15,pady=10,sticky=W)
            entry = ttk.Entry(add_window, font=('times new roman', 10))
            entry.grid(row=row_no,column=1,padx=15,pady=10)
            entry_values.append(entry)
            entry_widgets.append(entry)
            row_no=row_no+1

        submit_button = ttk.Button(add_window, text="SUBMIT", command=lambda: add_details([e.get() for e in entry_values], entry_widgets))
        submit_button.grid(row=row_no, columnspan=2, padx=15, pady=10)

    else:
        messagebox.showerror('Error','PLEASE SELECT A TABLE')

def add_details(entry_values, entry_widgets):
    global selected_table, column_names
    try:
        values = tuple(entry_values)
        query = f"INSERT INTO {selected_table} VALUES ({', '.join(['%s']*len(column_names))})"
        mycursor.execute(query, [value if value else None for value in entry_values])

        if selected_table == 'MEMBER':
            team_id_index = column_names.index('TEAM_ID')
            team_id = entry_values[team_id_index]
            mycursor.callproc('CHECK_MAX_MEMBERS_PROC', (team_id,))
        
        con.commit()
        print(query)
        clear_entries(entry_widgets)
        messagebox.showinfo("Success", "Successfully Entered")
        update_table_columns(selected_table)
    except Exception as e:
        con.rollback()
        messagebox.showerror('Error', f'Error during insertion: {str(e)}')

def search_func():
    global column_names,search_window
    if selected_table:
        search_window=Toplevel()
        search_window.title("SEARCH")
        search_window.grab_set()
        search_window.resizable(False,False)
        entry_values = []
        entry_widgets = []
        row_no=0

        for column_name in column_names:
            label = ttk.Label(search_window, text=column_name, font=('times new roman', 18, 'bold'))
            label.grid(row=row_no,column=0,padx=15,pady=10,sticky=W)
            entry = ttk.Entry(search_window, font=('times new roman', 10))
            entry.grid(row=row_no,column=1,padx=15,pady=10)
            entry_values.append(entry)
            entry_widgets.append(entry)
            row_no=row_no+1

        search_button = ttk.Button(search_window, text="SEARCH", command=lambda: search([e.get() for e in entry_values], entry_widgets))
        search_button.grid(row=row_no, columnspan=2, padx=15, pady=10)

    else:
        messagebox.showerror('Error','PLEASE SELECT A TABLE')

def search(entry_values, entry_widgets):
    global table, selected_table, column_names
    try:
        where_conditions = f" OR ".join(f"{column} = %s"  for column in column_names)
        query = f"SELECT * FROM {selected_table} WHERE {where_conditions}"
        
        mycursor.execute(query, [value if value else None for value in entry_values])
        result = mycursor.fetchall()
        print(query)
        
        if result:
            table.delete(*table.get_children())
            for data in result:
                datalist = list(data)
                table.insert('', END, values=datalist)
            messagebox.showinfo("Success", "Successful Search")
        else:
            messagebox.showinfo("No Matches", "No Matches Found")
        
        clear_entries(entry_widgets)
        search_window.destroy()

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Error during search: {str(e)}')
    except Exception as e:
        messagebox.showerror('Error', f'An unexpected error occurred: {str(e)}')

def del_func():
    global selected_table
    try:
        indexing = table.focus()
        content = table.item(indexing)
        content_id = content['values'][0]

        if selected_table=='DOMAIN':
            query = f"DELETE FROM {selected_table} WHERE {column_names[0]} = %s"
            mycursor.execute(query, (content_id,))
            con.commit()
            print(query)
            messagebox.showinfo('Deleted', 'Successfully Deleted')
            update_table_columns(selected_table)
        else:
            content_id1 = content['values'][1]
            query = f"DELETE FROM {selected_table} WHERE {column_names[0]} = %s AND {column_names[1]} = %s"
            mycursor.execute(query, (content_id, content_id1,))
            con.commit()
            print(query)
            messagebox.showinfo('Deleted', 'Successfully Deleted')
            update_table_columns(selected_table)
    except Exception as e:
        messagebox.showerror('Error', f'Error during deletion: {str(e)}')

def update_details(entry_values, entry_widgets):
    global selected_table, column_names
    try:
        primary_key_value = entry_values[0].get()
        values = tuple(entry.get() for entry in entry_values[0:])
        set_clause = f', '.join(f'{column} = %s' for column in column_names[0:])
        query = f"UPDATE {selected_table} SET {set_clause} WHERE {column_names[0]} = %s"
        mycursor.execute(query,values + (primary_key_value,))
        if selected_table == 'MEMBER':
            team_id_index = column_names.index('TEAM_ID')
            team_id = entry_values[team_id_index].get()
            mycursor.callproc('CHECK_MAX_MEMBERS_PROC', (team_id,))
            con.commit()
            print(query)
        

        con.commit()
        print(query)
        clear_entries(entry_widgets)
        messagebox.showinfo("Success", "Successfully updated")
        update_table_columns(selected_table)
        update_window.destroy()
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Error during update: {str(e)}')
    except Exception as e:
        messagebox.showerror('Error', f'An unexpected error occurred: {str(e)}')

def update_func():
    global selected_table, column_names,update_window
    indexing = table.focus()
    content = table.item(indexing)
    listdata = content['values']

    if not listdata:
        messagebox.showerror('Error', 'PLEASE SELECT A ENTRY TO UPDATE')
        return

    update_window = Toplevel()
    update_window.title("UPDATE DETAILS")
    update_window.grab_set()
    update_window.resizable(False, False)

    entry_values = []
    entry_widgets = []

    for row_no, column_name in enumerate(column_names):
        label = ttk.Label(update_window, text=column_name, font=('times new roman', 18, 'bold'))
        label.grid(row=row_no, column=0, padx=15, pady=10, sticky=W)

        entry = ttk.Entry(update_window, font=('times new roman', 10))
        entry.insert(0, listdata[row_no])
        entry.grid(row=row_no, column=1, padx=15, pady=10)

        entry_values.append(entry)
        entry_widgets.append(entry)

    update_button = ttk.Button(update_window, text="UPDATE", command=lambda: update_details(entry_values, entry_widgets))
    update_button.grid(row=row_no + 1, columnspan=2, padx=15, pady=10)

def exit_func():
    admin.destroy()

def update_table_columns(selected_table):
    global middleFrame, table, column_names

    if table is not None:
        table.destroy()

    table = ttk.Treeview(middleFrame, columns=column_names, show='headings', xscrollcommand=ScrollbarX.set, yscrollcommand=ScrollbarY.set)

    ScrollbarX.config(command=table.xview)
    ScrollbarY.config(command=table.yview)

    for column_name in column_names:
        table.heading(column_name, text=column_name,anchor=CENTER)

    ScrollbarX.pack(side=BOTTOM, fill=X)
    ScrollbarY.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=1)

    query=f'select * from {selected_table}'
    mycursor.execute(query)
    show_data=mycursor.fetchall()
    for data in show_data:
        datalist=list(data)
        table.insert('',END,values=datalist)
    
def show_admin_page():
    global middleFrame,ScrollbarX,ScrollbarY,admin
    def clock():
        date = time.strftime('%d/%m/%y')
        currtime = time.strftime('%H:%M:%S')
        datetimeLabel.config(text=f'DATE:{date}\nTIME:{currtime}')
        datetimeLabel.after(1000, clock)

    admin = ttkthemes.ThemedTk()
    admin.get_themes()
    admin.set_theme('itft1')
    admin.title("ADMIN")
    admin.geometry('1520x780+0+0')
    admin.resizable(False, False)

    datetimeLabel = ttk.Label(admin, text="", font=('times new roman', 18, 'bold'))
    datetimeLabel.place(x=5, y=5)
    clock()

    leftFrame = ttk.Frame(admin)
    leftFrame.place(x=50, y=80, width=200, height=670)

    pes_logo = Image.open('pes.png')
    pes_logo = pes_logo.resize((150, 100), Image.LANCZOS)
    pes_logo = ImageTk.PhotoImage(pes_logo)
    pes_label = ttk.Label(leftFrame, image=pes_logo)
    pes_label.grid(row=0, column=0, pady=15)

    Dept = ttk.Button(leftFrame, text='DEPARTMENT', width=25, command=lambda: set_selected_table('DEPARTMENT'))
    Dept.grid(row=1, column=0, pady=8)  # Decreased pady to 5
    Domain = ttk.Button(leftFrame, text='DOMAIN', width=25, command=lambda: set_selected_table('DOMAIN'))
    Domain.grid(row=2, column=0, pady=8)  # Decreased pady to 5
    Teacher = ttk.Button(leftFrame, text='TEACHER', width=25, command=lambda: set_selected_table('TEACHER'))
    Teacher.grid(row=3, column=0, pady=8)  # Decreased pady to 5
    Project = ttk.Button(leftFrame, text='PROJECT', width=25, command=lambda: set_selected_table('PROJECT'))
    Project.grid(row=4, column=0, pady=8)  # Decreased pady to 5
    Paper = ttk.Button(leftFrame, text='PAPER', width=25, command=lambda: set_selected_table('PAPER'))
    Paper.grid(row=5, column=0, pady=8)  # Decreased pady to 5
    Student = ttk.Button(leftFrame, text='STUDENT', width=25, command=lambda: set_selected_table('STUDENT'))
    Student.grid(row=7, column=0, pady=8)  # Decreased pady to 5
    Team = ttk.Button(leftFrame, text='TEAM', width=25, command=lambda: set_selected_table('TEAM'))
    Team.grid(row=8, column=0, pady=8)
    HasExpertiseIn = ttk.Button(leftFrame, text='HAS_EXPERTISE_IN', width=25, command=lambda: set_selected_table('HAS_EXPERTISE_IN'))
    HasExpertiseIn.grid(row=11, column=0, pady=8)  
    InterestedIn = ttk.Button(leftFrame, text='INTERESTED_IN', width=25, command=lambda: set_selected_table('INTERESTED_IN'))
    InterestedIn.grid(row=12, column=0, pady=8)  # Decreased pady to 5
    Member = ttk.Button(leftFrame, text='MEMBER', width=25, command=lambda: set_selected_table('MEMBER'))
    Member.grid(row=13, column=0, pady=8)  # Decreased pady to 5
    TeamProjectRelation = ttk.Button(leftFrame, text='TEAM_PROJECT_RELATION', width=25, command=lambda: set_selected_table('TEAM_PROJECT_RELATION'))
    TeamProjectRelation.grid(row=14, column=0, pady=8)  # Decreased pady to 5

    rightFrame = ttk.Frame(admin)
    rightFrame.place(x=300, y=80, width=1200, height=75)

    add = ttk.Button(rightFrame, text='ADD DETAILS', width=25,command=add_func)
    add.grid(row=0, column=1, pady=16,padx=20)
    delete = ttk.Button(rightFrame, text='DELETE', width=25,command=del_func)
    delete.grid(row=0, column=2, pady=16,padx=20)
    update = ttk.Button(rightFrame, text='UPDATE', width=25,command=update_func)
    update.grid(row=0, column=3, pady=16,padx=20)
    search = ttk.Button(rightFrame, text='SEARCH', width=25,command=search_func)
    search.grid(row=0, column=4, pady=16,padx=20)
    exit_but = Button(rightFrame, text='EXIT', bg='red', width=25,command=exit_func)
    exit_but.grid(row=0, column=5, pady=16,padx=20)

    middleFrame = ttk.Frame(admin)
    middleFrame.place(x=300, y=180, width=1200, height=570)

    ScrollbarX = Scrollbar(middleFrame, orient=HORIZONTAL)
    ScrollbarY = Scrollbar(middleFrame, orient=VERTICAL)

    admin.mainloop()

