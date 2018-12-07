import time
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

#File management
os.chdir(os.path.dirname(os.path.abspath(__file__))) #setea bien el directorio
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
os.mkdir(pathname) if not(os.path.isdir(pathname)) else print('ok')

#Crea lista de datos de directorio
listadedatos = sorted(list(os.walk("./graficar/"))[0][2])
nroarchivos = len(listadedatos)
cantidadporserie = nroarchivos//int(sys.argv[1]) #hay que pasarle 1 o 2
'''
#Carga primer serie de datos
listadedatos1 = listadedatos[0:cantidadporserie]
datos1 = np.loadtxt("./graficar/" + listadedatos1.pop(0),delimiter=',')
for datito in listadedatos1:
    datos1 = [x + y for x,y in zip(datos1,np.loadtxt("./graficar/" + datito,delimiter=','))]
'''

#Carga las series de datos
datos=[]
for nroserie in range(int(sys.argv[1])):
    listadedatos2 = listadedatos[nroserie*cantidadporserie:(nroserie+1)*cantidadporserie]#[cantidadporserie + 1:nroarchivos]
    print(listadedatos2)
    datos2 = np.loadtxt("./graficar/" + listadedatos2.pop(0),delimiter=',')
    for datito in listadedatos2:
        datos2 = [x + y for x,y in zip(datos2,np.loadtxt("./graficar/" + datito,delimiter=','))]
    datos.append(np.matrix(datos2)/cantidadporserie)#= [np.matrix(datos1)/cantidadporserie,np.matrix(datos2)/cantidadporserie]

#Grafica formatea y guarda
for index,dato in enumerate(datos):
    etiqueta=input("Leyenda para la serie {}? ".format(index+1))
    colorcito=input("Color? ")
    escalay = float(input("Multiplico eje y por? "))/60
    escalax = float(input("Multiplico eje x por? "))
    plt.plot(dato[:,0]*escalax,dato[:,1]*escalay,'-o',label=etiqueta,color=colorcito,)
    if input("Escala logaritmica? y/n ")=="y":
        plt.xscale('log')
        plt.yscale('log')
plt.legend()
plt.grid()
nombre = input('Título del gráfico? ')
plt.title(nombre)
plt.xlabel(input('x label? '))
plt.ylabel(input('y label? '))
plt.savefig(pathname + nombre + time.strftime('%H%M') + ".jpg",dpi=300)
plt.show()
