import json
import pandas as pd
import datetime as dt
import requests as req

from . import dirs
from . import fechas


__all__ = ['ApiCammesa',]

class ApiCammesa():
    '''Esta clase contiene principalmente métodos y pocos atributos.
    Sus atributos guardan consultas realizadas a la API de CAMMESA en la memoria.'''
    
    def __init__(self):
        self._consulta_total = None
        self._consulta_primeros = None
        self._consulta_ultimos = None
        self._consulta_custom = None
        self._filtro = None
        self._rts_vigentes = None
        
    @property
    def reportes_vigentes(self):
        if self._rts_vigentes is None:
            self._rts_vigentes = self.__cargar_rpts_vigentes()

        return self._rts_vigentes
    
    @property
    def filtro(self):
        return self._filtro
    
    @filtro.setter
    def filtro(self,val):
        self._filtro = self.__check_filtro(val)

    @property
    def consulta(self):

        if  self.filtro == 'primeros':
            return self._consulta_primeros
        elif self.filtro == 'ultimos':
            return self._consulta_ultimos
        elif self.filtro is None:
            return self._consulta_total
        else:
            return self._consulta_custom

    def __check_filtro(self,val):
            valores_posibles = ['primeros','ultimos']
            
            if  isinstance(val,str):
                val = val.lower()
                if not val in valores_posibles:
                    raise ValueError('La variable filtrar debe ser igual al string "primeros" o al string "ultimos"')
            elif val is None or val==True:
                pass
            else:
                raise TypeError('La variable filtro debe ser None, True o String')
            
            return val
    
    def __cargar_rpts_vigentes(self):
        
        url ='https://api.cammesa.com/pub-svc/public/catalogoPublicacionesVigentes'

        r = req.get(url)
        r_parsed = json.loads(r.text)

        return pd.DataFrame(list(r_parsed))
        
    def __get_fechas_consulta(self,fecha_i, fecha_f=None):
        
        fi, ff = fechas.validar_fechas(fecha_i, fecha_f)
        fi = fi.strftime('%Y-%m-%d')
        ff = ff.strftime('%Y-%m-%d')
        
        return fi, ff
    
    def __docs_by_nemo_rango(self,fecha_i, fecha_f=None,nemo_rpt=''):
        '''Consulta de reportes a la API de CAMMESA'''
        
        fi, ff = self.__get_fechas_consulta(fecha_i, fecha_f)
        
        url = 'https://api.cammesa.com/pub-svc/public/' + \
            'findDocumentosByNemoRango?' + \
            f'fechadesde={fi}T03%3A00%3A00.000%2B00%3A00&' + \
            f'fechahasta={ff}T03%3A00%3A00.000%2B00%3A00&' + \
            f'nemo={nemo_rpt}'
        
        r = req.get(url)
        
        return json.loads(r.text)
    
    def __get_link_descarga(self,archivo,id_doc,nemo_rpt):
        '''Simplemente devuelve un string que sirve para descargar un archivo'''
        
        if not(isinstance(archivo,str) and isinstance(id_doc,str) and isinstance(nemo_rpt,str)):
            raise ValueError('Las variables de entrada deben ser todas del tipo string')
        
        link_descarga = 'https://api.cammesa.com/pub-svc/public/' + \
                        'findAttachmentByNemoId?' + \
                        f'attachmentId={archivo}&' + \
                        f'docId={id_doc}&' + \
                        f'nemo={nemo_rpt}'
        
        return link_descarga

    def consultar(self,fecha_i, fecha_f, nemo_rpt,exportar_consulta=False,dir_consulta=None,filtro=None):
        '''Se ingresa con objetos datetime de fechas.
        Devuelve un dataframe de pandas con todos los archivos encontrados en dicho rango.
        NO FILTRA ni elimina duplicados en caso de existir varias versiones del mismo reporte (final/inicial)'''

        self.filtro = filtro

        r_parsed = self.__docs_by_nemo_rango(fecha_i, fecha_f,nemo_rpt=nemo_rpt)

        df_inicial = pd.DataFrame(list(r_parsed))
        df_inicial['adjuntos'] = df_inicial['adjuntos'].apply(list)
        df_inicial['fecha'] = pd.to_datetime(df_inicial['fecha'], format='%d/%m/%Y')
        df_inicial['version'] = pd.to_datetime(df_inicial['version'],format='%Y-%m-%dT%H:%M:%S.000-03:00')
        
        registros_adjuntos = [x[0] for x in df_inicial['adjuntos']]
        df_adjuntos = pd.DataFrame(registros_adjuntos).rename(columns={'id':'Archivo'})
        df_adjuntos['Archivo'] = df_adjuntos['Archivo'].str.upper()
        
        df_total  = df_inicial\
                    .drop(labels='adjuntos',axis=1)\
                    .join(df_adjuntos)\
                    .sort_values(by=['Archivo','version'],ascending=[1,1])
        
        self._consulta_total = df_total
        self._consulta_primeros = df_total.drop_duplicates(subset='Archivo',keep='first')
        self._consulta_ultimos = df_total.drop_duplicates(subset='Archivo',keep='last')

        if exportar_consulta:
            fecha_consulta = dt.datetime.now().strftime('%Y.%m.%d %H.%M.%S')
            nombre_archivo = f"Consulta {nemo_rpt} {fecha_consulta}.xlsx"
            
            if dir_consulta is None:
                dir_consulta = '' 
            else:
                dir_consulta = dirs.check_dir(dir_consulta) + '\\'
            
            self.consulta.to_excel(dir_consulta + nombre_archivo)
        
        del df_inicial, df_adjuntos
        
        return self.consulta
        
    def __descargar_reporte(self,archivo,id_doc,nemo_rpt,dir_descarga):
        '''Descarga un único archivo de la API de CAMMESA.'''
        
        if dir_descarga == None:
            dir_descarga = dirs.get_raiz() + '\\00 ZIP'
        else:
            dir_descarga = dirs.check_dir(dir_descarga)
        
        link_descarga = self.__get_link_descarga(archivo,id_doc,nemo_rpt)
        ruta_descarga = dir_descarga + "\\" + archivo

        print(f"Descargando: {archivo} {nemo_rpt}.")
        respuesta = req.get(link_descarga)

        with open(ruta_descarga, 'wb') as f:
            f.write(respuesta.content)

    def descargar_consulta(self,dir_descarga):
        '''Toma un dataframe de pandas formateado según la función consultar().
        Recorre el mismo y descarga todos los archivos en la carpeta designada como "dir_descarga"'''

        df = self.consulta
        registro_de_archivos = df.loc[:,['Archivo','id','nemo']].to_dict(orient='records')

        for r in registro_de_archivos:
            self.__descargar_reporte(
                r['Archivo'],
                r['id'],
                r['nemo'],
                dir_descarga
                )

    def descargar(self,
                  fecha_i, fecha_f,nemo_rpt, 
                  dir_descarga=None, 
                  exportar_consulta=False,dir_consulta=None, 
                  filtro=False
                  ):
        """Toma un dataframe de pandas formateado según la función consultar() del módulo cammesa_api.py.
        Recorre el mismo y descarga todos los archivos en la carpeta designada como 'dir_descarga' """

        if filtro != False:
            self.filtro = filtro
                   
        self.consultar(
            fecha_i, fecha_f, nemo_rpt,
            exportar_consulta=exportar_consulta, 
            dir_consulta=dir_consulta,
            filtro=self.filtro
            )
        
        self.descargar_consulta(dir_descarga)
    

        
        
