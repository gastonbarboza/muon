import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

###abre el osciloscopio
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

###define parámetros globales
sigomidiendo = True
nombrecarpeta = time.strftime("%m-%d-%H%M")
os.mkdir(nombrecarpeta)
nroplacas = int(sys.argv[1])
mismascondiciones = bool(int(sys.argv[2]))
n = int(sys.argv[3])

###funcion de escala para threshold
def escalafunc(threshold):
    if threshold < -.108:
        return(0.02)
    elif threshold <-.0539:
        return(0.01)
    elif threshold<-.0216:
        return(0.005)
    elif threshold < -.0108:
        return(0.002)
    else:
        return(0.001)

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
    for placa in placasAbarrertotal:
        #se posiciona en el canal que queremos medir
        osci.write('trigger:a:edge:slope fall; source ch{}'.format(placa))
        #crea lista de thresholds y array vacío de eventos
        listathresholds = np.linspace(arraycondiciones[placa-1][0],arraycondiciones[placa-1][1],arraycondiciones[placa-1][2])
        eventos = np.zeros(len(listathresholds))
        #hace el barrido (ahora si)
        segundos = arraycondiciones[placa-1][3]
        for index,threshold in enumerate(listathresholds):
            osci.write('trigger:a:level:ch{} {}'.format(placa,threshold)) #cambio el trigger
            escala = float(osci.query('horizontal:scale?'))
            osci.write('ch{}:scale {}'.format(placa,escalafunc(threshold)))
            osci.write('horizontal:scale {}; scale {}'.format(escala*1000,escala)) #esto reinicia el numero de adquisiciones
            time.sleep(segundos)
            mediciones = osci.query('acquire:numacq?')
            eventos[index] = int(mediciones)/segundos*60
        np.savetxt(nombrecarpeta + '/segplacafecha_{}_{}_{}.csv'.format(int(segundos),placa,time.strftime("%m-%d-%H%M%s")),np.transpose([listathresholds,eventos]),delimiter=',')
    sigomidiendo = int(input('Ingrese 0 para finalizar o cualquier otra número si quiere seguir explotándome. '))
input('noooo')
osci.close()

