import datetime as __dt

formatos_default = [
    '%Y-%m-%d',
    '%d/%m/%y',
    '%d/%m/%Y',
    '%d-%m-%y',
    '%d-%m-%Y',
    '%d.%m.%y',
    '%d.%m.%Y',
    '%d%m%y',
    '%d%m%Y',
    '%y-%m-%d',
]


def hora_op(fecha):
    if fecha.minute == 0:
        if fecha.hour == 0:
            hora_op = 24
        else:
            hora_op = fecha.hour
    else:
        hora_op = fecha.hour +1
    
    return hora_op

def fecha_op(fecha):  
    if hora_op(fecha) == 24 :
        if fecha.hour == 0:
            return (fecha.date() + __dt.timedelta(days=-1))
        else:
            return fecha.date()
    else:
        return fecha.date()

def sumar_mes(fecha):

    if fecha.month == 12:
        return fecha.replace(year=fecha.year +1, month=1)
    else:
        return fecha.replace(month=fecha.month +1)
    
def restar_mes(fecha):
    if fecha.month == 1:
        return fecha.replace(year=fecha.year -1, month=12)
    else:
        return fecha.replace(month=fecha.month -1)

def hoy():
    return __dt.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)

def mes_dia_1(fecha):
    return fecha.replace(day=1)

def mes_ult_dia(fecha):
    return sumar_mes(mes_dia_1(fecha)) - __dt.timedelta(days=1)
    
def mes_act_dia_1():
    return mes_dia_1(hoy())

def mes_act_ult_dia():
    return min(hoy(),mes_ult_dia(hoy()))

def mes_ant_dia_1():
    return restar_mes(mes_act_dia_1())

def mes_ant_ult_dia():
    return mes_ult_dia(mes_ant_dia_1())
    
def periodo_mes_actual():
    return mes_act_dia_1(),mes_act_ult_dia()

def periodo_mes_anterior():
    return mes_ant_dia_1(),mes_ant_ult_dia()

def periodo_mes(fecha):
    
    fecha_ini = mes_dia_1(fecha)
    fecha_fin = mes_ult_dia(fecha)
    
    fecha_ini, fecha_fin = validar_fechas(fecha_ini,fecha_fin)
    
    return fecha_ini, fecha_fin

def iterar_entre_timestamps(ts_ini,ts_fin,timedelta):
    '''Itera entre dos objetos datetime. 
    El intervalo de iteración está dado por el objeto timedelta.
    
    Importante: incluye el valor final'''
    
    ts_ini, ts_fin = validar_fechas(ts_ini,ts_fin)
    
    td = timedelta
    ts_loop = ts_ini
    ts_loop_end = ts_fin
    
    while ts_loop <= ts_loop_end:
        
        if ts_loop == ts_ini:
            ts_cur_ini = ts_ini
            ts_cur_end = ts_ini + td

        elif ts_loop == ts_loop_end:
            ts_cur_ini = ts_loop_end
            ts_cur_end = ts_fin
            
        else:
            ts_cur_ini = ts_loop
            ts_cur_end = ts_loop + td

        yield ts_cur_ini,ts_cur_end
        
        ts_loop += td
        
def iterar_entre_timestamps_diario(ts_ini,ts_fin):
    '''Devuelve un iterador diario entre dos objetos datetime. 
    
    Importante: incluye el valor final'''
    
    return iterar_entre_timestamps(ts_ini,ts_fin,__dt.timedelta(days=1))

        
def iterar_mensual(ts_ini,ts_fin,):
    '''Itera entre dos objetos datetime, mensualmente.
    Descarta los valores diarios y horarios que tengan las fechas ingresadas.
    Sólo tomará los valores de año y mes.
    
    Importante: incluye el valor final'''
    
    ts_ini, ts_fin = validar_fechas(ts_ini,ts_fin)
    
    ts_ini = ts_ini.replace(day=1)
    ts_fin = ts_fin.replace(day=1)
    
    ts_loop = ts_ini
    ts_loop_end = sumar_mes(ts_fin)

    while ts_loop <= ts_fin:

        if ts_loop == ts_ini:
            ts_cur_ini = ts_ini
            ts_cur_end = sumar_mes(ts_ini)

        else:
            ts_cur_ini = ts_loop
            ts_cur_end = sumar_mes(ts_loop)

        yield ts_cur_ini,ts_cur_end
        
        ts_loop = sumar_mes(ts_loop)

def _procesar_formato(fecha,formato):
    try:
        return __dt.datetime.strptime(fecha,formato)
    except ValueError:
        return None

def _procesar_formatos(fecha,formatos):

    for formato in formatos:
        fecha_formateada = _procesar_formato(fecha,formato)
        if fecha_formateada != None:
            return fecha_formateada
        
    raise ValueError('Formato de fecha no reconocido.')

def input_fecha(nombre=''):
    '''Se prueban distintas combinaciones para reconocer el formato de fecha ingresado en el input.
    Devuelve un objeto datetime.datetime'''

    if not isinstance(nombre,str):
        raise ValueError('La variable "nombre" debe ser del tipo string')

    fecha = input(f'- Ingresar fecha {nombre}: \n')
    
    return _procesar_formatos(fecha,formatos_default)
    
def input_fechas(*args):
    '''Toma un conjunto de strings para solicitar fechas al usuario.
    Los valores deberían ser indicativos del tipo de fecha que se espera, ejemplos:
    
    ["Inicial", "Final", etc.] '''
    
    fechas = []
    for v in args:
        if not (isinstance(v,str)):
            raise ValueError(f'La variable {v} debe ser del tipo string')
        else:
            fechas.append(input_fecha(v))

    return fechas

def validar_fecha(fecha):
    if isinstance(fecha,str):
        fecha = _procesar_formatos(fecha,formatos_default)
    elif isinstance(fecha,__dt.datetime):
        pass
    else:
        raise ValueError('La variable "fecha" debe ser del tipo String o datetime.datetime')
    
    return min(hoy(),fecha)

def validar_fechas(fecha_ini,fecha_fin):
    
    fecha_ini = validar_fecha(fecha_ini)
    fecha_fin = validar_fecha(fecha_fin)
    
    fecha_ini, fecha_fin = sorted([fecha_ini,fecha_fin])
    
    return fecha_ini, fecha_fin