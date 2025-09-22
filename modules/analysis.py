# modules/analysis.py

import pandas as pd
import numpy as np
from scipy.stats import gamma, norm
from modules.config import Config
from modules.utils import calculate_climatology # Se añadirá esta función en el paso 1.1

def calculate_spi(series, window):
    """
    Calcula el Índice Estandarizado de Precipitación (SPI) para una serie de tiempo.
    Requiere que la serie esté en formato Series de Pandas con índice de tiempo.
    """
    # 1. Calcula la suma móvil de la precipitación [cite: 236, 237]
    # Se usa .sort_index() para evitar problemas con rolling window en series desordenadas
    rolling_sum = series.sort_index().rolling(window, min_periods=window).sum()
    
    # 2. Ajusta una distribución Gamma a los datos de la suma móvil [cite: 238]
    # Se usa floc=0 porque la precipitación (o suma de precipitación) no puede ser negativa
    params = gamma.fit(rolling_sum.dropna(), floc=0)
    shape, loc, scale = params [cite: 239]
    
    # 3. Calcula la probabilidad acumulada (CDF) con la distribución Gamma [cite: 240, 241]
    cdf = gamma.cdf(rolling_sum, shape, loc=loc, scale=scale)
    
    # 4. Transforma la probabilidad acumulada a una distribución normal estándar (Z-score) [cite: 242]
    spi = norm.ppf(cdf)
    
    # 5. Manejo de valores infinitos (que pueden ocurrir en los extremos) [cite: 243]
    spi = np.where(np.isinf(spi), np.nan, spi)
    
    # Reconvertir a Series usando el índice original
    return pd.Series(spi, index=rolling_sum.index) [cite: 244, 245]

def calculate_monthly_anomalies(df_monthly_filtered, df_long):
    """
    Calcula la anomalía de la precipitación mensual respecto a la climatología
    histórica del DataFrame base (df_long).
    """
    # 1. Determinar la climatología del período histórico completo (df_long)
    # df_long es el DataFrame original cargado, usado como referencia climatológica
    df_climatology = df_long[
        df_long[Config.STATION_NAME_COL].isin(df_monthly_filtered[Config.STATION_NAME_COL].unique())
    ].groupby([Config.STATION_NAME_COL, Config.MONTH_COL])[Config.PRECIPITATION_COL].mean() \
     .reset_index().rename(columns={Config.PRECIPITATION_COL: 'precip_promedio_mes'}) [cite: 1343, 1344]

    # 2. Fusionar la climatología con los datos filtrados (df_monthly_filtered)
    df_anomalias = pd.merge(
        df_monthly_filtered, 
        df_climatology, 
        on=[Config.STATION_NAME_COL, Config.MONTH_COL], 
        how='left'
    ) [cite: 1345]

    # 3. Calcular la anomalía [cite: 1346]
    df_anomalias['anomalia'] = df_anomalias[Config.PRECIPITATION_COL] - df_anomalias['precip_promedio_mes']
    
    return df_anomalias.copy()
