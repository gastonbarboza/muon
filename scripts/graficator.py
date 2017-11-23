import numpy as np
import os
import sys
import matplotlib.pyplot as plt

#File management
os.chdir(os.path.dirname(sys.argv[0])) #setea bien el directorio
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
os.mkdir(pathname) if not(os.path.isdir(pathname)) else pass

listadedatos = list(os.walk("./graficar/"))[0][2]

print(listadedatos)
suma = []
for index,grafico in enumerate(listadedatos):
    dato = np.loadtxt("./graficar/" + grafico,delimiter=',')
    #etiqueta=input("Leyenda para {}? ".format(grafico))
    #colorcito=input("Color? ")
    #escala = float(input("Multiplico por? "))
    suma.append(dato[0,1])
print(suma)
sys.exit()
plt.scatter(index,suma)#,'-o',label=etiqueta,color=colorcito,) #-dato[:,0]
plt.legend()
plt.grid()
nombre = input('nombre? ')
plt.title(nombre)
plt.xlabel("Thresholds")
plt.ylabel("Rate")
plt.savefig(pathname + nombre + ".jpg",dpi=300)
plt.show()
