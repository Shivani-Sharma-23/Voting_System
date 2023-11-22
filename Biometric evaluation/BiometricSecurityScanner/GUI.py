#https://docs.python.org/2/library/tkinter.html
#https://docs.python.org/2/library/sqlite3.html
#https://pythonprogramming.net/change-show-new-frame-tkinter/


import tkinter as tk
#from PIL import ImageTk, Image
import os
import sys
import sqlite3
#import RPi.GPIO as GPIO
import time



LARGE_FONT= ("Verdana", 12)
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainMenu, OpenPage, PasswordPage,ManagePage,AddPage,DeletePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(MainMenu)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Main Menu", font=LARGE_FONT)
        label.pack(padx=5,pady=10)
        button = tk.Button(self, text="OPEN",
                           command=lambda: controller.show_frame(OpenPage))
        button.pack(padx=5,pady=20)
        button2 = tk.Button(self, text="Manage",
                            command=lambda: controller.show_frame(PasswordPage))
        button2.pack()


class OpenPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = tk.Label(self, text="OPEN LOCK PAGE", font=LARGE_FONT)
        label1.pack(pady=10,padx=10)
        #path = "fp.jpg"
        #img = ImageTk.PhotoImage(Image.open(path))
        #panel = tk.Label(window, image = img)

        button3 = tk.Button(self, text="Open Lock",
                            command=lambda: openlock())
        button3.pack(padx=5,pady=20)
        button4 = tk.Button(self, text="Fail Authorization",
                            command=lambda: led())
        button4.pack(padx=5,pady=20)
        button1 = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MainMenu))
        button1.pack(padx=5,pady=20)
	

class PasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="PASSWORD", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        entry = tk.Entry(self)
        entry.pack()
        
        button3 = tk.Button(self, text="OK",
                            command=lambda: checkpw(entry.get(),controller,tk))
        button3.pack(pady=5,padx=20)

        button1 = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MainMenu))
        button1.pack(padx=5,pady=20)
        


class ManagePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="MANAGE", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Menu",
                            command=lambda: controller.show_frame(MainMenu))

        button2 = tk.Button(self, text="Add User",
                            command=lambda: controller.show_frame(AddPage))
        button2.pack(pady=10,padx=10)
        button3 = tk.Button(self, text="Delete User",
                            command=lambda: controller.show_frame(DeletePage))
        button3.pack()
        button1.pack(padx=5,pady=20)
        

class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ADD PAGE", font=LARGE_FONT)
        label.pack(padx=5,pady=20)
        entry = tk.Entry(self)
        entry.pack()
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(ManagePage))
        
        #path = "fp.jpg"
        #img = ImageTk.PhotoImage(Image.open(path))
        #panel = tk.Label(window, image = img)
        #entry = tk.Entry(app,textvariable=ment)
        #entry.pack()

        button2 = tk.Button(self, text="ADD USER",
                            command=lambda: databaseadd(entry.get()))
        button2.pack(padx=5,pady=20)
        button1.pack(padx=5,pady=20)

        
class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="DELETE PAGE", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        

#        label2 = tk.Label(self, text = c, height = 5)
 #       label2.pack(pady=10,padx=10)

        entry = tk.Entry(self)
        entry.pack()
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(ManagePage))
        button2 = tk.Button(self, text="DELETE USER",
                            command=lambda: databasedelete(entry.get()))
        button2.pack(padx=5,pady=20)
        button1.pack(padx=5,pady=20)
        
def openlock():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31, GPIO.OUT)
    GPIO.output(31, True)
    time.sleep(2)
    GPIO.output(31, False)
    GPIO.cleanup()

def led():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.OUT)
    GPIO.output(29, True)
    time.sleep(1)
    GPIO.output(29, False)
    time.sleep(1)
    GPIO.output(29, True)
    time.sleep(1)
    GPIO.output(29, False)
    GPIO.cleanup() 

    
def databaseadd(s):
                            
    pw = "b"
    pw = input('Enter address path: ')
    cur = conn.cursor()
    cur.execute("INSERT INTO FINGER VALUES(?,?)",[s,pw])

    conn.commit()
    cur.execute("SELECT * FROM FINGER")
    print(cur.fetchall())

def checkpw(s,controller,tk):
 
    if s == correctpw:
        checker = 1
        controller.show_frame(ManagePage)
    else:
        checker = 0
        tk.messagebox.showerror("Error","Incorrect Password")
       

        
def databasedelete(s):

    cur = conn.cursor()

    cur.execute("DELETE FROM FINGER WHERE Name =?",[s])

    conn.commit()
    cur.execute("SELECT * FROM FINGER")
    print(cur.fetchall())

def incorrectPW(tk):
    tk.messagebox.showerror("Error","Incorrect Password")
        
conn = sqlite3.connect('finger.db')
cur = conn.cursor()
cur.execute("SELECT * FROM FINGER")
c = "c"
c = cur.fetchall()
print(c)

correctpw = "ohio"
checker = 0
app = GUI()
app.title("Fingerprint")
app.geometry("280x300")

app.mainloop()
