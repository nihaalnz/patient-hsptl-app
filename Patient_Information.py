# Importing modules
from tkinter import *
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image, ImageGrab
from tkcalendar import Calendar
import babel.numbers
import mysql.connector as mysql
from tkinter import ttk
from ttkthemes import themed_tk as tktheme
import webbrowser
import pygetwindow as gw
import win32gui
import os
import Pmw


# Main Window
#root = Tk()

# Making the main themed window
root = tktheme.ThemedTk()
root.focus_force()
root.resizable(False,False)
Pmw.initialise(root)
root.get_themes()
root.set_theme('vista')
root.title('Patient Information')
root.geometry('+110+70')
root.iconbitmap('icon.ico')
font_text = Font(family='helvetica', size='11')
font_button = Font(size='10')

# Assigning empty string for debug
path = ""

# Defining options for Dropdown
gen = ['Male', 'Female']
bl_gr = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
cov = ['Yes', 'No', 'N/A']

# Function to enter value into database
def database():

    try:
        # Defining Variables for db
        nme = name.get()
        p_h = ph.get()
        eid = e_id.get()
        ema_id = em_id.get()
        nat = nation.get()
        emer = emerg.get()
        gend = g.get()
        bloo = b.get()
        covi = co.get()
        dat = cal.selection_get()

        # Inserting into db
        if nme == "" or p_h == "" or eid == "" or ema_id == "" or nat == "" or emer == "" or gend == "" or bloo == "" or covi == "" or dat == "":
            messagebox.showinfo('Fill all', 'All fields are necessary',parent=root)

        else:
            # Establishing connection
            con = mysql.connect(host='', user='',
                                password='', database='')

            # Making SQL command
            sql_command = "INSERT into patient_infos (`Full Name`,`Phone Number`,`Emirates ID`,`Email Address`,`Gender`,`Date of Birth`,`Nationality`,`Blood Group`,`COVID result`,`Emergency Number`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            values = (nme, p_h, eid, ema_id, gend, str(
                dat), nat, str(bloo), str(covi), emer)
            # Defining cursor
            c = con.cursor()
            # Executing and saving SQL command
            c.execute(sql_command, values)
            c.execute('commit')
            # Closing the connection
            con.close()
            # Success message
            messagebox.showinfo(
                'Success', 'All values have been entered to the database',parent=root)
            # Reseting all the boxes
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e5.delete(0, END)
            e6.delete(0, END)

    except:
        messagebox.showinfo(
            'Fill all', 'Make sure to fil all fields including date',parent=root)

# Function to get access to admin panel
def manage(): 
    global q_mark_new

    # Defining Login window
    admin = Toplevel(root)
    admin.resizable(False,False)
    admin.title('Login')
    admin.focus_force()
    admin.geometry('470x522+550+70')
    admin.iconbitmap('Image/icn_5.ico')

    # Assigning username and password
    username = 'admin'
    password = '12345'

    def login(event=None):
        global q_mark_new

        # If user is authentic
        if e1.get() == username and e2.get() == password:

            # Login successfull
            messagebox.showinfo('Success', 'Succesfully logged in',parent=admin)
            admin.destroy()

            # Creating a new window
            update = Toplevel(root)
            update.resizable(False,False)
            update.focus_force()
            update.title('Administration')
            update.geometry('+550+70')
            update.iconbitmap('Image/icn_5.ico')

            # Defining screen-items and placing them
            e_i_d = ttk.Entry(update)
            e_i_d.focus_force()
            e_i_d.grid(row=1, column=1, padx=5, pady=5, ipady=5)
            l1 = ttk.Label(
                update, text='Enter ID of patient to be edited', font=font_text)
            l_head = Label(update, text='Administration Panel',
                           font=Font(size='20'))
            l1.grid(row=1, column=0, padx=5, pady=5)
            l_head.grid(row=0, columnspan=2, padx=10, sticky=E+W, pady=10)

            def updates(event=None):
                global q_mark_new
                # Assigning a variable for .get()
                values = e_i_d.get()

                # Defining error actions
                if values == "":
                    messagebox.showinfo(
                        'No value!', 'Please enter data in the box',parent=update)

                else:
                    # Establishing connection
                    con = mysql.connect(host='', user='',
                                        password='', database='')
                    # Making SQL command
                    sql_command = "SELECT * from patient_infos where `Sl.no.` = %s ;"
                    c = con.cursor()
                    # Executing and saving SQL command
                    c.execute(sql_command, (values,))
                    records = c.fetchall()

                    # Describing empty actions
                    if records == []:
                        messagebox.showinfo('Does not exist!',
                                            'Sorry such patient does not exist',parent=update)

                    else:
                        manage = Toplevel(update)
                        manage.resizable(False,False)
                        manage.title('Manage')
                        manage.focus_force()
                        manage.geometry('+550+290')
                        manage.iconbitmap('Image/icn_4.ico')

                        def edit():
                            if e10.get()=='' or e20.get()=='' or e30.get()=='' or e40.get()=='' or g.get(
                            )=='' or e_dt.get()=='' or e50.get()=='' or b.get()=='' or co.get()=='' or e60.get()=='' or e_i_d.get()=='':                          # Establishing connection
                                
                                messagebox.showerror('Fill all blanks','Make sure to fill all the data and leave nothing empty',parent=manage)
                            
                            else:
                                con = mysql.connect(host='', user='',
                                                    password='', database='')
                                # Making SQL command
                                sql_command = "UPDATE patient_infos set `Full Name`=%s ,`Phone Number`=%s,`Emirates ID`=%s,`Email Address`=%s,`Gender`=%s,`Date of Birth`=%s,`Nationality`=%s,`Blood Group`=%s,`COVID result`=%s,`Emergency Number`=%s where `Sl.no.` = %s ;"
                                values = e10.get(), e20.get(), e30.get(), e40.get(), g.get(
                                ), e_dt.get(), e50.get(), b.get(), co.get(), e60.get(), e_i_d.get()
                                c = con.cursor()
                                # Executing and saving SQL command
                                c.execute(sql_command, values)
                                c.execute('commit')

                                # Display sucess message
                                messagebox.showinfo(
                                    'Done', 'The data has been successfully updated.',parent=manage)

                                # Clearing entry box
                                e_i_d.delete(0, END)

                                # Closing the window automatically
                                con.close()
                                manage.destroy()

                        # Defining Labels
                        l_head = Label(manage, text='Edit',
                                       font=Font(size='20'))
                        l1 = ttk.Label(manage, text='Name', font=font_text)
                        l2 = ttk.Label(
                            manage, text='Phone Number', font=font_text)
                        l3 = ttk.Label(
                            manage, text='Emirates ID', font=font_text)
                        l4 = ttk.Label(
                            manage, text='Email Address', font=font_text)
                        l5 = ttk.Label(
                            manage, text='Nationality', font=font_text)
                        l6 = ttk.Label(
                            manage, text='Emergency Contact Number', font=font_text)
                        l7 = ttk.Label(manage, text='Gender', font=font_text)
                        l8 = ttk.Label(
                            manage, text='Blood Group', font=font_text)
                        l9 = ttk.Label(
                            manage, text='Test for COVID-19', font=font_text)
                        l10 = ttk.Label(manage, text='DOB', font=font_text)
                        l_wa = Label(
                            manage, text='NOTE: Date must be in yyyy-mm-dd format always', font=font_text, fg='red')

                        # Defining Entry boxes and button
                        e10 = ttk.Entry(manage)
                        e20 = ttk.Entry(manage)
                        e30 = ttk.Entry(manage)
                        e40 = ttk.Entry(manage)
                        e50 = ttk.Entry(manage)
                        e60 = ttk.Entry(manage)
                        e_dt = ttk.Entry(manage)
                        b_cls = ttk.Button(manage, text='Close',
                                           command=manage.destroy)
                        b_db = ttk.Button(
                            manage, text='Update Data', command=edit)

                        main = records[0]

                        # Defining Dropdowns
                        g = StringVar()
                        g.set(main[5])
                        opt_g = OptionMenu(manage, g, *gen)

                        b = StringVar()
                        b.set(main[8])
                        opt_blo = OptionMenu(manage, b, *bl_gr)

                        co = StringVar()
                        co.set(main[9])
                        opt_cov = OptionMenu(manage, co, *cov)

                        # Placing entry boxes on screen
                        e10.grid(row=1, column=1, pady=5, ipady=5, padx=5)
                        e20.grid(row=1, column=4, pady=5, ipady=5, padx=5)
                        e30.grid(row=2, column=1, pady=5, ipady=5, padx=5)
                        e40.grid(row=2, column=4, pady=5, ipady=5, padx=5)
                        e50.grid(row=3, column=1, pady=6, ipady=5, padx=5)
                        e60.grid(row=3, column=4, pady=5, ipady=5, padx=5)

                        # Inserting results on to boxes
                        for record in records:
                            e10.insert(0, record[1])
                            e20.insert(0, record[2])
                            e30.insert(0, record[3])
                            e40.insert(0, record[4])
                            e50.insert(0, record[7])
                            e60.insert(0, record[10])
                            e_dt.insert(0, record[6])
                        # Closing the connection
                        con.close()

                        # Placing labels and dropdowns on screen
                        l_head.grid(row=0, columnspan=5, pady=10, padx=5)
                        l1.grid(row=1, column=0, pady=5, ipady=5, padx=5)
                        l2.grid(row=1, column=3, pady=5, ipady=5, padx=5)
                        l3.grid(row=2, column=0, pady=5, ipady=5, padx=5)
                        l4.grid(row=2, column=3, pady=5, ipady=5, padx=5)
                        l5.grid(row=3, column=0, pady=5, ipady=5, padx=5)
                        l6.grid(row=3, column=3, pady=5, ipady=5, padx=5)
                        l7.grid(row=4, column=0, pady=5, ipady=5, padx=5)
                        l8.grid(row=4, column=3, pady=5, ipady=5, padx=5)
                        l9.grid(row=5, column=0, pady=5, ipady=5, padx=5)
                        l10.grid(row=5, column=3, pady=5, ipady=5, padx=5)

                        opt_g.grid(row=4, column=1, pady=5, ipadx=10, padx=5)
                        opt_blo.grid(row=4, column=4, pady=5, ipadx=10, padx=5)
                        opt_cov.grid(row=5, column=1, pady=5, ipadx=10, padx=5)
                        e_dt.grid(row=5, column=4, pady=5, ipady=5, padx=5)
                        b_db.grid(row=7, columnspan=6, pady=(
                            5, 0), ipadx=10, sticky=E+W)
                        b_cls.grid(row=8, columnspan=6, pady=(
                            5, 0), ipadx=10, sticky=E+W)
                        l_wa.grid(row=6, columnspan=5, pady=5,
                                  ipady=5, padx=5, sticky=E+W)

                        # Making 13 ? icons
                        q_mark_1 = Label(manage, image=q_mark_new)
                        q_mark_1.grid(row=1, column=2, padx=(0, 10))
                        q_mark_2 = Label(manage, image=q_mark_new)
                        q_mark_2.grid(row=2, column=2, padx=(0, 10))
                        q_mark_3 = Label(manage, image=q_mark_new)
                        q_mark_3.grid(row=3, column=2, padx=(0, 10))
                        q_mark_4 = Label(manage, image=q_mark_new)
                        q_mark_4.grid(row=4, column=2, padx=(0, 10))
                        q_mark_5 = Label(manage, image=q_mark_new)
                        q_mark_5.grid(row=5, column=2, padx=(0, 10))
                        q_mark_6 = Label(manage, image=q_mark_new)
                        q_mark_6.grid(row=1, column=5, padx=(0, 10),sticky=E)
                        q_mark_7 = Label(manage, image=q_mark_new)
                        q_mark_7.grid(row=2, column=5, padx=(0, 10),sticky=E)
                        q_mark_8 = Label(manage, image=q_mark_new)
                        q_mark_8.grid(row=3, column=5, padx=(0, 10),sticky=E)
                        q_mark_9 = Label(manage, image=q_mark_new)
                        q_mark_9.grid(row=4, column=5, padx=(0, 10))
                        q_mark_10 = Label(manage, image=q_mark_new)
                        q_mark_10.grid(row=5, column=5, padx=(0, 10),sticky=E)

                        # Creating a tooltip for each ? icon
                        nametooltip_1 = Pmw.Balloon(root)
                        nametooltip_1.bind(q_mark_1, 'Name:\nEnter a valid full name')
                        nametooltip_2 = Pmw.Balloon(root)
                        nametooltip_2.bind(q_mark_2, 'Emirates ID:\nEnter Emirates ID less than 16 digits')
                        nametooltip_3 = Pmw.Balloon(root)
                        nametooltip_3.bind(q_mark_3, 'Nationality:\nEnter your nationality')
                        nametooltip_4 = Pmw.Balloon(root)
                        nametooltip_4.bind(q_mark_4, 'Gender:\nChoose Gender from the dropdown box')
                        nametooltip_5 = Pmw.Balloon(root)
                        nametooltip_5.bind(q_mark_5, 'COVID result:\nChoose a suitable option\nYes - If tested positive\nNo - If tested negative\nN/A - If hadnt done a test yet')
                        nametooltip_6 = Pmw.Balloon(root)
                        nametooltip_6.bind(q_mark_6, 'Phone Number:\nEnter a phone number less than 11 digits')
                        nametooltip_7 = Pmw.Balloon(root)
                        nametooltip_7.bind(q_mark_7, 'Email Address:\nEnter a valid email address')
                        nametooltip_8 = Pmw.Balloon(root)
                        nametooltip_8.bind(q_mark_8, 'Emergency Number:\nEnter a number to be contacted in cases of emergency')
                        nametooltip_9 = Pmw.Balloon(root)
                        nametooltip_9.bind(q_mark_9, 'Blood Group:\nChoose your blood group from the dropdown box')
                        nametooltip_10 = Pmw.Balloon(root)
                        nametooltip_10.bind(q_mark_10, 'Date of Birth:\nPick Date of Birth from the box ')

            def sp_patient():
                global q_mark_new

                # Creating window
                sp_pat = Toplevel(update)
                sp_pat.resizable(False,False)
                sp_pat.title('Choose Patient')
                sp_pat.focus_force()
                sp_pat.geometry('+550+390')
                sp_pat.iconbitmap('Image/icn_2.ico')

                def search(event=None):
                    # Assigning variable to .get()
                    a = drops.get()

                    if a == 'Sl.no.' or a == 'Emirates ID' or a == 'Email Address' or a == 'Gender' or a == 'Date of Birth' or a == 'Blood Group' or a == 'COVID result':
                        
                        if e_1.get() == '':
                            messagebox.showerror('Fill in the blank','Make sure to fill the blank',parent=sp_pat)
                        
                        else:
                            # Establishing connection
                            con = mysql.connect(host='', user='',
                                                password='', database='')
                            # Making SQL command
                            sql_command = "SELECT * FROM patient_infos where `{}` = %s"
                            sql_command = sql_command.format(a)
                            values = (e_1.get(),)
                            # Executing and saving SQL command
                            c = con.cursor()
                            c.execute(sql_command, values)
                            records = c.fetchall()

                            # Declaring null actions
                            if records == []:
                                messagebox.showinfo('Does not exist!',
                                                    'Sorry such patient does not exist',parent=sp_pat)
                                e_1.delete(0,END)

                            else:
                                # Creating window
                                result_win = Toplevel(sp_pat)
                                result_win.resizable(False,False)
                                result_win.title('Search result')
                                result_win.geometry('+110+350')
                                result_win.focus_force()
                                result_win.iconbitmap('Image/icn_3.ico')

                                index = 0
                                for index, x in enumerate(records):
                                    num = 0
                                    for y in x:
                                        lookup_label = Label(result_win, text=y)
                                        lookup_label.grid(row=index+1, column=num)
                                        num += 1
                                # Closing connection
                                con.close()

                                # Creating column header and exit button
                                l_1 = Label(result_win, text='ID', font=font_text)
                                l_2 = Label(
                                    result_win, text='Full Name', font=font_text)
                                l_3 = Label(
                                    result_win, text='Phone no.', font=font_text)
                                l_4 = Label(
                                    result_win, text='Emirates ID', font=font_text)
                                l_5 = Label(
                                    result_win, text='Email addr.', font=font_text)
                                l_6 = Label(result_win, text='Gender',
                                            font=font_text)
                                l_7 = Label(result_win, text='DOB', font=font_text)
                                l_8 = Label(
                                    result_win, text='Nationality', font=font_text)
                                l_9 = Label(
                                    result_win, text='Blood group', font=font_text)
                                l_10 = Label(
                                    result_win, text='COVID test', font=font_text)
                                l_11 = Label(result_win, text='Emergency no.',
                                            font=font_text)
                                btn_ext = Button(result_win, text='Exit', font=font_text,
                                                command=result_win.destroy, borderwidth=2, fg='#eb4d4b')

                                # Placing it in screen
                                l_1.grid(row=0, column=0, padx=20)
                                l_2.grid(row=0, column=1, padx=20)
                                l_3.grid(row=0, column=2, padx=20)
                                l_4.grid(row=0, column=3, padx=20)
                                l_5.grid(row=0, column=4, padx=20)
                                l_6.grid(row=0, column=5, padx=20)
                                l_7.grid(row=0, column=6, padx=20)
                                l_8.grid(row=0, column=7, padx=20)
                                l_9.grid(row=0, column=8, padx=20)
                                l_10.grid(row=0, column=9, padx=20)
                                l_11.grid(row=0, column=10, padx=20)
                                btn_ext.grid(row=index+2, columnspan=11,
                                            ipadx=240, sticky=E+W)
                                e_1.delete(0,END)

                    elif a == 'Full Name' or a == 'Phone Number' or a == 'Nationality' or a == 'Emergency Number':

                        if e_1.get() == '':
                            messagebox.showerror('Fill in the blank','Make sure to fill the blank',parent=sp_pat)
                        
                        else:
                            
                            # Establishing connection
                            con = mysql.connect(host='', user='',
                                                password='', database='')
                            # Making SQL command
                            sql_command = "SELECT * FROM patient_infos where `{}` regexp %s;"
                            sql_command = sql_command.format(a)
                            # Executing and saving SQL command
                            c = con.cursor()
                            c.execute(sql_command, (e_1.get(),))
                            records = c.fetchall()
                            

                            # Declaring null actions
                            if records == []:
                                messagebox.showinfo('Does not exist!',
                                                    'Sorry such patient does not exist',parent=sp_pat)
                                e_1.delete(0,END)
                            
                            else:
                                # Creating window
                                result_win = Toplevel(sp_pat)
                                result_win.resizable(False,False)
                                result_win.title('Search result')
                                result_win.geometry('+110+350')
                                result_win.focus_force()
                                result_win.iconbitmap('Image/icn_3.ico')

                                # Looping and placing in systematic order
                                index = 0
                                for index, x in enumerate(records):
                                    num = 0
                                    for y in x:
                                        lookup_label = Label(result_win, text=y)
                                        lookup_label.grid(row=index+1, column=num)
                                        num += 1
                                # Closing connection
                                con.close()

                                # Creating column headers and exit button
                                l_1 = Label(result_win, text='ID', font=font_text)
                                l_2 = Label(
                                    result_win, text='Full Name', font=font_text)
                                l_3 = Label(
                                    result_win, text='Phone no.', font=font_text)
                                l_4 = Label(
                                    result_win, text='Emirates ID', font=font_text)
                                l_5 = Label(
                                    result_win, text='Email addr.', font=font_text)
                                l_6 = Label(result_win, text='Gender',
                                            font=font_text)
                                l_7 = Label(result_win, text='DOB', font=font_text)
                                l_8 = Label(
                                    result_win, text='Nationality', font=font_text)
                                l_9 = Label(
                                    result_win, text='Blood group', font=font_text)
                                l_10 = Label(
                                    result_win, text='COVID test', font=font_text)
                                l_11 = Label(result_win, text='Emergency no.',
                                            font=font_text)
                                btn_ext = Button(result_win, text='Exit', font=font_text,
                                                command=result_win.destroy, borderwidth=2, fg='#eb4d4b')

                                # Placing it on screen
                                l_1.grid(row=0, column=0, padx=20)
                                l_2.grid(row=0, column=1, padx=20)
                                l_3.grid(row=0, column=2, padx=20)
                                l_4.grid(row=0, column=3, padx=20)
                                l_5.grid(row=0, column=4, padx=20)
                                l_6.grid(row=0, column=5, padx=20)
                                l_7.grid(row=0, column=6, padx=20)
                                l_8.grid(row=0, column=7, padx=20)
                                l_9.grid(row=0, column=8, padx=20)
                                l_10.grid(row=0, column=9, padx=20)
                                l_11.grid(row=0, column=10, padx=20)
                                btn_ext.grid(row=index+2, columnspan=11,
                                            ipadx=240, sticky=E+W)
                                e_1.delete(0,END)

                    else:
                        # Error message
                        messagebox.showinfo(
                            'No choice given', 'Please choose a valid option to search by...',parent=sp_pat)

                # Defining dropdown and entry box
                drops = ttk.Combobox(sp_pat, value=['Search by...', 'Sl.no.', 'Full Name', 'Phone Number', 'Emirates ID', 'Email Address',
                                                    'Gender', 'Date of Birth', 'Nationality', 'Blood Group', 'COVID result', 'Emergency Number'], state='readonly')
                drops.current(0)
                e_1 = Entry(sp_pat)
                e_1.focus_force()

                # Defining Labels and search button
                l_sch = Label(sp_pat, text='Search', font=Font(size='20'))
                l_id = Label(sp_pat, text='Enter', font=font_text)
                bt_db = ttk.Button(sp_pat, text='Search', command=search)

                # Placing it in screen
                drops.grid(row=1, columnspan=3, ipady=5, padx=5, pady=10)
                e_1.grid(row=2, column=1, ipady=5, padx=5, pady=5)
                l_id.grid(row=2, column=0, padx=5, pady=5)
                bt_db.grid(row=3, columnspan=3, pady=(10,0), sticky=E+W)
                l_sch.grid(row=0, columnspan=2, sticky=E+W, padx=100, pady=10)
                e_1.bind('<Return>',search)

                # Making 13 ? icons
                q_mark_1 = Label(sp_pat, image=q_mark_new)
                q_mark_2 = Label(sp_pat, image=q_mark_new)
                q_mark_1.grid(row=1, column=2, padx=(0, 10))
                q_mark_2.grid(row=2, column=2, padx=(0, 10))

                nametooltip_1 = Pmw.Balloon(root)
                nametooltip_2 = Pmw.Balloon(root)
                nametooltip_1.bind(q_mark_1, 'Search by:\nChoose an option to search by..')
                nametooltip_2.bind(q_mark_2, 'Enter:\nEnter the corresponding information')

            def all_patients():

                # Making a new window
                all_pat = Toplevel(update)
                all_pat.resizable(False,False)
                all_pat.focus_force()
                all_pat.iconbitmap('Image/icn_3.ico')
                all_pat.geometry('+110+70')

                # setup treeview
                columns = (('ID', 50), ("Full Name", 150), ("Ph No.", 100), ("Emirates ID", 100), ("Email Addr.", 180),
                           ("Gender", 70), ("DOB", 100), ('Nationality', 80), ('B Grp', 60), ("COVID Test", 60), ("Emergency No.", 100))
                tree = ttk.Treeview(all_pat, height=20, columns=[
                                    x[0] for x in columns], show='headings')
                tree.grid(row=0, column=0, sticky='news')

                # setup columns attributes
                for col, width in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=width, anchor=tk.CENTER)

                # fetch data
                con = mysql.connect(host='', user='',
                                    password='', database='')
                c = con.cursor()
                c.execute('SELECT * FROM patient_infos')

                # populate data to treeview
                for rec in c:
                    tree.insert('', 'end', value=rec)

                # scrollbar
                sb = tk.Scrollbar(all_pat, orient=tk.VERTICAL,
                                  command=tree.yview)
                sb.grid(row=0, column=1, sticky='ns')
                tree.config(yscrollcommand=sb.set)
                a = tree.item(tree.focus())['values']

                btn = ttk.Button(all_pat, text='Close',
                                 command=all_pat.destroy)
                btn.grid(row=1, column=0, columnspan=2, sticky=E+W)
                con.close()

            # Defining buttons and placing them
            btn = ttk.Button(update, text='Edit', command=updates)
            btn_sp = ttk.Button(
                update, text='Search Patients', command=sp_patient)
            btn_all = ttk.Button(update, text='View all Patients',
                                 command=all_patients)
            btn_ext = ttk.Button(update, text='Close', command=update.destroy)
            btn_sp.grid(row=3, columnspan=3, sticky=E+W, pady=(10, 0))
            btn.grid(row=2, columnspan=3, sticky=E+W, pady=(10, 0))
            btn_all.grid(row=4, columnspan=3, sticky=E+W)
            btn_ext.grid(row=5, columnspan=3, sticky=E+W, pady=(10, 0))
            e_i_d.bind('<Return>',updates)

            # Making 1 ? icons
            q_mark_1 = Label(update, image=q_mark_new)
            q_mark_1.grid(row=1, column=2, padx=(0, 10))

            nametooltip_1 = Pmw.Balloon(root)
            nametooltip_1.bind(q_mark_1, 'Enter Sl.No:\nEnter the Sl.no. of the patient needed to be edited')

        else:
            messagebox.showerror(
                'Incorrect', 'Incorrect credentials, please try again',parent=admin)

    # Defining lables and buttons and entry widgets
    l = Label(admin, text='Login', font=Font(
        family='helvetica', size='20', weight='bold'))
    l2 = Label(admin, text='Username', font=Font(
        family='helvetica', size='13'))
    l3 = Label(admin, text='Password', font=Font(
        family='helvetica', size='13'))
    e1 = ttk.Entry(admin)
    e2 = ttk.Entry(admin, show='*')
    b = ttk.Button(admin, text='Login', command=login)

    # Placing buttons and labels and entry widgets and keybinding
    b.bind("<Return>", login)
    e2.bind("<Return>", login)
    e1.focus_force()
    l.grid(column=0, row=0, padx=(150,0), pady=(120, 15))
    l2.grid(column=0, row=1,columnspan=2)
    l3.grid(column=0, row=3,columnspan=2)
    e1.grid(column=0, row=2, ipady=5,padx=(150,0))
    e2.grid(column=0, row=4, ipady=5,padx=(150,0))
    b.grid(row=5, column=0, pady=(15,150), ipady=5, ipadx=35,columnspan=2)

    # Making 13 ? icons
    q_mark_1 = Label(admin, image=q_mark_new)
    q_mark_2 = Label(admin, image=q_mark_new)
    q_mark_1.grid(row=2, column=1, padx=(5, 130))
    q_mark_2.grid(row=4, column=1, padx=(5, 130))

    nametooltip_1 = Pmw.Balloon(root)
    nametooltip_2 = Pmw.Balloon(root)
    nametooltip_1.bind(q_mark_1, 'Username:\nEnter the given username')
    nametooltip_2.bind(q_mark_2, 'Password:\nEnter the given correct password')

# Function to get date of birth
def datepicker():
    global cal
    top = Toplevel(root)
    top.resizable(False,False)
    top.focus_force()
    top.title('Choose Date')
    top.geometry('+550+70')
    cal = Calendar(top, font="Arial 14", selectmode='day',
                   year=2006, month=9, day=1)
    cal.pack(fill="both", expand=True)
    Button(top, text="OK", command=top.destroy,
           font=font_text).pack(fill='both')

# Function to open health card
def newtop():

    def screenshots():
        win = gw.getWindowsWithTitle('Health Card')[0]
        winleft = win.left+9
        wintop = win.top+38
        winright = win.right-9
        winbottom = win.bottom-9
        final_rect = (winleft,wintop,winright,winbottom)
        card_img = ImageGrab.grab(final_rect)
        card_img.save(f'Health card of {e1.get()}.png')
        messagebox.showinfo(
            'Success', 'Image of Health Card has been saved successfully.',parent=new)

    if path == "":
        messagebox.showerror(
            'Choose Image', 'Please choose an image to see the health card',parent=root)

    else:
        try:
            dat = cal.selection_get()
            if e1.get() == "" or e2.get() == "" or e3.get() == "" or g.get() == "" or b.get() == "":
                messagebox.showerror(
                    'Fill all', 'Make sure to fill all fields, including date',parent=root)
            else:
                global new
                global img
                global img_prof
                new = Toplevel(root)
                new.resizable(False,False)
                new.focus_force()
                new.title('Health Card')
                new.iconbitmap('Image/icn_1.ico')
                new.geometry('+550+70')
                mainfiledir = Image.open('Image/ID Card.png')
                img = ImageTk.PhotoImage(mainfiledir)
                img_label = Label(new, image=img)
                img_label.grid(row=1, column=2)
                dir = Image.open(path)
                dir = dir.resize((150, 150), Image.ANTIALIAS)
                img_prof = ImageTk.PhotoImage(dir)
                img_label = Label(new, image=img_prof)
                img_label.place(x=500, y=150)

                # Placing Labels in grid
                lo1 = Label(new, text=e1.get(), bg='white',
                            font=Font(family='Times', size='14', weight='bold')).place(x=330, y=128)
                lo2 = Label(new, text=e2.get(), bg='white',
                            font=Font(family='Times', size='14', weight='bold')).place(x=345, y=158)
                lo3 = Label(new, text=e3.get(), bg='white',
                            font=Font(family='Times', size='14', weight='bold')).place(x=315, y=186)
                lo4 = Label(new, text=g.get(), bg='white',
                            font=Font(family='Times', size='14', weight='bold')).place(x=163, y=227)
                lo5 = Label(new, text=b.get(), bg='white',
                            font=Font(family='Times', size='14', weight='bold')).place(x=220, y=258)
                lo6 = Label(new, text=dat, bg='white',
                            font=Font(family='Times', size='14', weight='bold')).place(x=220, y=288)
                btn = ttk.Button(new, text='Save Card',
                                 command=screenshots)
                btn.place(x=495, y=350)

        except:
            messagebox.showerror(
                'Fill all', 'Make sure to fill all fields, including date',parent=root)

# Function to get the imagepath from filedialog
def imgpath():
    # Defining image path
    global path
    path = filedialog.askopenfilename(
        initialdir='/Downloads', title='Select Photo', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png')))

# Function to open exit messagebox
def popup():
    # Defining exit
    selection = messagebox.askyesno('Exit', 'Are you sure you want to exit?',parent=root)
    if selection == 1:
        root.destroy()
    else:
        Label(root, text="")

# Function to display about section
def about():
    # Defining Urls
    url = "https://nihaalnz.herokuapp.com"
    url_2 = "https://github.com/nihaalnz/patient-hsptl-app.git"

    def openweb():
        webbrowser.open(url, new=1)

    def openweb_2():
        webbrowser.open(url_2, new=1)

    # Define about section
    about = Toplevel(root)
    about.resizable(False,False)
    about.title('About')
    about.focus_force()
    about.iconbitmap('Image/icn_6.ico')
    about.geometry('300x300')
    # Making frames
    frame = LabelFrame(about, text='About this program', padx=5, pady=5)
    # Making frame items
    l_name = Label(frame, text='Created by Nihaal Nz')
    l_ver = Label(frame, text='Ver : 4.00')
    l_lic = Label(frame, text='Licensed under MIT')
    btn_sup = ttk.Button(frame, text='Website!', command=openweb)
    btn_cod = ttk.Button(frame, text='Source Code', command=openweb_2)
    btn_cls = ttk.Button(frame, text='Close', command=about.destroy)
    #Placing in screen
    frame.grid(row=0, column=0, padx=70, pady=40)
    l_name.grid(row=0, column=0)
    l_ver.grid(row=1, column=0)
    l_lic.grid(row=2, column=0)
    btn_sup.grid(row=3, columnspan=2, sticky=E+W, pady=(5, 0))
    btn_cod.grid(row=4, columnspan=2, sticky=E+W, pady=5)
    btn_cls.grid(row=5, columnspan=2, sticky=E+W)

# Function to reset all fields
def reset():
    # Defining Reset
    select = messagebox.askyesno(
        'Reset', 'Are you sure you want to reset all boxes?',parent=root)
    if select == 1:
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
    else:
        Label(root, text="")


# Define menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add menu items
file_menu = Menu(my_menu)
my_menu.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='Manage', command=manage)
file_menu.add_separator()
file_menu.add_command(label='About', command=about)
file_menu.add_separator()
file_menu.add_command(label='Reset', command=reset)
file_menu.add_command(label='Exit', command=popup)

# Defining Labels
l1 = ttk.Label(root, text='Name', font=font_text)
l2 = ttk.Label(root, text='Phone Number', font=font_text)
l3 = ttk.Label(root, text='Emirates ID', font=font_text)
l4 = ttk.Label(root, text='Email Address', font=font_text)
l5 = ttk.Label(root, text='Gender', font=font_text)
l6 = ttk.Label(root, text='Date Of Birth', font=font_text)
l7 = ttk.Label(root, text='Nationality', font=font_text)
l8 = ttk.Label(root, text='Blood Group', font=font_text)
l9 = ttk.Label(root, text='Test for COVID-19', font=font_text)
l10 = ttk.Label(root, text='Emergency Contact Number', font=font_text)
l11 = ttk.Label(root, text='Select Photo', font=font_text)

# Defining variables
name = StringVar()
ph = StringVar()
e_id = StringVar()
em_id = StringVar()
nation = StringVar()
emerg = StringVar()

# Defining Entry widget
e1 = ttk.Entry(root, textvariable=name)
e2 = ttk.Entry(root, textvariable=ph)
e3 = ttk.Entry(root, textvariable=e_id)
e4 = ttk.Entry(root, textvariable=em_id)
e5 = ttk.Entry(root, textvariable=nation)
e6 = ttk.Entry(root, textvariable=emerg)

# Defining Buttons
b_ch = ttk.Button(root, text='Select Image', command=imgpath)
b_id = ttk.Button(root, text='Make Health Card', command=newtop)
b_db = ttk.Button(root, text='Submit', command=database)
b_ex = ttk.Button(root, text='Exit', command=popup)
b_re = ttk.Button(root, text='Reset', command=reset)
b_dt = ttk.Button(root, text='Choose Date', command=datepicker)
b_mng = ttk.Button(root, text='Manage', command=manage)

# Defining Gender Dropdown
g = StringVar()
g.set('Choose Gender')
opt_g = OptionMenu(root, g, *gen)
men = opt_g.nametowidget(opt_g.menuname)
men.configure(font=font_button)

# Defining Blood Dropdown
b = StringVar()
b.set('Choose group')
opt_blo = OptionMenu(root, b, *bl_gr)
optu = opt_blo.nametowidget(opt_blo.menuname)
optu.configure(font=font_button)

# Defining COVID Dropdown
co = StringVar()
co.set('Choose result')
opt_cov = OptionMenu(root, co, *cov)
opti = opt_cov.nametowidget(opt_cov.menuname)
opti.configure(font=font_button)

# Placing Lables
l1.grid(row=0, column=0, padx=10)
l2.grid(row=1, column=0, padx=10)
l3.grid(row=2, column=0, padx=10)
l4.grid(row=3, column=0, padx=10)
l5.grid(row=4, column=0, padx=10)
l6.grid(row=5, column=0, padx=10)
l7.grid(row=6, column=0, padx=10)
l8.grid(row=7, column=0, padx=10)
l9.grid(row=8, column=0, padx=10)
l10.grid(row=9, column=0, padx=10)
l11.grid(row=10, column=0, padx=10)

# Placing Entry
e1.grid(row=0, column=1, pady=5, ipady=5, padx=5)
e2.grid(row=1, column=1, pady=5, ipady=5, padx=5)
e3.grid(row=2, column=1, pady=5, ipady=5, padx=5)
e4.grid(row=3, column=1, pady=5, ipady=5, padx=5)
e5.grid(row=6, column=1, pady=6, ipady=5, padx=5)
e6.grid(row=9, column=1, pady=5, ipady=5, padx=5)

# Placing Button
b_ch.grid(row=10, column=1, sticky=E+W, pady=5, padx=5)
b_id.grid(row=11, column=0, sticky=E+W, padx=30, pady=5)
b_db.grid(row=11, column=1, sticky=E+W, padx=5, pady=5)
b_ex.grid(row=13, columnspan=3, sticky=E+W, pady=(10, 0), ipady=3)
b_re.grid(row=12, column=0, sticky=E+W, padx=30, pady=5)
b_dt.grid(row=5, column=1, sticky=E+W, padx=7, pady=5, ipadx=5)
b_mng.grid(row=12, column=1, sticky=E+W, padx=5, pady=5)

# Placing Dropdown
opt_g.grid(row=4, column=1, ipadx=6, pady=3)
opt_blo.grid(row=7, column=1, padx=5, ipadx=10)
opt_cov.grid(row=8, column=1, ipadx=12, pady=5)

# Creating ? icons
q_mark = Image.open('Image/question_mark.png')
q_mark_re = q_mark.resize((15, 15), Image.ANTIALIAS)
q_mark_new = ImageTk.PhotoImage(q_mark_re)

# Making 13 ? icons
q_mark_1 = Label(root, image=q_mark_new)
q_mark_1.grid(row=0, column=2, padx=(0, 10))
q_mark_2 = Label(root, image=q_mark_new)
q_mark_2.grid(row=1, column=2, padx=(0, 10))
q_mark_3 = Label(root, image=q_mark_new)
q_mark_3.grid(row=2, column=2, padx=(0, 10))
q_mark_4 = Label(root, image=q_mark_new)
q_mark_4.grid(row=3, column=2, padx=(0, 10))
q_mark_5 = Label(root, image=q_mark_new)
q_mark_5.grid(row=4, column=2, padx=(0, 10))
q_mark_6 = Label(root, image=q_mark_new)
q_mark_6.grid(row=5, column=2, padx=(0, 10))
q_mark_7 = Label(root, image=q_mark_new)
q_mark_7.grid(row=6, column=2, padx=(0, 10))
q_mark_8 = Label(root, image=q_mark_new)
q_mark_8.grid(row=7, column=2, padx=(0, 10))
q_mark_9 = Label(root, image=q_mark_new)
q_mark_9.grid(row=8, column=2, padx=(0, 10))
q_mark_10 = Label(root, image=q_mark_new)
q_mark_10.grid(row=9, column=2, padx=(0, 10))
q_mark_11 = Label(root, image=q_mark_new)
q_mark_11.grid(row=10, column=2, padx=(0, 10))
q_mark_12 = Label(root, image=q_mark_new)
q_mark_12.grid(row=11, column=2, padx=(0, 10))
q_mark_13 = Label(root, image=q_mark_new)
q_mark_13.grid(row=12, column=2, padx=(0, 10))
q_mark_14 = Label(root, image=q_mark_new)
q_mark_14.grid(row=11, column=0, padx=(0, 10),sticky=E)
q_mark_15 = Label(root, image=q_mark_new)
q_mark_15.grid(row=12, column=0, padx=(0, 10),sticky=E)

# Creating a tooltip for each ? icon
nametooltip_1 = Pmw.Balloon(root)
nametooltip_1.bind(q_mark_1, 'Name:\nEnter a valid full name')
nametooltip_2 = Pmw.Balloon(root)
nametooltip_2.bind(q_mark_2, 'Phone Number:\nEnter a phone number less than 11 digits')
nametooltip_3 = Pmw.Balloon(root)
nametooltip_3.bind(q_mark_3, 'Emirates ID:\nEnter Emirates ID less than 16 digits')
nametooltip_4 = Pmw.Balloon(root)
nametooltip_4.bind(q_mark_4, 'Email Address:\nEnter a valid email address')
nametooltip_5 = Pmw.Balloon(root)
nametooltip_5.bind(q_mark_5, 'Gender:\nChoose Gender from the dropdown box')
nametooltip_6 = Pmw.Balloon(root)
nametooltip_6.bind(q_mark_6, 'Date of Birth:\nPick Date of Birth from the box ')
nametooltip_7 = Pmw.Balloon(root)
nametooltip_7.bind(q_mark_7, 'Nationality:\nEnter your nationality')
nametooltip_8 = Pmw.Balloon(root)
nametooltip_8.bind(q_mark_8, 'Blood Group:\nChoose your blood group from the dropdown box')
nametooltip_9 = Pmw.Balloon(root)
nametooltip_9.bind(q_mark_9, 'COVID result:\nChoose a suitable option\nYes - If tested positive\nNo - If tested negative\nN/A - If hadnt done a test yet')
nametooltip_10 = Pmw.Balloon(root)
nametooltip_10.bind(q_mark_10, 'Emergency Number:\nEnter a number to be contacted in cases of emergency')
nametooltip_11 = Pmw.Balloon(root)
nametooltip_11.bind(q_mark_11, 'Select a photo:\nClick to provide a photo for the health card')
nametooltip_12 = Pmw.Balloon(root)
nametooltip_12.bind(q_mark_12, 'Submit the data:\nClick to enter the data into the database')
nametooltip_13 = Pmw.Balloon(root)
nametooltip_13.bind(q_mark_13, 'Manage:\nClick to open administration panel')
nametooltip_14 = Pmw.Balloon(root)
nametooltip_14.bind(q_mark_14, 'Make a health card:\nClick to create health card with the given data')
nametooltip_15 = Pmw.Balloon(root)
nametooltip_15.bind(q_mark_15, 'Reset:\nClick to clear all the fields')


# Ending program
root.mainloop()
