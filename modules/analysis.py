# modules/analysis.py

import pandas as pd
import numpy as np
import streamlit as st
from scipy.stats import gamma, norm
from modules.config import Config

@st.cache_data
def calculate_spi(series, window):
    """
    Calcula el Índice Estandarizado de Precipitación (SPI) para una serie de tiempo.
    Requiere que la serie esté en formato Series de Pandas con índice de tiempo (Fecha).
    """
    # 1. Calcula la suma móvil de la precipitación
    # Usamos .sort_index() para asegurar el orden correcto del rolling window
    rolling_sum = series.sort_index().rolling(window, min_periods=window).sum()
    
    # 2. Ajusta una distribución Gamma a los datos de la suma móvil
    # Usamos floc=0 ya que la suma de precipitación no puede ser negativa
    try:
        params = gamma.fit(rolling_sum.dropna(), floc=0)
        shape, loc, scale = params
    except Exception as e:
        # En caso de que el ajuste falle por datos insuficientes o atípicos
        st.error(f"Error al ajustar la distribución Gamma para SPI-{window}: {e}")
        return pd.Series(np.nan, index=series.index)
    
    # 3. Calcula la probabilidad acumulada (CDF) con la distribución Gamma
    cdf = gamma.cdf(rolling_sum, shape, loc=loc, scale=scale)
    
    # 4. Transforma la probabilidad acumulada a una distribución normal estándar (Z-score)
    spi = norm.ppf(cdf)
    
    # 5. Manejo de valores infinitos (puede ocurrir en los extremos de la distribución)
    spi = np.where(np.isinf(spi), np.nan, spi)
    
    # Reconvertir a Series usando el índice de rolling_sum
    return pd.Series(spi, index=rolling_sum.index)


@st.cache_data
def calculate_monthly_anomalies(df_monthly_filtered, df_long):
    """
    Calcula la anomalía de la precipitación mensual respecto a la climatología
    histórica del DataFrame base (df_long).
    
    df_monthly_filtered: Datos actuales filtrados por rango temporal/estaciones.
    df_long: DataFrame base con todos los datos históricos (para climatología).
    """
    # 1. Determinar la climatología del período histórico completo (df_long)
    # Se usa df_long para tener una base climatológica estable.
    # Se asegura que solo se usen las estaciones seleccionadas para el análisis climatológico
    stations_in_filter = df_monthly_filtered[Config.STATION_NAME_COL].unique()
    
    df_climatology = df_long[
        df_long[Config.STATION_NAME_COL].isin(stations_in_filter)
    ].groupby([Config.STATION_NAME_COL, Config.MONTH_COL])[Config.PRECIPITATION_COL].mean() \
     .reset_index().rename(columns={Config.PRECIPITATION_COL: 'precip_promedio_mes'})

    # 2. Fusionar la climatología con los datos filtrados (df_monthly_filtered)
    df_anomalias = pd.merge(
        df_monthly_filtered, 
        df_climatology, 
        on=[Config.STATION_NAME_COL, Config.MONTH_COL], 
        how='left'
    )

    # 3. Calcular la anomalía
    df_anomalias['anomalia'] = df_anomalias[Config.PRECIPITATION_COL] - df_anomalias['precip_promedio_mes']
    
    # 4. Asegurar que la columna ENSO_ONI (si existe) se mantenga
    if Config.ENSO_ONI_COL in df_monthly_filtered.columns:
        # Se toma la primera anomalía ONI por fecha, ya que es un valor único mensual
        enso_info = df_monthly_filtered[[Config.DATE_COL, Config.ENSO_ONI_COL]].drop_duplicates(subset=[Config.DATE_COL])
        df_anomalias = pd.merge(df_anomalias, enso_info, on=Config.DATE_COL, how='left', suffixes=('_anom', '_enso'))
        
        # Eliminar columna duplicada o renombrar si es necesario, priorizando la ENSO
        # del df_anomalias si ya se fusionó, o la columna '_enso' si es nueva.
        # Si Config.ENSO_ONI_COL existía antes, usamos la columna fusionada.
        if Config.ENSO_ONI_COL + '_anom' in df_anomalias.columns:
             df_anomalias[Config.ENSO_ONI_COL] = df_anomalias[Config.ENSO_ONI_COL + '_anom'].fillna(df_anomalias[Config.ENSO_ONI_COL + '_enso'])
             df_anomalias.drop(columns=[Config.ENSO_ONI_COL + '_anom', Config.ENSO_ONI_COL + '_enso'], inplace=True)


    return df_anomalias.copy()
