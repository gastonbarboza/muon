import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

listadedatos = list(os.walk("./interpol"))[0][2]
pmt1 = np.loadtxt("./interpol/"+listadedatos[0],delimiter=',')
pmt2 = np.loadtxt("./interpol/"+listadedatos[1],delimiter=',')
#plt.plot(-pmt1[:,0],pmt1[:,1],'-o',label='datos')
def fitFunc(t, a, b, c):
    return a*np.exp(-b*t) + c
t = np.linspace(-pmt1[:,0][0],-pmt1[:,0][len(-pmt1[:,0])-1],50)
temp = fitFunc(t, 2.5, 1.3, 0.5)
noisy = temp + 0.25*np.random.normal(size=len(temp))


fitParams, fitCovariances = curve_fit(fitFunc, -pmt1[:,0],noisy)

plt.plot(t, fitFunc(t, fitParams[0], fitParams[1], fitParams[2]))
plt.show()
input()
