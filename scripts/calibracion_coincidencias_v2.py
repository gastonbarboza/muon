import visa
from time import strftime,sleep
import numpy as np
import time
import sys
import os
from  interpol import threshold
from escalafunc import escalafunc

#El programa debe ser llamado de la siguiente manera:
# >>python3 barridolargo.py thrminimo(mv) thrmaximo(mv) nropuntos(...) tiempoporpunto(s) repeticiones cualcanal
#donde el tiempo esta medido en segundos
#rate debe ser mayor que 22

rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

#Parametros de nuestra medicion
nropuntos = int(sys.argv[3])
thrshlist = np.linspace(float(sys.argv[1])/(-1000), float(sys.argv[2])/(-1000), int(sys.argv[3])) #ahora esto es una lista de thresholds
tiempomedicion = float(sys.argv[4]) #Cuanto tiempo quiero barrer cada rate
repeticiones = int(sys.argv[5])
cualcanal = int(sys.argv[6])
cualcanalno = cualcanal +  (-1)**(cualcanal+1) #da 1 si es 2 y da 2 si es 1
seg = 0 #cuánto tiempo vamos a dedicar a ver si el rate es el correcto

#File management
os.chdir(os.path.dirname(os.path.abspath(__file__))) 
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
if not(os.path.isdir(pathname)):
    os.mkdir(pathname) 
nombrecarpeta = pathname + "coincidencias"+time.strftime("%y.%m.%d_%H.%M")+"/"
if not(os.path.isdir(nombrecarpeta)):
    os.mkdir(nombrecarpeta)
nombrearchivo = "coincidencias.flor.y.emi.88cm.seg_{}.".format(tiempomedicion)

#Imprime rates para chequear que esté todo bien
ratestring = ', '.join(map(str,thrshlist.tolist()))
print('Thresholds a barrer: ' + ratestring)

#Crea array para guardar
matrizdedatos = np.transpose([thrshlist,np.zeros(nropuntos)])
matrizderates = np.transpose([thrshlist,np.zeros(nropuntos),np.zeros(nropuntos)])

#Hace el barrido
for j in range(repeticiones):
    for index,threshold in enumerate(thrshlist):
        escala = escalafunc(threshold,3)
        if seg>0:
            #Primero miramos cuál es el rate real para cada uno
            #para contrastar por lo predicho por la curva
            osci.write('ch{}:scale {}'.format(cualcanal,escala))
            osci.write('trigger:a:type edge')
            osci.write('trigger:a:edge:source ch{}'.format(cualcanal))
            osci.write('trigger:a:level {}'.format(threshold))
            muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
            time.sleep(seg)
            muonesNuevos = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
            #ahora para el canal que no varia su threshold
            osci.write('trigger:a:edge:source ch{}'.format(cualcanalno))
            muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
            time.sleep(seg)
            muonesNuevos2 = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
            matrizderates[index][1] = muonesNuevos/seg
            matrizderates[index][2] = muonesNuevos2/seg
            print(muonesNuevos/seg)
        osci.write('trigger:a:logic:class sethold')
        osci.write('trigger:a:type logic')
        osci.write('tigger:a:sethold:clock:source ch{}'.format(cualcanal))
        osci.write('tigger:a:sethold:data:source ch{}'.format(cualcanalno))
        osci.write('ch{}:scale {}'.format(cualcanal,escala))
        osci.write('TRIGger:A:SETHold:CLOCk:THReshold {}'.format(threshold))
        print('Estamos configurando la siguiente medición. Por favor espere...')
        sleep(1)
        muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
        print('{} eventos iniciales'.format(muonesIniciales))
        print('seteamos el threshold en {}mV para el canal {}'.format(threshold*(-1000),cualcanal))
        sleep(tiempomedicion)
        nromuones = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
        matrizdedatos[index][1] = nromuones/tiempomedicion
        print(str(nromuones) + ' coincidencias en ' + str(tiempomedicion) + ' segundos')
    np.savetxt(nombrecarpeta + nombrearchivo + strftime("%y_%m_%d.%H_%M_%s") + '.csv',matrizdedatos,delimiter=',')
    np.savetxt(nombrecarpeta + nombrearchivo + strftime("_rates_%y_%m_%d.%H_%M_%s") + '.csv',matrizderates,delimiter=',')
osci.close()
