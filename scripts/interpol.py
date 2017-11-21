import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.pyplot as plt

def threshold(rate):
    #ordena alfabeticamente los archivos del directorio
    listadedatos = sorted(list(os.walk("./interpol"))[0][2])

    #los divide en las dos series
    nroarchivos = len(listadedatos)
    cantidadporserie = nroarchivos//2

    listadedatos1 = listadedatos[0:cantidadporserie]
    listadedatos2 = listadedatos[cantidadporserie + 1:nroarchivos]

    #carga las dos series de archivos sumandolas
    datos1 = np.loadtxt("./interpol/" + listadedatos1.pop(0),delimiter=',')
    for datito in listadedatos1:
        datos1 = [x + y for x,y in zip(datos1,np.loadtxt("./interpol/" + datito,delimiter=','))]

    datos2 = np.loadtxt("./interpol/" + listadedatos2.pop(0),delimiter=',')
    for datito in listadedatos2:
        datos2 = [x + y for x,y in zip(datos2,np.loadtxt("./interpol/" + datito,delimiter=','))]
    datos = [np.matrix(datos1)/cantidadporserie,np.matrix(datos2)/cantidadporserie]

    #los divide por la cantidad de archivos por serie
    datos = [np.matrix(datos1)/cantidadporserie,np.matrix(datos2)/cantidadporserie]

    #el carozo del durazno
    thresholds = []
    r = rate*60
    for dato in datos:
        for fila in range(len(dato)):
            r1 = dato[fila,1]
            if r < r1:
                pass
            else:
                r0 = dato[fila-1,1]
                t1 = dato[fila,0]
                t0 = dato[fila-1,0]
                T = t1 + (r - r1)/(r0- r1) * (t0 - t1)
                thresholds.append(T)
                break
    return thresholds
