
from . import dirs
from . import fechas

from .cl_ReporteBase import *

__all__ = ['DTE',]

class DTE(ReporteBase):
    
    def __init__(
        self,
        fecha_i = fechas.hoy(),
        fecha_f = fechas.hoy(),
        nemo_rpt = 'DTE_UNIF',
        nombre = 'DTE',
        formato_nombre_archivo = 'DTE%y%m',
        parques = [],
        extension = 'mdb',
        tabla_datos = 'Q_RepItems',
        tabla_fecha = 'VALORES_PERIODO',
        col_filtro = 'NEMO',
        dir_salida = dirs.get_raiz(),
        dir_descarga = None,
        dir_extraccion = None,
        funcion_archivos_necesarios = fechas.iterar_mensual,
        ):

        if dir_descarga is None:
            try:
                dir_descarga=dirs.get_dc_dte() + '\\00 ZIP'
            except:
                dir_descarga = dirs.get_raiz() + '\\00 ZIP'

        if dir_extraccion is None:
            try:
                dir_extraccion=dirs.get_dc_dte() + '\\01 MDB'
            except:
                dir_extraccion = dirs.get_raiz() + '\\01 MDB'
        
        super().__init__(
            fecha_i = fecha_i,
            fecha_f = fecha_f,
            nemo_rpt = nemo_rpt,
            nombre = nombre,
            formato_nombre_archivo = formato_nombre_archivo,
            parques = parques,
            extension = extension,
            tabla_datos = tabla_datos,
            tabla_fecha = tabla_fecha,
            col_filtro = col_filtro,
            dir_salida = dir_salida,
            dir_descarga = dir_descarga,
            dir_extraccion = dir_extraccion,
            funcion_archivos_necesarios = funcion_archivos_necesarios
            )
    #Fin de la función __init__
    