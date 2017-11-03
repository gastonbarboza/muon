import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#cargo archivos
listadedatos = list(os.walk("./interpol"))[0][2]
pmt2 = np.loadtxt("./interpol/"+listadedatos[0],delimiter=',')
print(listadedatos[0])
pmt1 = np.loadtxt("./interpol/"+listadedatos[1],delimiter=',')

#parametros para pmt1
y1 = 21.27975
A1 = 783197.61244
R1 = 97.72976
#intento calcularlos con scipy
y,A,R = curve_fit(lambda t,y,A,R: A*np.exp(R*t), pmt1[:,0],pmt1[:,1],p0 = [y1,A1,R1])[0]
print('Para A me da {} con Origin y {} con scipy'.format(A1,A))
print('Para R me da {} con Origin y {} con scipy'.format(R1,R))
print('Para y me da {} con Origin y {} con scipy'.format(y1,y))
#grafico
plt.plot(pmt1[:,0],pmt1[:,1],'-o',label='pmt 1',color='blue')
t = np.linspace(pmt1[:,0][0],pmt1[:,0][len(pmt1[:,0])-1],50)
plt.plot(t, y1 + A1*np.exp(R1*t),label='fit',color='green')
plt.plot(t, y+A*np.exp(R*t),label='scipy_fit',color='red')
plt.legend()
plt.show(block=False)

#creo nueva figura
plt.figure()
#parametros para pmt2
y2 = -.041866
A2 = 122846.14004
R2 = 134.89787
#Ahora con scipy
y,A,R = curve_fit(lambda t,y,A,R: A*np.exp(R*t), pmt2[:,0],pmt2[:,1],p0 = [y2,A2,R2])[0]
#grafico
plt.plot(pmt2[:,0],pmt2[:,1],'-o',label='datos 2')
t = np.linspace(pmt2[:,0][0],pmt2[:,0][len(pmt2[:,0])-1],50)
plt.plot(t, y2 + A2*np.exp(R2*t),label='fit')
plt.plot(t, y+A*np.exp(R*t),label='scipy_fit',color='red')
plt.legend()
plt.show()

