import glob
import pandas as pd
import wrf
import re
from datetime import date, timedelta, datetime
from netCDF4 import Dataset


# Diccionario para almacenar variables de nc
variables_dict = {}


def identidad(var):
    """
    Función identidad
    """
    return var


def k_to_c(var):
    """
    Convierte de gr
    ados kelvin a grados celsius
    """
    var.values = var.values - 273.15
    var.attrs['units'] = 'degC'
    return var


def cargaListaCSV(path: str, param: str):
    """  Esta funcion recorrer todo un path en busca de archvios csv de la
    slaida de wrfplot y los carga en un dataframe
    """
    lista_csv = glob.glob(path, recursive=True)

    if param == 'A':
        lista_filtrada = lista_csv[420:828]
    elif param == 'B':
        lista_filtrada = lista_csv[248:619]
    elif param == 'C':
        lista_filtrada = lista_csv[241:613]
    elif param == 'D':
        lista_filtrada = lista_csv[201:580]

    dfData = pd.DataFrame([], columns=['date', 'Temp'], dtype=float)

    for path in lista_filtrada:
        try:
            csv_data = pd.read_csv(f"{path}")
        except IOError:
            print("Error: File does not appear to exist.")

        dfTemp = pd.DataFrame(dtype=float)

        dfTemp['date'] = pd.to_datetime(csv_data['fecha'],
                                        format='%Y-%m-%d %H:%M:%S')
        dfTemp['Temp'] = csv_data['t2']

        dfData = pd.concat([dfData, dfTemp[9:33]], ignore_index=True)

    dfTest = dfData.set_index('date')

    return dfTest


def guardarPickle(dfTmp, filename: str):
    dfTmp.to_pickle(f'../pickles/{filename}')


def filter_by_dates(file_list, start_date, end_date, extra_filter=None):
    """filter files names in 'file_list' that belongs to creation dates
    betweeen [start_date, end_date)
    start_date and end_date are given as YYYY-MM-DD"""

    filtered_dates = list()
    sd = datetime.strptime(start_date, '%Y-%m-%d').date()  # start date
    ed = datetime.strptime(end_date, '%Y-%m-%d').date()   # end date
    for name in file_list:
        match = re.search('\d{4}-\d{2}-\d{2}', name)
        date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        if sd <= date <= ed:
            filtered_dates.append(name)
    return filtered_dates


def obtenerListaArchivos(path: str):

    lista = glob.glob(path, recursive=True)

    return lista


def extraerWrfoutSerie(file_paths: str, x: int, y: int):
    dfData = pd.DataFrame()

    for f in file_paths:
        wrf_temp = Dataset(f)
        t2 = wrf.getvar(wrf_temp, "T2", timeidx=wrf.ALL_TIMES)
        wrf_temp.close()
        t2_ubp = t2[:, y, x]

        dfT2ubp = pd.DataFrame(t2_ubp.to_pandas(), columns=['T2'])
        dfT2ubp['T2'] = dfT2ubp['T2'] - 273.15

        dfData = pd.concat([dfData, dfT2ubp[9:33]])

    return dfData
