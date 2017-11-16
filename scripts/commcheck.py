import visa
import time
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination = '\n')
cero = time.time()
print(osci.query('*IDN?'))
print(time.time()-cero)
osci.close()
