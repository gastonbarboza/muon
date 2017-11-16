import time
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

listadedatos = sorted(list(os.walk("./graficar/"))[0][2])
nroarchivos = len(listadedatos)
listadedatos1 = listadedatos[1:8]
listadedatos2 = listadedatos[9:16]

datos1 = np.loadtxt("./graficar/" + listadedatos[0],delimiter=',')
for datito in listadedatos1:
    datos1 = [x + y for x,y in zip(datos1,np.loadtxt("./graficar/" + datito,delimiter=','))]

datos2 = np.loadtxt("./graficar/" + listadedatos[8],delimiter=',')
for datito in listadedatos2:
    datos2 = [x + y for x,y in zip(datos2,np.loadtxt("./graficar/" + datito,delimiter=','))]

datos = [np.matrix(datos1),np.matrix(datos2)]

for index,dato in enumerate(datos):
    etiqueta=input("Leyenda para la placa {}? ".format(index+1))
    colorcito=input("Color? ")
    escala = float(input("Multiplico por? "))
    plt.plot(-dato[:,0],dato[:,1]*escala,'-o',label=etiqueta,color=colorcito,)
plt.legend()
plt.grid()
nombre = input('Título del gráfico? ')
plt.title(nombre)
plt.xlabel(input('x label? '))
plt.ylabel(input('y label?'))
plt.savefig(nombre + time.strftime('%H%M') + ".jpg",dpi=300)
plt.show()
