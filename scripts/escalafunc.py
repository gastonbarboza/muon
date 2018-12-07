# El nivel de trigger (trig) del osciloscopio Tektronix DPO3054 
# solo puede tomar valores en cierto rango determinado por
# la posicion horizontal de la señal (h) y
# el tamaño de la división de la escala (div)
# dado por la fórmula
# -8 < trig + h < 8
# donde trig y h están dados en unidades de div
# e.g. si la escala es 1V y la señal está en h = 3div = 3V
# el trigger como muy bajo puede ser -11div = -11V

# Este programa calcula, dado un trigger deseado,
# qué escala debe setearse en el osciloscopio

def escalafunc(threshold,hpos):
    if threshold < 0:
        mindiv = threshold/(-8-hpos)*1.01
    elif threshold > 0:
        mindiv = threshold/(8-hpos)*1.01
    else:
        raise ValueError('Zero threshold can use any scale.')
    return mindiv
