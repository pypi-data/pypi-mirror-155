from cProfile import label
from tkinter import *
import tkinter
from tkinter.ttk import *
from time import strftime

def Calc():
    root = Tk()
    root.title("Clock")

    def time():
        string = strftime('%H:%M:%S %p')
        label.config(text = string)
        label.after(1000, time)

    label = Label(root, font=("sans-serif", 80), background = "black", foreground = "white")
    label.pack(anchor = 'center')
    time()

    mainloop()
Calc()