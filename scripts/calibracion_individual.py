import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from escalafunc import escalafunc

###abre el osciloscopio
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

###define parámetros globales
sigomidiendo = True
nroplacas = int(sys.argv[1]) 
mismascondiciones = bool(int(sys.argv[2]))
n = int(sys.argv[3])
pmt = [2,1]
pin = [5,9]
volt = [850,852]
cent = [2,2]
##al programa hay que llamarlo
## >>python3 calibracion_individual.py nroplacas mismascondiciones n
## donde nroplacas es 0 para ambas, 1 para la placa 1, 2 para la placa 2
## mismascondiciones es 0 (falso) o 1 (verdadero)
## n es la cantidad de veces que barre la serie (por cortes de luz)

#puntos extra (agregados a manopla)
puntoextra=[2,1]
posicionextra=[1,0]

#File management
os.chdir(os.path.dirname(os.path.abspath(__file__))) 
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
if not(os.path.isdir(pathname)):
    os.mkdir(pathname) 
nombrecarpeta = pathname + "calibracion"+time.strftime("%y.%m.%d_%H.%M")+"/"
if not(os.path.isdir(nombrecarpeta)):
    os.mkdir(nombrecarpeta)

###hace el barrido
while sigomidiendo:
    #crea arrays para el barrido
    placasAbarrer = [1,2] if nroplacas == 0 else [nroplacas]
    arraycondiciones = [0,0]
    if nroplacas == 0:
        arraycondiciones[0] = [float(num) for num in input('Thresholds superior, inferior, nro datos, tiempo por medición para la placa 1 separados por espacios: ').split()] #.1 .2 25 60
        if mismascondiciones == True: #input('Mismas condiciones para placa 2? y/n: ')=='y': 
            arraycondiciones[1] = arraycondiciones[0]
        else:
            arraycondiciones[1] = [float(num) for num in input('Bueno dale... vos sabés qué hacer: ').split()]
    else:
        arraycondiciones[0] = [float(num) for num in input('Thresholds superior, inferior, nro datos, tiempo por medición para la placa {} separados por espacios: '.format(nroplacas)).split()]
        arraycondiciones[1] = arraycondiciones[0]
    placasAbarrertotal = [item[j] for item in [placasAbarrer] for i in range(n) for j in range(len(placasAbarrer))]

    #empieza el barrido
    input("Chequeemos comunicacion: {}. Presione enter para continuar".format(osci.query('*IDN?')))
    print('Hora de detectar muones. Que la fuerza electrodébil te acompanie.')
    print('\n')
    for placa in placasAbarrer:
        segundos = arraycondiciones[placa-1][3]
        print('Para la placa {}, vamos a barrer los siguientes thresholds'.format(placa))
        print(listathresholds)
        print('con {} segundos cada punto.'.format(segundos))
        print('\n')
    for placa in placasAbarrertotal:
        #se posiciona en el canal que queremos medir
        osci.write('trigger:a:edge:slope fall; source ch{}'.format(placa))
        #crea lista de thresholds y array vacío de eventos
        listathresholds = np.insert(np.linspace(arraycondiciones[placa-1][0],arraycondiciones[placa-1][1],arraycondiciones[placa-1][2]),posicionextra[placa-1],puntoextra[placa-1])/-1000
        eventos = np.zeros(len(listathresholds))
        #hace el barrido (ahora si)
        for index,threshold in enumerate(listathresholds):
            osci.write('trigger:a:level:ch{} {}'.format(placa,threshold)) #cambio el trigger
            escala = float(osci.query('horizontal:scale?'))
            osci.write('ch{}:scale {}'.format(placa,escalafunc(threshold))) #cambia la escala para no perder eventos por falta de resolucion
            osci.write('horizontal:scale {}; scale {}'.format(escala*1000,escala)) #esto reinicia el numero de adquisiciones
            time.sleep(segundos)
            mediciones = osci.query('acquire:numacq?')
            eventos[index] = int(mediciones)/segundos*60
        nombrearchivo = 'date_{}.plc_{}.pmt_{}.pin_{}.volt_{}.cent_{}.seg_{}.csv'.format(time.strftime("%m-%d-%H%M%s"),placa,pmt[placa-1],pin[placa-1],volt[placa-1],cent[placa-1],int(segundos))
        np.savetxt(nombrecarpeta + nombrearchivo,np.transpose([listathresholds,eventos]),delimiter=',')
    sigomidiendo = int(input('Ingrese 0 para finalizar o cualquier otra número si quiere seguir explotándome. '))
print('noooo')
osci.close()

