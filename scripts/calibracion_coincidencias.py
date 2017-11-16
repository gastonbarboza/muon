import visa
from time import strftime,sleep
import numpy as np
import sys
import os

#El programa debe ser llamado de la siguiente manera:
# >>sudo python3 barridolargo.py rateminimo ratemaximo nropuntos tiempoporpunto repeticiones (
#donde el tiempo esta medido en segundos
#rate debe ser mayor que 22

rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

#Parametros de nuestra medicion
nropuntos = int(sys.argv[3])
ratelist = np.logspace(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
tiempomedicion = float(sys.argv[4]) #Cuanto tiempo quiero barrer cada threshold
repeticiones = int(sys.argv[5])

#Funcion que calcula el treshold para cada PMT en funcion del rate deseado
def thresholds(rate):
    y2 = 0
    A2 = 242.7012
    R2 = 51.23416
    y1 = 0.78340
    A1 = 159.0289
    R1 = 83.3262
    threshold1 = np.log((rate + y1)/A1)/R1 
    threshold2 = np.log((rate + y2)/A2)/R2 
    return threshold1, threshold2

print(np.transpose(np.matrix(ratelist)))
print(thresholds(30))

#Crea csv para guardar
matrizdedatos = np.transpose([ratelist,np.zeros(nropuntos)])

#Hace el barrido
nombrecarpeta = "coincidencias_"+strftime("%H_%M")
os.mkdir(nombrecarpeta)

for j in range(repeticiones):
    dateinicial = strftime("%y.%m.%d_%H.%M.%s")

    for index,rate in enumerate(ratelist):
        threshold1, threshold2 = thresholds(rate)
        osci.write('TRIGger:A:SETHold:CLOCk:THReshold {}'.format(threshold2))
        osci.write('TRIGger:A:SETHold:DATa:THReshold {}'.format(threshold1))
        print('vamos bien')
        muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
        sleep(tiempomedicion)
        nromuones = int(osci.query('ACQuire:NUMACq?'))- muonesIniciales
        matrizdedatos[index][1] = nromuones
        np.savetxt(nombrecarpeta + '/coinc' + dateinicial + '.csv',matrizdedatos,delimiter=',')
        print(str(nromuones) + ' coincidencias para rate {}'.format(rate))
        print('Threshold 1: {}'.format(threshold1))
        print('Threshold 2: {}'.format(threshold2))
osci.close()
