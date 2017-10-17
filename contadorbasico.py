import visa
import time
import numpy as np
import matplotlib.pyplot as plt
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination='\n')

####
#código viejo:
####
seg = int(input('Cuántos segundos? '))
muonesIniciales = int(osci.query('ACQuire:NUMACq?'))
time.sleep(seg)
muonesNuevos = int(osci.query('ACQuire:NUMACq?')) - muonesIniciales
print('En {}s llegaron {} muones :u'.format(seg,muonesNuevos))
osci.close()
