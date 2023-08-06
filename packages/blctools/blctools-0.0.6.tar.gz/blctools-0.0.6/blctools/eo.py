def convertir_a_rosa_de_los_vientos(val,estricto=True):
    '''Toma un valor int o float y asume que es una dirección de vientos en 360° grados Norte.
    
    val: Valor de la dirección de viento (int o float).
    
    estricto=True (por defecto) devuelve un error al ingresar un tipo de dato no numérico.
    estructi=False devuelve el dato original ante errores'''
    
    if isinstance(val,(int,float)):
        val %= 360
        
        rosa = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        rosa_aux = ["N"] + [e for e in rosa[1:] for _ in (0, 1)] + ["N"]

        rango_medio_bin = 180/len(rosa)
        indice = int(val//rango_medio_bin)
    
        return rosa_aux[indice]
    else:
        if estricto:
            raise ValueError('La dirección de viento debe ser un número int o float')
        else:
            return val