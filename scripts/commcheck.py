import visa
import time
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination = '\n')
cero = time.time()
osci.query('*IDN?')
while(True):
    input()
    osci.write('ch1:scale {}; :ch2:scale {}'.format(escala1,escala2))
    print(osci.query('ACQuire:NUMACq?'))
osci.close()
