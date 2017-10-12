import visa
import time
import numpy as np
import matplotlib.pyplot as plt
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

voltajeminimo = float(input('Threshold minimo: '))
segundos = int(input('Cuánto tiempo mido? Decimeee: '))
input("Chequeemos comunicacion: {}. Presione enter para continuar".format(osci.query('*IDN?')))
print('Hora de detectar muones de otra manera. Que la fuerza electrodébil te acompanie.')

listamediciones = []
#CONFIGURA TRIGGER Y MEDICION
osci.write('trigger:a:level:ch1 {}'.format(voltajeminimo)) #apago la adquisición y cambio el trigger
osci.write('measurement:immediate:type minimum')
#REINICIA NUMERO ADQUISICIONES
escala = float(osci.query('horizontal:scale?')) #esto se fija qué escala estamos usando
osci.write('horizontal:scale {}; scale {}'.format(1,escala)) #esto reinicia el numero de adquisiciones
#EMPIEZA A MEDIR
origen = time.time()
while time.time() - origen < segundos:
    #osci.write('*WAI')
    osci.write('measurement:immediate:value')
    while int(osci.query('*BUSY'))==1:
        0 == 0
    listamediciones.append(osci.read('measurement:immediate:value?'))
numeroadquisiciones = int(osci.query('acquire:numacq?'))
print(len(listamediciones))
print(numeroadquisiciones)
input("presione enter para terminar")
#np.savetxt('medicion_{}.csv'.format(time.strftime("%m-%d-%H%M")),np.transpose([listathresholds,eventos]),delimiter=',')
#plt.plot(-1*listathresholds,eventos,'ro')
#plt.grid()
#plt.show()
osci.close()

####
#código viejo:
####
#seg = int(input('Cuántos segundos? '))
#muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
#time.sleep(seg)
#muonesNuevos = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
#print('En {}s llegaron {} muones :u'.format(seg,muonesNuevos))
#osci.close()
