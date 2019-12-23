import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
# from tkinter import *

m=398.6005e12
H = 400e3
Re = 6371e3
r = H+Re
# t1=1
period = 2*math.pi*(r**3/m)**0.5
r_0 = [r, 0,0]
v_0 = (m/np.linalg.norm(r_0))**(1/2)
x_0, y_0, z_0 = r_0
v_x_0, v_y_0, v_z_0, = 0, v_0, 0
F0 = np.array([x_0, y_0, z_0, v_x_0, v_y_0, v_z_0])

def f(F, t):
        x, y, z = F[0], F[1], F[2]
        v_x, v_y, v_z = F[3], F[4], F[5]
        r = [x,y,z]
        return [
            v_x,
            v_y,
            v_z,
            -m*(x)/((np.linalg.norm(r))**3),
            -m*y/((np.linalg.norm(r))**3),
            -m*z/((np.linalg.norm(r))**3)
            ]

a_vozm = 5e-1
def f1(F, t):
        x, y, z = F[0], F[1], F[2]
        v_x, v_y, v_z = F[3], F[4], F[5]
        r = np.array([x, y, z])
        # print(f"{-m*(y)/((np.linalg.norm([x,y,z]))**3):.5f} : {-m*(y)/((np.linalg.norm([x,y,z]))**3) - 4e-10:.5f}")
        return [
            v_x,
            v_y,
            v_z,
            -(m*(x)/((np.linalg.norm(r))**3)) - a_vozm*math.cos(math.atan(y/(x+0.0001))) if x > 0 \
                else  -(m*(x)/((np.linalg.norm(r))**3)) + a_vozm*math.cos(math.atan(y/(x+0.0001))),
            -(m*(y)/((np.linalg.norm(r))**3)) - a_vozm*math.sin(math.atan(y/(x+0.0001))) if y > 0 \
                else -(m*(y)/((np.linalg.norm(r))**3)) + a_vozm*math.sin(math.atan(y/(x+0.0001))),
            -m*(z)/((np.linalg.norm(r))**3)
            ]

t = np.arange(0,period*6)
soln = odeint(f, F0, t).T
soln1 = odeint(f1, F0, t).T
X, Y, Z = soln[0], soln[1], soln[2]
X1, Y1, Z1 = soln1[0], soln1[1], soln1[2]

# fig = plt.figure(1, figsize=(8,7))

# ax = fig.add_subplot(211, projection="3d")
# ax.set_xlabel("x")
# ax.set_ylabel("y")
# ax.set_zlabel("z")
# ax.set_xlim(-8e6, 8e6)
# ax.set_ylim(-8e6, 8e6)
# # ax.set_zlim(-8e6, 8e6)

# ax2=fig.add_subplot(212, projection="3d")
# ax2.set_xlabel("x")
# ax2.set_ylabel("y")
# ax2.set_zlabel("z")
# ax2.set_xlim(-7e6, 7e6)
# ax2.set_ylim(-7e6, 7e6)
# # ax2.set_zlim(-8e1, 8e1)


# ax.scatter(0, 0, 0, s=500, zorder=1)
# ax.plot(X, Y, Z, color='blue', zorder=2)

# ax2.scatter(0, 0, 0, s=500, zorder=1)
# ax2.plot(X1, Y1, Z1, color='red', zorder=2)


def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
        # line.set_marker("o")
    return lines

# Attaching 3D axis to the figure
fig = plt.figure(1, figsize=(8,7))
ax = fig.add_subplot(111, projection="3d")

data = np.array([[X,Y,Z],[X1,Y1,Z1]])

lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]


ax.set_xlim(-8e6, 8e6)
ax.set_ylim(-8e6, 8e6)
# ax.set_zlim(-8e6, 8e6)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

line_ani = animation.FuncAnimation(fig, update_lines, t.size, fargs=(data, lines),
    interval=1, blit=True, repeat=True)


ax.scatter(0, 0, 0, s=500, zorder=1)

plt.show()