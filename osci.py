import visa
import time
import numpy as np
import matplotlib.pyplot as plt
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

voltajeinicial = float(input('Threshold más grande: '))
voltajefinal = float(input('Threshold menos grande: '))
numerothresholds = int(input('Decime cuántos datos: '))
segundos = int(input('Cuánto tiempo mido? Decimeee: '))
input("Chequeemos comunicacion: {}. Presione enter para continuar".format(osci.query('*IDN?')))
print('Hora de detectar muones. Que la fuerza electrodébil te acompanie.')
listathresholds = np.linspace(-.1,-.08,3)
listathresholds = np.linspace(voltajeinicial,voltajefinal,num=numerothresholds)

eventos = np.zeros(len(listathresholds))
for index,threshold in enumerate(listathresholds):
    osci.write('trigger:a:level:ch1 {}'.format(threshold)) #apago la adquisición y cambio el trigger
    escala = float(osci.query('horizontal:scale?')) #esto se fija qué escala estamos usando
    osci.write('horizontal:scale {}; scale {}'.format(1,escala)) #esto reinicia el numero de adquisiciones
    time.sleep(segundos)
    eventos[index] = int(osci.query('acquire:numacq?'))
np.savetxt('medicion_{}.csv'.format(time.strftime("%m-%d-%H%M")),np.transpose([listathresholds,eventos]),delimiter=',')
plt.plot(-1*listathresholds,eventos,'ro')
plt.grid()
plt.show()
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
