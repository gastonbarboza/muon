import visa
import time
import numpy as np
import sys

#El programa debe ser llamado de la siguiente manera:
# >>sudo python3 barridolargo.py rateminimo ratemaximo nropuntos tiempoporpunto
#donde el tiempo esta medido en segundos
#rate debe ser mayor que 22

dateinicial = time.strftime("%y.%m.%d_%H.%M")
rm = visa.ResourceManager('@sim')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

#Parametros de nuestra medicion
nropuntos = int(sys.argv[3])
ratelist = np.linspace(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
tiempomedicion = float(sys.argv[4]) #Cuanto tiempo quiero barrer cada threshold

#Funcion que calcula el treshold para cada PMT en funcion del rate deseado
def thresholds(rate):
    y2 = -.041866
    A2 = 122846.14004
    R2 = 134.897872
    y1 = 21.27975
    A1 = 783197.61244
    R1 = 97.72976
    threshold1 = np.log((rate - y1)/A1)/R1 #rate debe ser mayor que 22
    threshold2 = np.log((rate - y2)/A2)/R2 
    return threshold1, threshold2

#Crea csv para guardar
matrizdedatos = np.transpose([ratelist,np.zeros(nropuntos)])

#Hace el barrido
for index,rate in enumerate(ratelist):
    threshold1, threshold2 = thresholds(rate)
    osci.write('TRIGger:A:SETHold:CLOCk:THReshold {}'.format(threshold2))
    osci.write('TRIGger:A:SETHold:DATa:THReshold {}'.format(threshold1))
    muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
    time.sleep(tiempomedicion)
    nromuones = int(osci.query('ACQuire:NUMACq?'))- muonesIniciales
    matrizdedatos[index][1] = nromuones
    np.savetxt('barridolargo_' + dateinicial + '.csv',matrizdedatos,delimiter=',')
    print(str(nromuones) + ' coincidencias para rate {}'.format(rate))
    print('Threshold 1: {0:.2f}'.format(threshold1))
    print('Threshold 2: {0:.2f}'.format(threshold2))
osci.close()
