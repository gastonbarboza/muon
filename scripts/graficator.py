import time
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

listadedatos = list(os.walk("./graficar/"))[0][2]
print(listadedatos)
for grafico in listadedatos:
    dato = np.loadtxt("./graficar/" + grafico,delimiter=',')
    etiqueta=input("Leyenda para {}? ".format(grafico))
    colorcito=input("Color? ")
    escala = float(input("Multiplico por? "))
    plt.plot(-dato[:,0],dato[:,1]*escala,'-o',label=etiqueta,color=colorcito,)
plt.legend()
plt.grid()
nombre = input('nombre? ')
plt.title(nombre)
plt.xlabel("Thresholds")
plt.ylabel("Rate")
plt.savefig(nombre + ".jpg",dpi=300)
plt.show()
