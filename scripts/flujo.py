import visa
import time
import numpy as np
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

#barrido de flujo
divisiones = 24*6
tiempototal = 86400
muones = []

dateinicial = time.strftime("%y.%m.%d_%H.%M")
tiempocero = time.time()
for hora in range(divisiones):
    muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
    time.sleep(tiempototal/divisiones)
    nromuones = int(osci.query('ACQuire:NUMACq?'))- muonesIniciales
    print(nromuones)
    muones.append(nromuones)
    hora = str(time.time()-tiempocero)
    np.savetxt('barridolargo_'+dateinicial+'.csv',muones,delimiter=',')
osci.close()
