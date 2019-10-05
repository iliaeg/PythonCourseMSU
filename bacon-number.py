# import pandas as pd
# import numpy as np
# import math
import sys
# import json
# from os import path
import tkinter as tk

from utils import eprint


def main(argv):
    '''
    Usage: python transaq.py config.json [-d]

    Args:
        config: path to json configuration file
        flag -d: print debug info
    '''

    try:

        # if (len(argv) < 2):
        #     eprint("Usage: python transaq.py config.json [-d]")
        #     return 1

        # if "-h" in argv or "--help" in argv:
        #     print("Usage: python bacon-number.py [-d]")
        #     return 0

        # config_file = path.abspath(argv[1])

        # if "-d" in argv:
        #     debug = True
        # else:
        #     debug = False

        # if not path.exists(config_file):
        #     raise FileNotFoundError(f"Configuration file {config_file} not found")
        # # read config
        # with open(config_file, "r") as read_file:
        #     config = json.load(read_file)

        # data_file = path.abspath(config['dataFileName'])
        # if not path.exists(data_file):
        #     raise FileNotFoundError(f"Data file {data_file} not found")

        
        # tkinter._test()

        def Hello(event):
            print("Yet another hello world")

        root = tk.Tk()

        btn = tk.Button(root,                  #родительское окно
             text="Click me",       #надпись на кнопке
             width=30,height=5,     #ширина и высота
             bg="white",fg="black") #цвет фона и надписи
        btn.bind("<Button-1>", Hello)       #при нажатии ЛКМ на кнопку вызывается функция Hello
        btn.pack()                          #расположить кнопку на главном окне
        root.mainloop()

        return 0

    except FileNotFoundError as ex:
        eprint("FileNotFoundError exception caught: \n", ex)
    except Exception as ex:
        eprint("An exception caught: ", ex)

    return 1

if __name__ == "__main__":
    main(sys.argv[:])