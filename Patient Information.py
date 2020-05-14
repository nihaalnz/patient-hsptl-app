from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from tkcalendar import Calendar
import mysql.connector as mysql
from tkinter import ttk
from ttkthemes import themed_tk as tktheme
import webbrowser
#root = Tk()

#Makign the main window 
root = tktheme.ThemedTk()
root.get_themes()
root.set_theme('vista')
root.title('Patient Information')
root.iconbitmap('icon.ico')
font_text = Font(family='helvetica', size='11')
font_button = Font(size='10')

#Defining Dropdown options
gen = ['Male', 'Female']
bl_gr = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
cov = ['Yes', 'No', 'N/A']

#Defining functions:

def database():
    #Defining Variables for db
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

    #Inserting into db
    if nme == "" or p_h == "" or eid == "" or ema_id == "" or nat == "" or emer == "" or gend == "" or bloo == "" or covi == "" or dat == "":
        messagebox.showinfo('Fill all', 'All fields are necessary')
    else:
        #Establishing connection
        con = mysql.connect(host='db4free.net', user='nihaalnz',
                            password='monkey12345', database='nihaalnztrying')
        
        #Making SQL command
        sql_command = "INSERT into patient_infos (`full_name`,`ph_no`,`emirate_id`,`email_addr`,`gender`,`DOB`,`nationality`,`blood_grp`,`COVID_test`,`emergency_no`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"                     
        values = (nme,p_h,eid,ema_id,gend,str(dat),nat,str(bloo),str(covi),emer)
        #Defining cursor
        c = con.cursor()
        #Executing and saving SQL command
        c.execute(sql_command, values)
        c.execute('commit')
        #Closing the connection
        con.close()
        #Success message
        messagebox.showinfo(
            'Success', 'All values have been entered to the database')
        #Reseting all the boxes
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)


def datepicker():
    global cal
    global a

    def date():
        global cal
        a = cal.selection_get()

    top = Toplevel(root)
    top.title('Choose Date')
    cal = Calendar(top, font="Arial 14", selectmode='day',
                   year=2006, month=1, day=1)
    cal.pack(fill="both", expand=True)
    Button(top, text="OK", command=top.destroy,
           font=font_text).pack(fill='both')


def newtop():
    global new
    global img
    global img_prof
    new = Toplevel(root)
    mainfiledir = Image.open('Image/ID Card.png')
    img = ImageTk.PhotoImage(mainfiledir)
    img_label = Label(new, image=img)
    img_label.grid(row=1, column=2)
    dir = Image.open(path)
    dir = dir.resize((150, 150), Image.ANTIALIAS)
    img_prof = ImageTk.PhotoImage(dir)
    img_label = Label(new, image=img_prof)
    img_label.place(x=500, y=150)
    #Placing Labels in grid
    lo1 = Label(new, text=e1.get(), bg='white',
                font=font_text).place(x=330, y=130)
    lo2 = Label(new, text=e2.get(), bg='white',
                font=font_text).place(x=345, y=160)
    lo3 = Label(new, text=e3.get(), bg='white',
                font=font_text).place(x=315, y=188)
    lo4 = Label(new, text=g.get(), bg='white',
                font=font_text).place(x=163, y=229)
    lo5 = Label(new, text=b.get(), bg='white',
                font=font_text).place(x=220, y=260)
    lo6 = Label(new, text=cal.selection_get(), bg='white',
                font=font_text).place(x=220, y=290)


def imgpath():
    #Defining image path
    global path
    path = filedialog.askopenfilename(initialdir='/Donwloads', title='Select Photo', filetypes=(('PNG files', '*.png'),
                                                                                                ('JPEG files', '*.jpg')))


def popup():
    #Defining exit 
    selection = messagebox.askyesno('Exit', 'Are you sure you want to exit?')
    if selection == 1:
        root.destroy()
    else:
        Label(root, text="")


def about():
    #Defining Urls 
    url = "https://nihaalnz.herokuapp.com"
    url_2 = "https://github.com/nihaalnz/patient-hsptl-app.git"

    def openweb():
        webbrowser.open(url,new=1)
    
    def openweb_2():
        webbrowser.open(url_2,new=1)
    
    #Define about section
    about = Toplevel(root)
    about.title('About')
    about.geometry('300x300')
    #Making frames
    frame = LabelFrame(about,text='About this program',padx=5,pady=5)    
    #Making frame items
    l_name = Label(frame,text='Created by Nihaal Nz')
    l_ver = Label(frame,text='Ver : 1.00')
    l_lic = Label(frame,text='Licensed under MIT')
    btn_sup = Button(frame,text='Website!',command=openweb)
    btn_cod = Button(frame,text='Source Code',command=openweb_2)
    btn_cls = Button(frame,text='Close',command=about.destroy)
    #Placing in screen
    frame.grid(row=0,column=0,padx=70,pady=40)
    l_name.grid(row=0,column=0)
    l_ver.grid(row=1,column=0)
    l_lic.grid(row=2,column=0)
    btn_sup.grid(row=3,columnspan=2,sticky=E+W,pady=(5,0))
    btn_cod.grid(row=4,columnspan=2,sticky=E+W,pady=5)
    btn_cls.grid(row=5,columnspan=2,sticky=E+W)


def reset():
    #Defining Reset  
    select = messagebox.askyesno('Reset', 'Are you sure you want to reset all boxes?')
    if select == 1:
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
    else:
        Label(root, text="")


#Define menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add menu items
file_menu = Menu(my_menu)
my_menu.add_cascade(label='File',menu=file_menu)
file_menu.add_command(label='About',command=about)
file_menu.add_separator()
file_menu.add_command(label='Reset',command=reset)
file_menu.add_command(label='Exit',command=popup)

#Defining Labels
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

#Defining variables
name = StringVar()
ph = StringVar()
e_id = StringVar()
em_id = StringVar()
nation = StringVar()
emerg = StringVar()

#Defining Entry widget
e1 = ttk.Entry(root, textvariable=name)
e2 = ttk.Entry(root, textvariable=ph)
e3 = ttk.Entry(root, textvariable=e_id)
e4 = ttk.Entry(root, textvariable=em_id)
e5 = ttk.Entry(root, textvariable=nation)
e6 = ttk.Entry(root, textvariable=emerg)

#Defining Buttons
b_ch = ttk.Button(root, text='Select Image', command=imgpath)
b_id = ttk.Button(root, text='Make Health Card', command=newtop)
b_db = ttk.Button(root, text='Enter Database', command=database)
b_ex = ttk.Button(root, text='Exit', command=popup)
b_re = ttk.Button(root, text='Reset', command=reset)
b_dt = ttk.Button(root, text='Choose Date', command=datepicker)

#Defining Gender Dropdown
g = StringVar()
g.set('Choose Gender')
opt_g = OptionMenu(root, g, *gen)
men = opt_g.nametowidget(opt_g.menuname)
men.configure(font=font_button)

#Defining Blood Dropdown
b = StringVar()
b.set('Choose group')
opt_blo = OptionMenu(root, b, *bl_gr)
optu = opt_blo.nametowidget(opt_blo.menuname)
optu.configure(font=font_button)

#Defining COVID Dropdown
co = StringVar()
co.set('Choose result')
opt_cov = OptionMenu(root, co, *cov)
opti = opt_cov.nametowidget(opt_cov.menuname)
opti.configure(font=font_button)

#Placing Lables
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

#Placing Entry
e1.grid(row=0, column=1, pady=5, ipady=5, padx=5)
e2.grid(row=1, column=1, pady=5, ipady=5, padx=5)
e3.grid(row=2, column=1, pady=5, ipady=5, padx=5)
e4.grid(row=3, column=1, pady=5, ipady=5, padx=5)
e5.grid(row=6, column=1, pady=6, ipady=5, padx=5)
e6.grid(row=9, column=1, pady=5, ipady=5, padx=5)

#Placing Button
b_ch.grid(row=10, column=1, sticky=E+W, pady=5, padx=5)
b_id.grid(row=11, column=0, sticky=E+W, padx=10, pady=5)
b_db.grid(row=11, column=1, sticky=E+W, padx=5, pady=5)
b_ex.grid(row=12, column=1, sticky=E+W, padx=5, pady=5)
b_re.grid(row=12, column=0, sticky=E+W, padx=10, pady=5)
b_dt.grid(row=5, column=1, sticky=E+W, padx=7, pady=5, ipadx=5)

#Placing Dropdown
opt_g.grid(row=4, column=1, ipadx=6, pady=3)
opt_blo.grid(row=7, column=1, padx=5, ipadx=10)
opt_cov.grid(row=8, column=1, ipadx=12, pady=5)

#Ending program
root.mainloop()
