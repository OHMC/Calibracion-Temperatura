import numpy as np
import pandas as pd


def fromCSVtoDF(csvpath):
    """ Obtirene un path a un csv de una AWS
    y lo convierte en un df con su valores en float
    """
    try:
        csv_data = pd.read_csv(csvpath)
    except IOError:
        print("Error: File does not appear to exist.")

    dfData = pd.DataFrame(dtype=float)
    dfData['date'] = pd.to_datetime(csv_data['Fecha'], format='%d-%m-%Y %H:%M')
    # dfData['ppn'] = csv_data['Registro de Lluvia [mm]']
    dfData['Temp'] = csv_data['Temperatura [°C]']

    dfData['Temp'] = dfData['Temp'].astype(float)

    return dfData.set_index('date')


def getAWSvsWRF(dfWRF, dfAWS, awsname, param):
    """ Utilizando los indexes, arma pares WRF-AWS
    y los guarda en un dataframe dfTmp
    """
    dfTmp = pd.DataFrame()
    fieldname = f'WRF_{awsname}_{param}'

    for index, Temp in dfWRF.iterrows():
        try:
            a = dfAWS.loc[index]
        except KeyError as error:
            print(f"Index Error: {error}")
            continue

        dfTmp = dfTmp.append({'date': index,
                              fieldname: float(Temp[0]),
                              'AWS': float(a['Temp'])},
                             ignore_index=True)

    return dfTmp


def getMetricas(dfWRF_AWS, awsname, param):
    """ Esta funcion obtiene un dataframe con WRF y AWS en un punto
    y calcula la RMSE, MAE y devuelve un DF con el error
    agrupado por hora
    """
    error = dfWRF_AWS[f'WRF_{awsname}_{param}'] - dfWRF_AWS['AWS']

    rmse = np.sqrt(np.mean(error**2))

    mae = np.sum(np.absolute(error))/error.size

    dfError = pd.DataFrame({'date': dfWRF_AWS['date'], f'WRF_{awsname}_{param}': error})
    data = dfError.groupby([dfError["date"].dt.hour]).mean()

    return data, rmse, mae
