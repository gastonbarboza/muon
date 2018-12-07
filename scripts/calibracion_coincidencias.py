import visa
from time import strftime,sleep
import numpy as np
import time
import sys
import os
from  interpol import threshold
from escalafunc import escalafunc

#El programa debe ser llamado de la siguiente manera:
# >>python3 barridolargo.py rateminimo ratemaximo nropuntos tiempoporpunto repeticiones (
#donde el tiempo esta medido en segundos
#rate debe ser mayor que 22

rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

#Parametros de nuestra medicion
nropuntos = int(sys.argv[3])
ratelist = np.linspace(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]))
tiempomedicion = float(sys.argv[4]) #Cuanto tiempo quiero barrer cada rate
repeticiones = int(sys.argv[5])
seg = 0 #cuánto tiempo vamos a dedicar a ver si el rate es el correcto

#File management
os.chdir(os.path.dirname(os.path.abspath(__file__))) 
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
if not(os.path.isdir(pathname)):
    os.mkdir(pathname) 
nombrecarpeta = pathname + "coincidencias"+time.strftime("%y.%m.%d_%H.%M")+"/"
if not(os.path.isdir(nombrecarpeta)):
    os.mkdir(nombrecarpeta)
nombrearchivo = "coincidencias.pines_5_9.volt_850_852.seg_{}.".format(tiempomedicion)

#Imprime rates para chequear que esté todo bien
ratestring = ', '.join(map(str,ratelist.tolist()))
print('Rates a barrer: ' + ratestring)

#Crea array para guardar
matrizdedatos = np.transpose([ratelist,np.zeros(nropuntos)])
matrizderates = np.transpose([ratelist,np.zeros(nropuntos),np.zeros(nropuntos)])

#Hace el barrido
for j in range(repeticiones):
    for index,rate in enumerate(ratelist):
        threshold1, threshold2 = threshold(rate)
        escala1 = escalafunc(threshold1,3)
        escala2 = escalafunc(threshold2,3)
        if seg>0:
            #Primero miramos cuál es el rate real para cada uno
            #para contrastar por lo predicho por la curva
            osci.write('ch1:scale {}; :ch2:scale {}'.format(escala1,escala2))
            osci.write('trigger:a:type edge')
            osci.write('trigger:a:edge:source ch1')
            osci.write('trigger:a:level {}'.format(threshold1))
            muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
            time.sleep(seg)
            muonesNuevos = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
            #ahora para el canal 2
            osci.write('trigger:a:edge:source ch2')
            osci.write('trigger:a:level {}'.format(threshold2))
            muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
            time.sleep(seg)
            muonesNuevos2 = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
            matrizderates[index][1] = muonesNuevos/seg
            matrizderates[index][2] = muonesNuevos2/seg
            print(muonesNuevos/seg)
        osci.write('trigger:a:logic:class sethold')
        osci.write('trigger:a:type logic')
        osci.write('tigger:a:sethold:clock:source ch1')
        osci.write('tigger:a:sethold:data:source ch2')
        osci.write('ch1:scale {}; :ch2:scale {}'.format(escala1,escala2))
        osci.write('TRIGger:A:SETHold:CLOCk:THReshold {}'.format(threshold1))
        osci.write('TRIGger:A:SETHold:DATa:THReshold {}'.format(threshold2))
        print('Estamos configurando la siguiente medición. Por favor espere...')
        sleep(1)
        muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
        print('{} eventos iniciales'.format(muonesIniciales))
        print('Para el rate {} seteamos los thresholds en {}mV para el canal 1 y {}mV para el 2'.format(rate,int(threshold1*-1000),int(threshold2*-1000)))
        sleep(tiempomedicion)
        nromuones = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
        matrizdedatos[index][1] = nromuones/tiempomedicion
        print(str(nromuones) + ' coincidencias en ' + str(tiempomedicion) + ' segundos')
    np.savetxt(nombrecarpeta + nombrearchivo + strftime("%y_%m_%d.%H_%M_%s_labo7") + '.csv',matrizdedatos,delimiter=',')
    np.savetxt(nombrecarpeta + nombrearchivo + strftime("_rates_%y_%m_%d.%H_%M_%s") + '.csv',matrizderates,delimiter=',')
osci.close()
