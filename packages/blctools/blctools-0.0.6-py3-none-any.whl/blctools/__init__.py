#Funciones
from . import eo
from . import fv
from . import fechas
from .dirs import  *

#Clases
from .cl_UsuarioCammesa import *    # Alberga métodos y propiedades de la API de CAMMESA, cuando ésta requiere log in
from .cl_Pronosticos import *       # Dreivada de la clase UsuarioCammesa. Dispara consultas a la api de CAMMESA (requiere log in) para descargar pronósticos de generación

from .cl_ApiCammesa import *        # Maneja consultas de CAMMESA que NO requieren log in
from .cl_ReporteBase import *       # Derivada de la clase cl_ApiCammesa. Agrega funcionalidades alrededor de la nube de BLC y la Api de CAMMESA
from .cl_PPO import *               # Derivada de la clase cl_ReporteBase. Simplemente tiene configuraciones "listas para" consultar los reportes PPO diarios de CAMMESA
from .cl_DTE import *               # Derivada de la clase cl_ReporteBase. Simplemente tiene configuraciones "listas para" consultar los reportes DTE mensuales de CAMMESA

#Versión
__version__ = "0.0.6"