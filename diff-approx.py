# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import math
from math import pi
import sys
# import json
# from os import path
from tkinter import *
from tkinter.ttk import Frame#, Button, Label, Style

# from utils import eprint

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

        # root = Tk()
        # root.geometry("350x300+300+300")
        # MainWindow()
        # root.mainloop()

        def F(u,t):
            return np.sin(0,1 * u + t)

        N = 11 # must be odd, segmentation for x
        S = 3 # number of iteratioins on layer
        D = 0.3 # diffusion
        dt = 0.1
        NT = 10

        x = np.linspace(0, 2*pi, N)
        u_0 = np.sin(5*x)
        f_u = np.fft.fft(u_0)
        u = u_0
        h = 2*pi/N
        l = np.empty(N)


        for k in range(N//2+1):
            l[k] = 4*D/h**2*np.sin(k*h/4)**2 # lambda
            l[-k] = l[k]

        for t in range(NT):
            u_s = u
            f_u_s = f_u
            
            for s in range(S):
                F_1 = F(u, (t-1)*dt)
                F_2 = F(u_s, t*dt)
                f = np.fft.fft(F_1 + F_2)

                # l = np.append(l, 4*D/h**2*np.sin(s*h/4)**2) # lambda

                f_u_s = ((2-dt*l)*f_u + dt*f)/(2+dt*l)
                u_s = np.fft.ifft(f_u_s)
            z = np.real(u_s)
            u = u_s
            f_u = f_u_s

        print(z)

        # plt.imshow(z)
        plt.plot(z)
        data = [z]

        fig, ax = plt.subplots()
        im = ax.imshow(data)#, cmap=plt.get_cmap('hot'), interpolation='nearest', vmin=0, vmax=1)
        fig.colorbar(im)
        plt.show()


        return 0

    except FileNotFoundError as ex:
        print("FileNotFoundError exception caught: \n", ex)
    except Exception as ex:
        print("An exception caught: ", ex)
        raise ex

    return 1

if __name__ == "__main__":
    main(sys.argv[:])