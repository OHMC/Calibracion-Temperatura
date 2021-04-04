import pandas as pd

def getDataBetweenDates(wrfA: pd.DataFrame, wrfB: pd.DataFrame,
                        wrfC: pd.DataFrame, wrfD: pd.DataFrame,
                        start_date, end_date):
    wrfA_mask = (wrfA.index > start_date) & (wrfA.index < end_date)
    wrfA_val = wrfA.loc[wrfA_mask]
wrf_LH_B_T2_18_val_mask = (wrf_LH_T2_B_18.index > start_date) & (wrf_LH_T2_B_18.index < end_date)
wrf_LH_B_T2_18_val = wrf_LH_T2_B_18.loc[wrf_LH_B_T2_18_val_mask]
wrf_LH_C_T2_18_val_mask = (wrf_LH_T2_C_18.index > start_date) & (wrf_LH_T2_C_18.index < end_date)
wrf_LH_C_T2_18_val = wrf_LH_T2_C_18.loc[wrf_LH_C_T2_18_val_mask]
wrf_LH_D_T2_18_val_mask = (wrf_LH_T2_D_18.index > start_date) & (wrf_LH_T2_D_18.index < end_date)
wrf_LH_D_T2_18_val = wrf_LH_T2_D_18.loc[wrf_LH_D_T2_18_val_mask]