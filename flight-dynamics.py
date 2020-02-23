import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

A = 65 # any from 0 to 100
B = A
C = 15 # any from 0 to 100
K = 1

p_0, q_0, r_0 = [0.01, 0.01, 0.01]
F0 = np.array([p_0, q_0, r_0])

def f(F, t):
        p, q, r = F[0], F[1], F[2]
        return [
            (1-C/A)*q*r,
            (C/A-1)*p*q,
            0
            ]

t = np.arange(0, 1000, 1)
soln = odeint(f, F0, t).T
P, Q, R = soln[0], soln[1], soln[2]


#plot

fig = plt.figure(1, figsize=(8,7))

ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
# ax.set_xlim(-8e6, 8e6)
# ax.set_ylim(-8e6, 8e6)
# ax.set_zlim(-8e6, 8e6)

ax.plot(P, Q, R, color='blue', zorder=2)



coefs = ((A/K)**2, (B/K)**2, (C/K)**2)  # Coefficients in a0/c x**2 + a1/c y**2 + a2/c z**2 = 1 
# Radii corresponding to the coefficients:
rx, ry, rz = 1/np.sqrt(coefs)

# Set of all spherical angles:
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

# Cartesian coordinates that correspond to the spherical angles:
# (this is the equation of an ellipsoid):
x = rx * np.outer(np.cos(u), np.sin(v))
y = ry * np.outer(np.sin(u), np.sin(v))
z = rz * np.outer(np.ones_like(u), np.cos(v))

# Plot:
ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='gray', alpha=0.5)

plt.show()