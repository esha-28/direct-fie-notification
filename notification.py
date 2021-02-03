import urllib.request
import webbrowser

from pynotifier import Notification

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from bs4 import BeautifulSoup as bs
import re

import whois
from urllib.parse import urlparse

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pa01720283795pa",
    database="mydatabase"
)

root = Tk()
root.title('file information of a webpage')
root.geometry('600x500')  # ('width*height)
root.config(bg="ghost white")
root.iconbitmap(r'iconfinder_Folder-Info_60178.ico')

def mouse_left_click(u):
    message = messagebox.askokcancel("download", "it is a direct download file.r u sure to download it?")
    if message is True:
        webbrowser.open_new(u)
    else:
        pass


def files(ff):
    global f_info
    if f_info:
        f_info.destroy()
    f_info = Frame(frame_format, bg='powder blue')
    f_info.grid(rowspan=2, columnspan=6, padx=10, pady=10, sticky='w', ipadx=20, ipady=10)
    links = []
    texts = []
    for i in soup.find_all("a", href=re.compile(ff)):

        if i.get('href')[-4:] == ff:

            links.append(i.get('href'))
            texts.append(i.get_text())
        else:
            pass

    if len(links) > 0:

        for k in range(len(links)):
            l = Label(f_info, text=texts[k], cursor='hand2', bg='powder blue', fg='blue')
            l.bind("<Button-1>", lambda e: mouse_left_click(links[k]))
            l.grid(row=k, column=0, ipadx=3, ipady=3, padx=5, pady=5, sticky='w')
    else:
        l = Label(f_info, text='no' + '  ' + ff + '  ' + ' file', bg='powder blue', fg='blue')
        l.grid(row=0, column=0, ipadx=3, ipady=3, padx=5, pady=5, sticky='w')

def func():
    global file_format
    file_format = comboExample.get()
    if file_format.lower() == '.exe':
        files(file_format)
    elif file_format.lower() == '.zip':
        files(file_format)
    elif file_format.lower() == '.pdf':
        files(file_format)
    elif file_format.lower() == '.doc':
        files(file_format)
    else:
        messagebox.showinfo('Format Information', 'Only for file format types .exe, .zip, .pdf, .doc')


def func_keyboard(event):
    func()

def domain_info():
    try:
        if 'http://' in E1.get() or 'https://' in E1.get():
            domain_url = urlparse(E1.get())
        else:
            domain_url=urlparse('http://'+E1.get())
        domain=domain_url.netloc
        domain_info = whois.whois(domain)
        root2 = Tk()
        root2.title("domain information")
        t1 = Text(root2, bg='teal', fg='white', font=('arial', 10))
        t1.insert(END, domain_info)
        t1.grid()

        def close():
            root2.destroy()

        close_button = Button(root2, text='close', command=close, border=2, bg='gray')
        close_button.grid(row=1, sticky='e')
        root2.mainloop()


    except:
        messagebox.showerror('check', 'Invalid Domain.\n check the url')


def open_url():
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(E1.get())

def func2():
    global frame_format
    if frame_format:
        frame_format.destroy()
    frame_format = Frame(root, bg='ghost white')
    frame_format.grid(rowspan=3, columnspan=3, pady=10, sticky='w', padx=50)
    global p
    global soup
    try:
        request_url = urllib.request.urlopen(E1.get())
        p = request_url.read()
        soup = bs(p, 'html.parser')
        mycursor = mydb.cursor()
        sql_delete = "DROP TABLE IF EXISTS url"
        mycursor.execute(sql_delete)
        mycursor.execute("CREATE TABLE url (link VARCHAR(1000), text VARCHAR(1000))")
        sql = "INSERT INTO url (link,text) VALUES (%s, %s)"

        for link in soup.find_all("a"):
            val = (link.get('href'), link.get_text())
            mycursor.execute(sql, val)
        mycursor.execute(
            "SELECT link FROM url WHERE link LIKE '%.exe' OR link LIKE '%.zip' OR link LIKE '%.pdf' OR link LIKE '%.doc'")
        myresult_link = mycursor.fetchall()

        if len(myresult_link) > 0:
            Notification(title='FILE INFORMATION',
                         description='has direct download files in this url code',
                         icon_path=r'bell_sign_twitter_icon_127116.ico',
                         duration=15).send()

            labelTop = Label(frame_format, text="Choose file format:", font=('arial', 10, 'bold'), bg='teal',
                             fg='white', border=2)
            labelTop.grid(column=0, row=0, padx=5, ipady=3, ipadx=3)
            global comboExample
            comboExample = ttk.Combobox(frame_format,
                                        values=[
                                            ".exe",
                                            ".zip",
                                            ".pdf",
                                            ".doc"]
                                        )
            comboExample.grid(column=1, row=0, padx=5, ipady=3)
            comboExample.bind("<Return>", func_keyboard)

            format_button = Button(frame_format, image=photo2, command=func)
            format_button.grid(row=0, column=2, pady=3)
        else:
            Notification(title='FILE INFORMATION',
                         description='no direct download file in this url',
                         icon_path=r'C:bell_sign_twitter_icon_127116.ico',
                         duration=15).send()

    except:
        Notification(title='Check the URL',
                     description='May be format is incorrect or incorrect url.\n Format_Ex- http://example.--/--/ or https://example.--/--/',
                     icon_path=r'bell_sign_twitter_icon_127116.ico',
                     duration=15).send()



def func2_keyboard(event):
    func2()


L1 = Label(root, text="Search a Url:", font=('arial', 10, 'bold'), bg='light gray')
L1.grid(row=0, column=0, padx=5, ipady=3)
photo1 = PhotoImage(file=r"iconfinder_search_magnifying_glass_find_103857.png")
photo2 = PhotoImage(file=r"602.9-send-message-icon-iconbunny.png")

E1 = Entry(root, textvariable=StringVar(), width=60, border=3)
E1.grid(row=0, column=1, ipady=5, pady=6, sticky='w')
E1.bind("<Return>", func2_keyboard)

E1_button = Button(root, image=photo1, command=func2)
E1_button.grid(row=0, column=2, pady=5)

url_button=Button(root,text='open in browser >>',command=open_url)
url_button.grid(row=1,columnspan=2,sticky='e')

domain_info=Button(root,text='domain info >>',command=domain_info)
domain_info.grid(row=2,column=0,sticky='w',padx=5)

frame_format = None
f_info = None

root.mainloop()
