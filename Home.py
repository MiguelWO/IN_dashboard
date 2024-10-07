import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(
    layout="wide",
    page_title="Tablero BI Adventure Works 2022",
    page_icon="📊",
    initial_sidebar_state="expanded")

# Title
st.title(':bar_chart: Tablero BI Adventure Works 2022')
st.markdown('<style>body{background-color: #f0f0f5;}</style>',unsafe_allow_html=True)
st.image('data/logo.png')
st.write('Este tablero de control es una herramienta de Business Intelligence que permite visualizar y analizar los datos de la empresa Adventure Works Cycles. La información se ha obtenido de la base de datos de la empresa y se ha procesado para su análisis. A continuación, se presentan las visualizaciones de los datos más relevantes de la empresa.')

