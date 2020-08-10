import numpy as np
import pandas as pd


def getAWSvsWRF(dfWRF, dfAWS, awsname, param):
    """ Utilizando los indexes, arma pares WRF-AWS
    y los guarda en un dataframe dfTmp
    """
    dfTmp = pd.DataFrame()

    for index, Temp in dfWRF.iterrows():
        try:
            a = dfAWS.loc[index]
        except KeyError as error:
            print(f"Index Error: {error}")
            continue

        dfTmp = dfTmp.append({'date': index,
                              'f"WRF_{awsname}_{param}"': float(Temp[0]),
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

    dfError = pd.DataFrame({'date': dfWRF_AWS['date'], 'WRF_60_A': error})
    data = dfError.groupby([dfError["date"].dt.hour]).mean()

    return data, rmse, mae
