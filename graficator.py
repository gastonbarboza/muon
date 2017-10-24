import time
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

listadedatos = list(os.walk("./graficar/"))[0][2]
print(listadedatos)
for grafico in listadedatos:
    dato = np.loadtxt("./graficar/" + grafico,delimiter=',')
    etiqueta=input("Leyenda para {}?".format(grafico))
    colorcito=input("Color?")
    plt.scatter(-dato[:,0],dato[:,1],label=etiqueta,color=colorcito)
plt.legend()
plt.grid()
plt.title(time.strftime("%d de %b"))
plt.xlabel("Thresholds (logV)")
plt.ylabel("log(eventos/minuto)")
plt.savefig(time.strftime("%d_de_%b")+"sinlog.jpg",dpi=1500)
plt.show()