from tkinter import *
root = Tk()
def firstFarme():
    f=Frame(root)
    global f
    f.pack()
    b=Button(f, text='first page',command=second)
    b.pack()
def secondFarme():
    v=Frame(root)
    global v
    v.pack()
    bt=Button(v, text='second page', command=first)
    bt.pack()
def second(event=None):
    f.destroy()
    

