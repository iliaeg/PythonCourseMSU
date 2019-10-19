# import pandas as pd
# import numpy as np
# import math
import sys
# import json
# from os import path
from tkinter import *
from tkinter.ttk import Frame#, Button, Label, Style

from utils import eprint

global data_lbl, filename, select_btn, load_btn, select_lbl, dropbox, \
    number_lbl, bacon_number, path_from, path

actors = []

def load_file(event):
    # print(event)
    print(f"file has been loaded {filename.get()}")
    filename.delete(0, END)
    filename.insert(0, "Insert string")
    path.insert(1.0, "adaasd ad")

class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        global data_lbl, filename, select_btn, load_btn, select_lbl, dropbox, \
            number_lbl, bacon_number, path_from, path

        self.master.title("Bacon Number")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        data_lbl = Label(self, text="Data file")
        data_lbl.grid(row=0, column=0, columnspan=2)
        filename = Entry(self)
        filename.grid(row=1, column=0, columnspan=2)
        select_btn = Button(self, text="Select")
        select_btn.grid(row=2, column=0)
        load_btn = Button(self, text="Load")
        load_btn.grid(row=2, column=1)
        load_btn.bind("<Button-1>", load_file)

        select_lbl = Label(self, text="Select actor")
        select_lbl.grid(row=0, column=2, columnspan=2)
        # variable = StringVar()
        # variable.set(actors[0])
        # *actors
        dropbox = OptionMenu(self, StringVar(), None)
        dropbox.grid(row=1, column=2, columnspan=2)

        number_lbl = Label(self, text="Bacon number:")
        number_lbl.grid(row=3, column=0, columnspan=2)
        bacon_number = Label(self, text="num")
        bacon_number.grid(row=3, column=2, columnspan=2)
        path_from = Label(self, text="path from .. to ..")
        path_from.grid(row=4, column=0, columnspan=4)
        path = Text(self)
        path.grid(row=5, column=0, columnspan=4, padx=5, sticky=E+W+S+N)

        # print(type(data_lbl))
        # print(type(filename))
        # print(type(select_btn))
        # print(type(dropbox))
        # print(type(path))
        
# win = Elements()

def main(argv):
    try:

        root = Tk()
        root.geometry("350x300+300+300")
        MainWindow()
        root.mainloop()

        return 0

    except FileNotFoundError as ex:
        eprint("FileNotFoundError exception caught: \n", ex)
    except Exception as ex:
        eprint("An exception caught: ", ex)

    return 1

if __name__ == "__main__":
    main(sys.argv[:])