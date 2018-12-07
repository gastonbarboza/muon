# Este es un programa para hacer el bias curve de pmts
# conectados a placas centelladoras enviando pulsos negativos
# a un osciloscopio tektronix
# como parte de un detector de muones de la materia Laboratorio 7 
# de la carrera de Ciencias Fisicas de la Universidad de Buenos Aires
# entre agosto del 2017 y julio del 2018
# en el Instituto de Astrofisica del Espacio (IAFE) del CONICET
# bajo la dirección de los doctores Adrián Rovero y Ana Pichel
# con los alumnos Tomás Codina y Gastón Barboza

# Información de contacto:
# barbozagaston@gmail.com
# tomycodina@gmail.com

# El programa cuenta el número de pulsos detectados por el osciloscopio
# que se encuentran por debajo de cierto threshold que se varía por 
# comunicación USB usando el módulo pyvisa de hgrecco




## al programa hay que llamarlo
## >>python3 calibracion_individual.py nroplacas mismascondiciones n
## donde nroplacas es 0 para ambas, 1 para la placa 1, 2 para la placa 2
## mismascondiciones es 0 (falso) o 1 (verdadero)
## n es la cantidad de veces que barre la serie (por cortes de luz)
## e.g. python3 calibracion_individual.py 2 0 3
## levantará curvas para los dos canales del osciloscopio variando
## los thresholds de manera distinta para cada canal, y lo hará 3 veces



###Comienza el programa
import visa
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from escalafunc import escalafunc

###abre la comunicación con el osciloscopio
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
hpos = 3

###establece dónde se grabarán los archivos
os.chdir(os.path.dirname(os.path.abspath(__file__))) 
pathname = "../datos_temp/"+time.strftime("%d%b")+"/"
if not(os.path.isdir(pathname)):
    os.mkdir(pathname) 
nombrecarpeta = pathname + "calibracion"+time.strftime("%y.%m.%d_%H.%M")+"/"
if not(os.path.isdir(nombrecarpeta)):
    os.mkdir(nombrecarpeta)

########
#acá comienza la sección de barrido
########
while sigomidiendo:
    #pregunta si usar configuración predeterminada
    print("Por default se miden ambas placas, haciendo series de 5hs.")
    print("Se levantan 15 puntos de cada una con 600s de medición,")
    print("barriendo logarítmicamente de 20mV a 200mV para el canal 1,")
    print("y de 50mV a 700mV para el canal 2.")
    default = input("Usar configuración predeterminada? (y/n)")
    if  default == "y":
        placasAbarrer = [1,2]
        arraycondiciones = [[3,5.3,15,600],[3.91,6.55,15,600]]
        placasAbarrertotal = [item[j] for item in [placasAbarrer] for i in range(n) for j in range(len(placasAbarrer))]
     

    #en caso de querer establecer nuevas condiciones, lo hace acá
    elif default == "n":
        
        placasAbarrer = [1,2] if nroplacas == 0 else [nroplacas]
        arraycondiciones = [0,0]
        logarraybool = input('Espaciado logarítmico de los thresholds? (y/n): ')
        if logarraybool == "y":
            logarray = True
        elif logarraybool == "n":
            logarray = False
        else:
            print("No sabés escribir?")
            osci.close()
            break

        #Barrido lineal
        if logarray == False:
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

        #Barrido logaritmico ## completar
        elif logarray == True:
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
    else:
        print('Escribiste mal salame:')
        break





    ########
    #empieza el barrido
    ########
    input("Chequeemos comunicacion: {}. Presione enter para continuar".format(osci.query('*IDN?')))
    print('Hora de detectar muones. Que la fuerza electrodébil te acompanie.')
    print('\n')
    for placa in placasAbarrer:
        segundos = arraycondiciones[placa-1][3]
        listathresholds = np.linspace(arraycondiciones[placa-1][0],arraycondiciones[placa-1][1],arraycondiciones[placa-1][2])/-1000#np.logspace(arraycondiciones[placa-1][0],arraycondiciones[placa-1][1],arraycondiciones[placa-1][2],base= 2.718281828459045)/-1000
        print('Para la placa {}, vamos a barrer los siguientes thresholds'.format(placa))
        print(listathresholds)
        print('con {} segundos cada punto.'.format(segundos))
        print('\n')
    for placa in placasAbarrertotal:
        #se posiciona en el canal que queremos medir
        osci.write('trigger:a:edge:slope fall; source ch{}'.format(placa))
        #crea lista de thresholds y array vacío de eventos
        listathresholds = np.linspace(arraycondiciones[placa-1][0],arraycondiciones[placa-1][1],arraycondiciones[placa-1][2])/-1000#np.logspace(arraycondiciones[placa-1][0],arraycondiciones[placa-1][1],arraycondiciones[placa-1][2],base= 2.718281828459045)/-1000
        eventos = np.zeros(len(listathresholds))
        #hace el barrido (ahora si)
        for index,threshold in enumerate(listathresholds):
            osci.write('trigger:a:level:ch{} {}'.format(placa,threshold)) #cambio el trigger
            escala = float(osci.query('horizontal:scale?'))
            osci.write('ch{}:scale {}'.format(placa,escalafunc(threshold,hpos))) #cambia la escala para no perder eventos por falta de resolucion
            osci.write('horizontal:scale {}; scale {}'.format(escala*1000,escala)) #esto reinicia el numero de adquisiciones
            time.sleep(segundos)
            mediciones = osci.query('acquire:numacq?')
            eventos[index] = int(mediciones)/segundos*60
        nombrearchivo = 'date_{}.plc_{}.pmt_{}.pin_{}.volt_{}.cent_{}.seg_{}.csv'.format(time.strftime("%m-%d-%H%M%s"),placa,pmt[placa-1],pin[placa-1],volt[placa-1],cent[placa-1],int(segundos))
        np.savetxt(nombrecarpeta + nombrearchivo,np.transpose([listathresholds,eventos]),delimiter=',')
    sigomidiendo = int(input('Ingrese 0 para finalizar o cualquier otra número si quiere seguir explotándome. '))
print('noooo')
osci.close()

