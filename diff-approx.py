import numpy as np
from math import pi, cos
import matplotlib
from matplotlib.animation import FuncAnimation
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter.ttk import Frame


global canvas, fig, ax, Window, n, d, nt, dt_entry

def F(u, t):
    return np.sin(0.1*u+t)

N = 1001 # must be odd, segmentation for x
S = 3 # number of iteratioins on layer
NT = 2510
dt = 0.01
D = 0.04
z = []

figsize_x = 6
figsize_y = 4

def calculate_z():
    global z, S, N, D, NT, dt 

    x = np.linspace(0,2*pi,N)
    u0 = np.sin(10*x)
    fu = np.fft.fft(u0)
    u = u0
    z = np.empty((NT,N), dtype=float)
    h= 2*pi/N

    l = np.empty(N)
    for k in range(N//2+1):
        l[k] = 2*D/(h**2) * (1 - cos(k*h/2))
        l[-k] = l[k]

    for t in range(1, NT):
        us = u
        fus = fu

        for s in range(S):
            F1 = F(u, (t-1)*dt)
            F2 = F(us, t*dt)

            f = np.fft.fft(F1+F2)

            fus = ((2-dt*l)*fu + dt*f)/(2 + dt*l)
            us = np.fft.ifft(fus)
        u = us
        fu = fus
        z[t] = np.real(us)


z_calculated = False

def get_const():
    global N, D, NT, dt, n, d, nt, dt_entry, z_calculated
    N_cur = int(n.get())
    D_cur = float(d.get())
    NT_cur = int(nt.get())
    dt_cur = float(dt_entry.get())

    eps = 0.0001

    if N != N_cur \
        or NT != NT_cur \
        or abs(D - D_cur) > eps \
        or abs(dt - dt_cur) > eps:

        z_calculated = False
    
    N = N_cur
    D = D_cur
    NT = NT_cur
    dt = dt_cur


def heatmap_plot():
    global z_calculated, canvas, fig, ax, Window, N, D, NT, dt, figsize_x, figsize_y

    get_const()

    if not z_calculated:
        calculate_z()

    # plot
    fig = Figure(figsize=(figsize_x, figsize_y), dpi=100)
    ax = fig.add_subplot(111)

    im = ax.imshow(z.transpose())
    fig.colorbar(im)

    canvas = FigureCanvasTkAgg(fig, Window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="E"+"W"+"S"+"N")

def animate_plot():
    global z_calculated, canvas, fig, ax, N, D, NT, dt, figsize_x, figsize_y

    get_const()

    if not z_calculated:
        calculate_z()
        z_calculated = True

    # plot
    test = False

    fig = Figure(figsize=(figsize_x, figsize_y), dpi=100)
    ax = fig.add_subplot(111)

    frame_width = 500
    if not test:
        ax.set_xlim(0, frame_width)
        ax.set_ylim(-3, 3)
        # ax = plt.axes(xlim=(0, frame_width), ylim=(-3, 3))
    else:
        ax.set_xlim(-100, NT+100)
        ax.set_ylim(-3, 3)
        # ax = plt.axes(xlim=(-100, NT+100), ylim=(-3, 3))
    line, = ax.plot([], [], lw=3)

    def init():
        line.set_data([], [])
        return line,

    z_T = z.transpose()

    def animate(i):
        if not test:
            x = np.linspace(0-i, NT-i, NT)
        else:
            x = np.linspace(0, NT, NT) # NT points in [0, NT]

        y = z_T[len(z_T) // 2]

        line.set_data(x,y)
        return line,

    frames_of_NT_to_show = 1897

    canvas = FigureCanvasTkAgg(fig, Window)
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="E"+"W"+"S"+"N")

    anim = FuncAnimation(fig, animate, init_func=init,
                                frames=frames_of_NT_to_show, interval=10, blit=True)

class MainWindow(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        global canvas, fig, ax, Window, figsize_x, figsize_y, n, d, nt, dt_entry
        Window = self

        self.rowconfigure(0, pad=5)
        self.rowconfigure(1, pad=5)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=4)

        self.master.title("Diffusion Equation")
        self.pack(fill=BOTH, expand=True)

        n_lbl = Label(self, text="N :")
        n_lbl.grid(row=0, column=0, sticky="E")
        n = Entry(self)
        n.insert(0, N)
        n.grid(row=0, column=1, sticky="W")
        d_lbl = Label(self, text="D :")
        d_lbl.grid(row=1, column=0, sticky="E")
        d = Entry(self)
        d.insert(0, D)
        d.grid(row=1, column=1, sticky="W")

        nt_lbl = Label(self, text="NT :")
        nt_lbl.grid(row=0, column=2, sticky="E")
        nt = Entry(self)
        nt.insert(0, NT)
        nt.grid(row=0, column=3, sticky="W")
        dt_lbl = Label(self, text="dt :")
        dt_lbl.grid(row=1, column=2, sticky="E")
        dt_entry = Entry(self)
        dt_entry.insert(0, dt)
        dt_entry.grid(row=1, column=3, sticky="W")

        heatmap_btn = Button(self, text="heatmap", command=heatmap_plot)
        heatmap_btn.grid(row=0, column=4, padx=15, sticky="W"+"E")
        # heatmap_btn.bind("<Button-1>", heatmap_plot)
        animate_btn = Button(self, text="animate", command=animate_plot)
        animate_btn.grid(row=1, column=4, padx=15, sticky="W"+"E")
        # animate_btn.bind("<Button-1>", animate_plot)

        fig = Figure(figsize=(figsize_x, figsize_y), dpi=100)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="E"+"W"+"S"+"N")
        
# win = Elements()

def main(argv):
    try:

        root = Tk()
        app = MainWindow()
        root.mainloop()

        return 0

    except Exception as ex:
        print("An exception caught: ", ex)
        raise ex

    return 1

if __name__ == "__main__":
    main(sys.argv[:])