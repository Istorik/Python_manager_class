#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ssh nohup firefox "438school.spb.ru" &
# "ssh " + ip + " \'export DISPLAY=:0; nohup firefox \'438school.spb.ru\' \' >/dev/null"
# "ssh " + ip + " \'export DISPLAY=:0; notify-send "Система оповещения" "Пример работы" \' >/dev/null"

import threading, time, os
from datetime import datetime
from tkinter import *
from subprocess import *
from colored import fg, bg, attr

dt = datetime.now()
dt = dt.strftime("%d.%m.%Y")

ip_list_all = ["192.168.10.51", "192.168.10.52", "192.168.10.53", "192.168.10.54", "192.168.10.55", "192.168.10.56", "192.168.10.57", "192.168.10.58", "192.168.10.59", "192.168.10.60"]
ip_list = []
tex = dict()
text_comp = dict()

# Функции
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
        text="Обновляем %s OK\n" % (ip)
    except:
        text="Обновляем %s ERROR\n" % (ip) 
    tex.insert(END, text)

def shutdown(ip):
    try:
        check_call(["ssh " + ip +" \'sudo shutdown -h now\' >/dev/null"], shell = True)
        text="Выключаем %s OK\n" % (ip)
    except:
        text="Выключаем %s ERROR\n" % (ip) 
    tex.insert(END, text)

def com(ip, command):
	try:
		check_call(["ssh " + ip + " \'sudo " + command + " \' >/dev/null"], shell = True)
		text="%s %s OK\n" % (command, ip)
	except:
		text="%s %s ERROR\n" % (command, ip)
	tex.insert(END, text)

# Функции ученика

def com_uchenik(ip, command):
	try:
		check_call(["ssh uchenik@" + ip + " \'export DISPLAY=:0; " + command + " \' >/dev/null"], shell = True)
		text="%s %s OK\n" % (command, ip)
	except:
		text="%s %s ERROR\n" % (command, ip)
	tex.insert(END, text)

def com_upload(ip, file_):
	try:
		check_call(["scp "+ file_ + "uchenik@" + ip + ":/home/uchenik/Material"], shell = True)
		text="Загрузка файла %s на %s OK\n" % (file_, ip)
	except:
		text="Загрузка файла %s на %s ERROR\n" % (file_, ip)
	tex.insert(END, text)
	
def com_download(ip, file_):
	try:
		check_call(["scp -r " + ip + ":/home/uchenik/Rabota/* " + file_], shell = True)
		text="%s %s OK\n" % (command, ip)
	except:
		text="%s %s ERROR\n" % (command, ip)
	tex.insert(END, text)

# Кнопки

def button_ping(event):
    text_command.insert(END, "Ping")
    ip_list.clear()
    for ip in ip_list_all:
        threading.Thread(target=ping_class, args=[ip]).start()

def button_update(event):
    text_command.insert(END, "Обновляем")
    for ip in ip_list_all:
        print("Обновляем %s ...\r" % (ip), end="")
        threading.Thread(target=update, args=[ip]).start()

def button_ntpdate(event):
    text_command.insert(END, "ntpdate")
    for ip in ip_list:
        threading.Thread(target=com, args=[ip, 'ntpdate -s 192.168.10.1']).start()

def button_reboot(event):
    text_command.insert(END, "Перезагружаем")
    for ip in ip_list:
        threading.Thread(target=com, args=[ip, 'reboot']).start()

def button_shutdown(event):
    print("Выключаем %s ...\r" % (ip), end="")
    for ip in ip_list:
        threading.Thread(target=shutdown, args=[ip]).start()     

# Команды ученика

def button_link(event):
    s = ent.get()
    print("Открыть ссылку")
    print(s)
    for ip in ip_list:
        threading.Thread(target=com_uchenik, args=[ip, 'firefox \"%s\"' % s ]).start()
        
def button_send(event):
    s = ent.get()
    print("Сообщение")
    print(s)
    for ip in ip_list:
        threading.Thread(target=com_uchenik, args=[ip, 'export DISPLAY=:0; notify-send "Система оповещения" "%s"' % s ]).start()

def button_upload(event):
    print("Загрузить файл")
    for ip in ip_list:
        threading.Thread(target=com_upload, args=[ip, 'firefox \"438school.spb.ru\"']).start()

def button_download(event):
    print("Собрать работы")
    os.mkdir(dt, mode=0o777, dir_fd=None) 
    for ip in ip_list:
        threading.Thread(target=com_download, args=[ip, 'firefox \"438school.spb.ru\"']).start()

# Меню

def new_win():
    win = Toplevel(root)
 
def close_win():
#     global root
#     root.destroy()
    root.quit()
 
def about():
    win = Toplevel(root)
    lab = Label(win,text="Это просто программа-тест \n меню в Tkinter")
    lab.pack() 

# Окошки

root = Tk()

m = Menu(root) #создается объект Меню на главном окне
root.config(menu=m) #окно конфигурируется с указанием меню для него

frame_button = Frame(root,width=100,heigh=100,bd=5)
frame_info = Frame(root,width=50,heigh=100,bd=5)
frame_txt = Frame(root,width=50,heigh=100,bd=5)

for ip in ip_list_all:
    text_comp[ip] = Label(frame_info, text=ip, font="Verdana 12")

text_command = Entry(frame_txt,width=30, font="Verdana 12")

for ip in ip_list_all:
    tex[ip] = Entry(frame_txt,width=6, font="Verdana 12")

ent = Entry(frame_button,width=40)

#but = Button(root)
#but["text"] = "ping" 
#but.bind("<Button-1>",printer)

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

# Конец
but99.pack()

for ip in ip_list_all:
    text_comp[ip].pack()

text_command.pack()

for ip in ip_list_all:
    tex[ip].pack()

ent.pack()

# Старт системы

print("Ping class")
text_command.insert(END, "Ping")

for ip in ip_list_all:
    threading.Thread(target=ping_class, args=[ip]).start()

ip_list = ip_list_all if len(ip_list) == 0 else ip_list

root.mainloop()



