import numpy as np
import os
import time

#File management
os.chdir(os.path.dirname(os.path.abspath(__file__))) 
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
if not(os.path.isdir(pathname)):
    os.mkdir(pathname) 
nombrearchivo = "backup.txt"

archivo = input('filename? ')
dato = False
coincidencias = []
with open(archivo) as input_file:
    for line in input_file:
        if dato == True:
            valor = ''.join(x for x in line if x.isdigit())
            coincidencias.append(int(valor))
        if line[0] == 'P':
            dato = True
        else:
            dato = False
nropuntos = 15 #int(input('Número de puntos? '))
nrorepeticiones = 45 #int(input('Número de repeticiones? '))
sumadatos = [0]*nropuntos
for punto in range(nropuntos):
    suma = 0
    for n in range(nrorepeticiones-1):
        suma += coincidencias[punto+n*nropuntos]
    sumadatos[punto] = suma/nrorepeticiones
ratelist = [39.0, 36.5, 34.0, 31.5, 29.0, 26.5, 24.0, 21.5, 19.0, 16.5, 14.0, 11.5, 9.0, 6.5, 4.0]
np.savetxt(pathname + nombrearchivo,np.transpose(np.matrix([ratelist,sumadatos])),delimiter=',')
