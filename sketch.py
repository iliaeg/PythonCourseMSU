import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math
import numpy.linalg as lin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from tkinter import *

# def clicked():
#     try:
#         Amplituda = int(txt_N.get())
#         Period = int(txt_NT.get())
#         Visota = float(txt_dt.get())
#     except:
#         return
#     x = np.linspace(0, 2 * pi, N)

m=398.6005e12
H = 400e3
Re = 6371e3
r = H+Re
# t1=1
period = 2*math.pi*(r**3/m)**0.5
r0 = [r, 0,0]
v0 = (m/lin.norm(r0))**(1/2)
x0, y0, z0 = r0
vx0, vy0, vz0, = 0, v0, 0
F0 = np.array([x0, y0, z0, vx0, vy0, vz0])
def f(F, t,params):
        x, y, z = F[0], F[1], F[2]
        vx, vy, vz = F[3], F[4], F[5]
        r = [x,y,z]
        return [vx, vy, vz,-m*(x)/((lin.norm(r))**3),-m*y/((lin.norm(r))**3),-m*z/((lin.norm(r))**3)]
def f1(F, t,params):
        x, y, z = F[0], F[1], 0#F[2]
        vx, vy, vz = F[3], F[4], F[5]
        r = [x,y,z]
        #for n in range(10):
            #c=(n/np.math.factorial(n))*np.sin(1)
            #print(c)
        # print(z)
        # print(f"{-m*(y)/((lin.norm([x,y,z]))**3):.5f} : {-m*(y)/((lin.norm([x,y,z]))**3) - 4e-10:.5f}")
        # print(lin.norm([x,y,z]))
        return [vx, vy, vz,-m*(x)/((lin.norm(r))**3),-m*(y)/((lin.norm(r))**3) + 4e-2,-m*(z*3*np.sin(1))/((lin.norm(r))**3)+8]

t = np.arange(0,period*4, 0.01)#l5,60)
psoln = odeint(f, F0, t, args=(m,)).T
psoln1 = odeint(f1, F0, t, args=(m,)).T
X, Y, Z = psoln[0], psoln[1], psoln[2]
# move nevozmushenniy down
Z -= 8e5
X1, Y1, Z1 = psoln1[0], psoln1[1], psoln1[2]
    # print(psoln)
    #plt.plot(psoln[:, 0],psoln[:, 1])
    #plt.grid(True)
    #plt.show()

fig = plt.figure(1, figsize=(8,7))

ax=fig.add_subplot(211)#,projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
# ax.set_zlabel("z")
ax.set_xlim(-8e6, 8e6)
ax.set_ylim(-8e6, 8e6)

ax2=fig.add_subplot(212)
ax2.set_xlabel("x")
ax2.set_ylabel("y")
# ax.set_zlabel("z")
ax2.set_xlim(-8e6, 8e6)
ax2.set_ylim(-8e6, 8e6)

# ax.set_zlim(-8e6, 8e6)
    # xxx=np.arange(-8e5, 8e5, 1e3)
    # yyy=np.arange(-8e5, 8e5, 1e3)
    # zzz=np.arange(-8e5, 8e5, 1e3)
    # xxx, yyy, zzz = np.meshgrid(xxx, yyy, zzz)
#, Z, color='blue')
ax.plot(X, Y, color='blue')
ax2.plot(X1, Y1, color='red')#, Z1, color='red')
plt.show()

# root = Tk()
# root.configure(bg='#E8ADAA')
# root.title("Space orbit")
# root.geometry("370x300")
# lbl_fun = Label(root, text = "Function of disturbance")
# lbl_fun.place(x=5, y=25)
# lbl_fun.configure(bg='#E8ADAA')
# txt_fun = Entry(root, width = 20)
# txt_fun.place(x=170, y=25)
# lbl_D = Label(root, text = "Amplituda")
# lbl_D.place(x=5, y=50)
# lbl_D.configure(bg='#E8ADAA')
# txt_D = Entry(root, width = 20)
# txt_D.place(x=170, y=50)
# lbl_N = Label(root, text = "Period")
# lbl_N.place(x=5, y=75)
# lbl_N.configure(bg='#E8ADAA')
# txt_N = Entry(root, width = 20)
# txt_N.place(x=170, y=75)
# lbl_dt = Label(root, text = "Visota of orbit")
# lbl_dt.place(x=5, y=100)
# lbl_dt.configure(bg='#E8ADAA')
# txt_dt = Entry(root, width = 20)
# txt_dt.place(x=170, y=100)
# lbl_NT = Label(root, text = "")
# lbl_NT.place(x=5, y=125)
# lbl_NT.configure(bg='#E8ADAA')
# btn = Button(root, text = "Run!", command = clicked, bg = "#F778A1")
# btn.place(x=150, y=200)
# root.mainloop()