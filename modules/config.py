# modules/config.py

import streamlit as st
import pandas as pd
import os

# Define la ruta base del proyecto de forma robusta
# Asume que los archivos de datos están en 'data' y los módulos en 'modules'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    # Nombres de Columnas de Datos
    STATION_NAME_COL = 'nom_est'
    PRECIPITATION_COL = 'precipitation'
    LATITUDE_COL = 'latitud_geo'
    LONGITUDE_COL = 'longitud_geo'
    YEAR_COL = 'año'
    MONTH_COL = 'mes'
    DATE_COL = 'fecha_mes_año'
    ENSO_ONI_COL = 'anomalia_oni'
    ORIGIN_COL = 'origen'
    ALTITUDE_COL = 'alt_est'
    MUNICIPALITY_COL = 'municipio'
    REGION_COL = 'depto_region'
    PERCENTAGE_COL = 'porc_datos'
    CELL_COL = 'celda_xy'
    # Índices climáticos
    SOI_COL = 'soi'
    IOD_COL = 'iod'
    
    # Rutas de Archivos (usando la ruta absoluta)
    LOGO_PATH = os.path.join(BASE_DIR, "data", "Cuenca Verde_Logo.jpg")
    LOGO_DROP_PATH = os.path.join(BASE_DIR, "data", "Cuenca Verde_Logo.jpg")
    GIF_PATH = os.path.join(BASE_DIR, "data", "PPAM.gif")

    # Mensajes de la UI
    APP_TITLE = "Sistema de información de las lluvias y el Clima en el norte de la región Andina"
    WELCOME_TEXT = """
    Esta plataforma interactiva está diseñada para la visualización y análisis de datos históricos de
    precipitación y su
    relación con el fenómeno ENSO en el norte de la región Andina.
    **¿Cómo empezar?**
    """
    
    @staticmethod
    def initialize_session_state():
        """Inicializa todas las variables necesarias en el estado de la sesión de Streamlit."""
        state_defaults = {
            'data_loaded': False,
            'analysis_mode': "Usar datos originales",
            'select_all_checkbox': True,
            'filtered_station_options': [],
            'station_multiselect': [],
            'df_monthly_processed': pd.DataFrame(),
            'gdf_stations': None,
            'df_precip_anual': None,
            'gdf_municipios': None,
            'df_long': None,
            'df_enso': None,
            'min_data_perc_slider': 0,
            'altitude_multiselect': [],
            'regions_multiselect': [],
            'municipios_multiselect': [],
            'celdas_multiselect': [],
            'exclude_na': False,
            'exclude_zeros': False,
            'uploaded_forecast': None,
            'sarima_forecast': None,
            'prophet_forecast': None,
            'year_range': (1970, 2021),
            'meses_nombres': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            'meses_numeros': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        }
        for key, value in state_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
