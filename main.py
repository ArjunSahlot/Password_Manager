#
#  Password manager
#  A password manager built with tkinter.
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from tkinter import *
from tkinter import messagebox
import tkinter.messagebox
import os, pickle

objects = []
window = Tk()
window.withdraw()
window.title('Email Storage')

access = None


class Password:
    def __init__(self, text):
        self.text = text


class PopupWindow:
    attempts = 0

    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title('Input Password')
        top.geometry('{}x{}'.format(250, 100))
        top.resizable(width=False, height=False)
        self.l = Label(top, text=" Password: ", font=('Courier', 14), justify=CENTER)
        self.l.pack()
        self.e = Entry(top, show='*', width=30)
        self.e.pack(pady=7)
        self.b = Button(top, text='Submit', command=self.cleanup, font=('Courier', 14))
        self.b.pack()

    def cleanup(self):
        value = self.e.get()

        if value == access:
            self.top.destroy()
            window.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                window.quit()
            self.e.delete(0, 'end')
            messagebox.showerror('Incorrect Password',
                                 'Incorrect password, attempts remaining: ' + str(5 - self.attempts))


class EntityAdd:
    def __init__(self, master, n, p, e):
        self.password = p
        self.name = n
        self.email = e
        self.window = master

    def write(self):
        f = open('info.txt', "a")
        n = self.name
        e = self.email
        p = self.password

        encryptedN = ""
        encryptedE = ""
        encryptedP = ""
        for letter in n:
            if letter == ' ':
                encryptedN += ' '
            else:
                encryptedN += chr(ord(letter) + 5)

        for letter in e:
            if letter == ' ':
                encryptedE += ' '
            else:
                encryptedE += chr(ord(letter) + 5)

        for letter in p:
            if letter == ' ':
                encryptedP += ' '
            else:
                encryptedP += chr(ord(letter) + 5)

        f.write(encryptedN + ',' + encryptedE + ',' + encryptedP + ', \n')
        f.close()


class EntityDisplay:
    def __init__(self, master, n, e, p, i):
        self.password = p
        self.name = n
        self.email = e
        self.window = master
        self.i = i

        dencrypted_n = ""
        dencrypted_e = ""
        dencrypted_p = ""
        for letter in self.name:
            if letter == ' ':
                dencrypted_n += ' '
            else:
                dencrypted_n += chr(ord(letter) - 5)

        for letter in self.email:
            if letter == ' ':
                dencrypted_e += ' '
            else:
                dencrypted_e += chr(ord(letter) - 5)

        for letter in self.password:
            if letter == ' ':
                dencrypted_p += ' '
            else:
                dencrypted_p += chr(ord(letter) - 5)

        self.label_name = Label(self.window, text=dencrypted_n, font=('Courier', 14))
        self.label_email = Label(self.window, text=dencrypted_e, font=('Courier', 14))
        self.label_pass = Label(self.window, text=dencrypted_p, font=('Courier', 14))
        self.delete_button = Button(self.window, text='X', fg='red', command=self.delete)

    def display(self):
        self.label_name.grid(row=6 + self.i, sticky=W)
        self.label_email.grid(row=6 + self.i, column=1)
        self.label_pass.grid(row=6 + self.i, column=2, sticky=E)
        self.delete_button.grid(row=6 + self.i, column=3, sticky=E)

    def delete(self):
        answer = tkinter.messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?')

        if answer == 'yes':
            for i in objects:
                i.destroy()

            f2 = open('info.txt', 'r')
            lines = f.readlines()
            f2.close()

            f2 = open('info.txt', "w")
            count = 0

            for line in lines:
                if count != self.i:
                    f.write(line)
                    count += 1

            f2.close()
            read_file()

    def destroy(self):
        self.label_name.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.delete_button.destroy()


if not os.path.isfile(os.path.join(os.path.dirname(__file__), "info.txt")):
    with open(os.path.join(os.path.dirname(__file__), "info.txt"), "w") as f1:
        f1.write("")


if not os.path.isfile(os.path.join(os.path.dirname(__file__), "master.txt")):
    with open(os.path.join(os.path.dirname(__file__), "master.txt"), "wb") as f1:
        master_pwd = input("To create a new master password delete the master.txt file\nNew master password: ")
        pickle.dump(Password(master_pwd), f1)
        access = master_pwd

else:
    access = pickle.load(open("master.txt", "rb")).text


def on_submit():
    m = email.get()
    p = password.get()
    n = name.get()
    e = EntityAdd(window, n, p, m)
    e.write()
    name.delete(0, 'end')
    email.delete(0, 'end')
    password.delete(0, 'end')
    messagebox.showinfo('Added Entity', 'Successfully Added, \n' + 'Name: ' + n + '\nEmail: ' + m + '\nPassword: ' + p)
    read_file()


def clear_file():
    f3 = open('info.txt', "w")
    f3.close()


def read_file():
    f3 = open('info.txt', 'r')
    count = 0

    for line in f3:
        entity_list = line.split(',')
        e = EntityDisplay(window, entity_list[0], entity_list[1], entity_list[2], count)
        objects.append(e)
        e.display()
        count += 1
    f3.close()


m = PopupWindow(window)

entity_label = Label(window, text='Add Entity', font=('Courier', 18))
name_label = Label(window, text='Name: ', font=('Courier', 14))
email_label = Label(window, text='Email: ', font=('Courier', 14))
pass_label = Label(window, text='Password: ', font=('Courier', 14))
name = Entry(window, font=('Courier', 14))
email = Entry(window, font=('Courier', 14))
password = Entry(window, show='*', font=('Courier', 14))
submit = Button(window, text='Add Email', command=on_submit, font=('Courier', 14))

entity_label.grid(columnspan=3, row=0)
name_label.grid(row=1, sticky=E, padx=3)
email_label.grid(row=2, sticky=E, padx=3)
pass_label.grid(row=3, sticky=E, padx=3)

name.grid(columnspan=3, row=1, column=1, padx=2, pady=2, sticky=W)
email.grid(columnspan=3, row=2, column=1, padx=2, pady=2, sticky=W)
password.grid(columnspan=3, row=3, column=1, padx=2, pady=2, sticky=W)

submit.grid(columnspan=3, pady=4)

name_label2 = Label(window, text='Name: ', font=('Courier', 14))
email_label2 = Label(window, text='Email: ', font=('Courier', 14))
pass_label2 = Label(window, text='Password: ', font=('Courier', 14))

name_label2.grid(row=5)
email_label2.grid(row=5, column=1)
pass_label2.grid(row=5, column=2)

read_file()

window.mainloop()
