import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#cargo archivos
listadedatos = list(os.walk("./interpol"))[0][2]
pmt1 = np.loadtxt("./interpol/"+listadedatos[0],delimiter=',')
pmt2 = np.loadtxt("./interpol/"+listadedatos[1],delimiter=',')

#parametros para pmt1
y1 = -.041866
A1 = 122846.14004
R1 = 134.89787
#grafico
plt.plot(pmt1[:,0],pmt1[:,1],'-o',label='datos')
t = np.linspace(pmt1[:,0][0],pmt1[:,0][len(-pmt1[:,0])-1],50)
plt.plot(t, y1 + A1*np.exp(R1*t),label='fit')
plt.legend()
plt.show()

#creo nueva figura
plt.figure()
#parametros para mt2
y2 = 21.27975
A2 = 783197.61244
R2 = 97.72976
#grafico
plt.plot(pmt2[:,0],pmt2[:,1],'-o',label='datos')
t = np.linspace(pmt2[:,0][0],pmt2[:,0][len(-pmt2[:,0])-1],50)
plt.plot(t, y2 + A2*np.exp(R2*t),label='fit')
plt.legend()
plt.show()
