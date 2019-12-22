import numpy as np
# from math import pi, cos
import math
import matplotlib
from scipy.integrate import odeint

mu = 398.6005*(10**12)
r_x_0 = 1000
r_y_0 = 1
r_z_0 = 1

def pend(y_0, t, r_x_0, r_y_0, r_z_0, v_x_0, v_y_0, v_z_0, mu):
    r_x = r_x_0
    r_y = r_y_0
    r_z = r_z_0
    v_x = v_x_0
    v_y = v_y_0
    v_z = v_z_0
    ddt = [
        v_x,
        v_y,
        v_z,
        -mu*r_x/np.linalg.norm(r_x)**3,
        -mu*r_y/np.linalg.norm(r_y)**3,
        -mu*r_z/np.linalg.norm(r_z)**3
        ]
    return ddt

def speed(r_0, mu):
    return math.sqrt(mu/np.linalg.norm(r_0))

t = np.linspace(1, 10, 101)

y_0 = [r_x_0,r_y_0,r_z_0,speed(r_x_0, mu),speed(r_y_0, mu),speed(r_z_0, mu)]
sol = odeint(pend, y_0, t, \
    args=(
        r_x_0,
        r_y_0,
        r_z_0,
        speed(r_x_0, mu),
        speed(r_y_0, mu),
        speed(r_z_0, mu),
        mu
    ))

import matplotlib.pyplot as plt
plt.plot(t, sol[:, 0], 'b', label='r(t)')
plt.plot(t, sol[:, 1], 'g', label='v(t)')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()