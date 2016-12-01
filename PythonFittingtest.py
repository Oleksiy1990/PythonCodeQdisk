import numpy as np 
import scipy as sp 


import matplotlib.pyplot as plt 
import numpy.random as rnd 


x = np.linspace(-2*np.pi, 2*np.pi, 128, endpoint=True)
r = 0.2*rnd.ranf(len(x))
C, S = np.cos(x)+r, np.sin(x)+r

A, k = 1, 1
def residuals(p, y, x):
    A, k, offset= p
    err = y - (A * np.sin(2 * np.pi * k * x) + offset)
    return err



def peval(x, p):
    return p[0] * np.sin(2 * np.pi * p[1] * x) + p[2]    

p0 = [2,  0.2, 0.1]

from scipy.optimize import leastsq
plsq = leastsq(residuals, p0, args=(S, x))
print(plsq[0])



plt.plot(x, peval(x, plsq[0]),x, S,'o')

plt.show()
