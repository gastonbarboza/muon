import visa
rm = visa.ResourceManager('@py')
osci = rm.open_resource(rm.list_resources()[0],read_termination = '\n')
print(osci.query('*IDN?'))
