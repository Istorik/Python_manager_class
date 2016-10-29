#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ssh nohup firefox "438school.spb.ru" &
# "ssh " + ip + " \'export DISPLAY=:0; nohup firefox \'438school.spb.ru\' \' >/dev/null"
# "ssh " + ip + " \'export DISPLAY=:0; notify-send "Система оповещения" "Пример работы" \' >/dev/null"

import threading, time, os
from datetime import datetime
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from subprocess import *
from colored import fg, bg, attr

dt = datetime.now()
dt = dt.strftime("%d.%m.%Y")

ip_list_all = ["192.168.10.51", "192.168.10.52", "192.168.10.53", "192.168.10.54", "192.168.10.55", "192.168.10.56", "192.168.10.57", "192.168.10.58", "192.168.10.59", "192.168.10.60"]
ip_list = []
tex = dict()
text_comp = dict()

# Функции
def info(inf):
    text_command.delete(0,END)
    text_command.insert(END, inf)

def ping_class(ip):
    try:
        check_call(["ping -c 1 " + ip +" >/dev/null"], shell = True)
        ip_list.append(ip)
        text = "OK" 
    except:
        text = "ERROR" 
    tex[ip].insert(END, text)

def update(ip):
    try:
        check_call(["ssh " + ip +" \'sudo aptitude update && sudo aptitude dist-upgrade -y \' >/dev/null"], shell = True)
        text="OK"
    except:
        text="ERROR" 
    tex[ip].insert(END, text)

def shutdown(ip):
    try:
        check_call(["ssh " + ip +" \'sudo shutdown -h now\' >/dev/null"], shell = True)
        text="OK"
    except:
        text="ERROR" 
    tex[ip].insert(END, text)

def com(ip, command):
    try:
        check_call(["ssh " + ip + " \'sudo " + command + " \' >/dev/null"], shell = True)
        text = "OK"
    except:
        text = "ERROR"
    tex[ip].insert(END, text)

# Функции ученика

def com_uchenik(ip, command):
    try:
        check_call(["ssh uchenik@" + ip + " \'" + command + "\' >/dev/null"], shell = True)
        text = "OK"
    except:
        text = "ERROR"
    tex[ip].insert(END, text)

def com_upload(ip, file_):
    try:
        check_call(["scp "+ file_ + "uchenik@" + ip + ":/home/uchenik/Material"], shell = True)
        text="OK"
    except:
        text="ERROR"
    tex[ip].insert(END, text)
	
def com_download(ip, file_):
    try:
        check_call(["scp -r " + ip + ":/home/uchenik/Rabota/* " + file_ + "/" + ip], shell = True)
        #check_call(["touch  " + file_ + "/" + ip], shell = True)
        text="OK"
        com_uchenik(ip, "rm -r /home/uchenik/Rabota/*")
    except:
        text="ERROR"
    tex[ip].insert(END, text)

# Кнопки

def button_ping(event):
    info("Ping")
    ip_list.clear()
    for ip in ip_list_all:
        tex[ip].delete(0,END)
        threading.Thread(target=ping_class, args=[ip]).start()

def button_update(event):
    info("Обновляем")
    for ip in ip_list_all:
        tex[ip].delete(0,END) 
        threading.Thread(target=update, args=[ip]).start()

def button_ntpdate(event):
    info("ntpdate")
    for ip in ip_list:  
        tex[ip].delete(0,END)
        threading.Thread(target=com, args=[ip, 'ntpdate -s 192.168.10.1']).start()

def button_reboot(event):
    info("Перезагружаем")
    for ip in ip_list:
        threading.Thread(target=com, args=[ip, 'reboot']).start()

def button_shutdown(event):
    text_command.insert(END, "Выключаем")
    info("Выключаем")
    for ip in ip_list:
        threading.Thread(target=shutdown, args=[ip]).start()     

def button_com(event):
    info("Команда")
    for ip in ip_list:
        tex[ip].delete(0,END)
        threading.Thread(target=com, args=[ip, ent.get()]).start()

# Команды ученика

def button_link(event):
    s = ent.get()
    info("Открыть ссылку")
    for ip in ip_list:
        threading.Thread(target=com_uchenik, args=[ip, 'export DISPLAY=:0; firefox \"%s\"' % s ]).start()
        
def button_send(event):
    s = ent.get()
    info("Сообщение")
    for ip in ip_list:
        tex[ip].delete(0,END)
        threading.Thread(target=com_uchenik, args=[ip, 'export DISPLAY=:0; notify-send "Система оповещения" "%s"' % s ]).start()

def button_upload(event):
    info("Загрузить файл")
    op = askopenfilename()
    for ip in ip_list:
        threading.Thread(target=com_upload, args=[ip, op]).start()

def button_download(event):
    info("Собрать работы")
    op = askdirectory()
    if len(op)>1:
        _dir = op + "/" + dt
        os.mkdir(_dir, mode=0o750, dir_fd=None)
        for ip in ip_list:
            tex[ip].delete(0,END)
            d = _dir + "/" + ip
            os.mkdir(d, mode=0o750, dir_fd=None)
            threading.Thread(target=com_download, args=[ip, d]).start()
    else:
        info("Упс...")

# Меню

def new_win():
    win = Toplevel(root)
 
def close_win():
    if askyesno("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()
 
def about():
    showinfo("Editor", "This is text editor.\n(test version)")

# Окошки

root = Tk()

m = Menu(root) #создается объект Меню на главном окне
root.config(menu=m) #окно конфигурируется с указанием меню для него

frame_button = Frame(root,width=100,heigh=100,bd=5)
frame_info = Frame(root,width=50,heigh=100,bd=5)
frame_txt = Frame(root,width=50,heigh=100,bd=5)

text_comp0 = Label(frame_info, text="Команда", font="Verdana 12")
text_command = Entry(frame_txt,width=30, font="Verdana 12")

ent = Entry(frame_button,width=40)

but2 = Button(frame_button)
but2["text"] = "ping class" 
but2["width"] = 20
but2["font"] = 'arial 14'
but2.bind("<Button-1>",button_ping)
but3 = Button(frame_button, text='Выключить class', width=20, font='arial 14')
but3.bind("<Button-1>",button_shutdown)
but4 = Button(frame_button, text='Перезагрузить class', width=20, font='arial 14')
but4.bind("<Button-1>",button_reboot)
but5 = Button(frame_button, text='Обновить class', width=20, font='arial 14')
but5.bind("<Button-1>",button_update)
but6 = Button(frame_button, text='NtpUpdate', width=20, font='arial 14')
but6.bind("<Button-1>",button_ntpdate)
but7 = Button(frame_button, text='Ссылка', width=20, font='arial 14')
but7.bind("<Button-1>",button_link)
but8 = Button(frame_button, text='Сообщение', width=20, font='arial 14')
but8.bind("<Button-1>",button_send)
but9 = Button(frame_button, text='Загрузить файл', width=20, font='arial 14')
but9.bind("<Button-1>",button_upload)
but10 = Button(frame_button, text='Собрать работы', width=20, font='arial 14')
but10.bind("<Button-1>",button_download)
but11 = Button(frame_button, text='Выполнить команду', width=20, font='arial 14')
but11.bind("<Button-1>",button_com)

but99 = Button(frame_button, text='Закрыть', width=20, font='arial 14')
but99.bind("<Button-1>",close_win)

# Меню

fm = Menu(m) #создается пункт меню с размещением на основном меню (m)
m.add_cascade(label="File",menu=fm) #пункту располагается на основном меню (m)
fm.add_command(label="Open...") #формируется список команд пункта меню
fm.add_command(label="New",command=new_win)
fm.add_command(label="Save...")
fm.add_command(label="Exit",command=close_win)

hm = Menu(m) #второй пункт меню
m.add_cascade(label="Help",menu=hm)
hm.add_command(label="Help")
hm.add_command(label="About",command=about) 

frame_button.grid(row=0, column=0, sticky='n')
frame_info.grid(row=0, column=1, rowspan=2)
frame_txt.grid(row=0, column=2, rowspan=2)

but2.pack()
but3.pack()
but4.pack()
but5.pack()
but6.pack()
but7.pack()
but8.pack()
but9.pack()
but10.pack()
but11.pack()

# Конец
but99.pack()

text_comp0.pack()
text_command.pack()

# Вся правая колонка запихнута в один цикл. 
for ip in ip_list_all:
    text_comp[ip] = Label(frame_info, text=ip, font="Verdana 12")
    tex[ip] = Entry(frame_txt,width=6, font="Verdana 12")
    text_comp[ip].pack()
    tex[ip].pack()

ent.pack()

# Старт системы

info("Ping class")


for ip in ip_list_all:
    threading.Thread(target=ping_class, args=[ip]).start()

ip_list = ip_list_all if len(ip_list) == 0 else ip_list

root.mainloop()
