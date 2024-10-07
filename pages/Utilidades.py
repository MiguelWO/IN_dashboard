import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    layout="wide",
    page_title="Analisis de Utilidades",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded")

st.title(':bar_chart: Analisis de Utilidades')
st.markdown('<style>body{background-color: #f0f0f5;}</style>', unsafe_allow_html=True)

FactInternetSales = pd.read_csv('data/FactInternetSales.csv')
FactResellerSales = pd.read_csv('data/FactResellerSales.csv')
DimSalesTerritory = pd.read_csv('data/DimSalesTerritory.csv')

# Merge de las tablas FactInternetSales y FactResellerSales
FactSales = pd.concat([FactInternetSales, FactResellerSales])

# Agrupar por año y mes
FactSales['OrderDate'] = pd.to_datetime(FactSales['OrderDate'])
FactSales['Year'] = FactSales['OrderDate'].dt.year
FactSales['Month'] = FactSales['OrderDate'].dt.month
# Convert to str yearmonth
FactSales['YearMonth'] = FactSales['OrderDate'].dt.to_period('M')
FactSales['YearMonth'] = FactSales['YearMonth'].astype(str)

FactSales['Profit'] = FactSales['SalesAmount'] - FactSales['TotalProductCost']

# Merge con SalesTerritory
FactSales = pd.merge(FactSales, DimSalesTerritory, on='SalesTerritoryKey')

regions = FactSales['SalesTerritoryRegion'].unique()
countries = FactSales['SalesTerritoryCountry'].unique()

# Filtros Interactivos
st.sidebar.title('Filtros')
region = st.sidebar.multiselect('Selecciona una Región', regions, default=regions)
country = st.sidebar.multiselect('Selecciona un País', countries, default=countries)
selected_year = st.sidebar.multiselect('Selecciona un Año', options=FactSales['Year'].unique(), default= FactSales['Year'].unique())
selected_month = st.sidebar.multiselect('Selecciona un Mes', options=FactSales['Month'].unique(), default= FactSales['Month'].unique())

# Filtrar los datos
if not region:
    FactSales_filtered = FactSales
else:
    FactSales_filtered = FactSales[FactSales['SalesTerritoryRegion'].isin(region)]

if not country:
    FactSales_filtered = FactSales_filtered
else:
    FactSales_filtered = FactSales_filtered[FactSales_filtered['SalesTerritoryCountry'].isin(country)]

if not selected_year:
    FactSales_filtered = FactSales_filtered
else:
    FactSales_filtered = FactSales_filtered[FactSales_filtered['Year'].isin(selected_year)]

if not selected_month:
    FactSales_filtered = FactSales_filtered
else:
    FactSales_filtered = FactSales_filtered[FactSales_filtered['Month'].isin(selected_month)]

FactSales = FactSales_filtered

# Información referente al total de utilidades generadas
total_ventas = FactSales['SalesAmount'].sum()
total_costos = FactSales['TotalProductCost'].sum()
total_ganancias = total_ventas - total_costos
total_discount = FactSales['DiscountAmount'].sum()

c1, c2 = st.columns((0.6, 0.4), gap="large")
with c1:
    # Plot del total de utilidades generadas usando Plotly
    fig = go.Figure(go.Indicator(
        mode="number",
        value=total_ganancias,
        title={"text": "<b>Total de Ganancias</b>"},
        number={'prefix': "$", "font": {"size": 70, "color": "#4caf50"}},
    ))
    # fig.update_layout(title="Total de Ganancias")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    # Centrar el contenido y ajustar el estilo de los textos
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <p style="font-size: 18px;">El total de <b>ventas realizadas</b> por la empresa es de:</p>
            <h4 style="color: #27AE60;">${:,}</h4>
            <p style="font-size: 18px;">El total de <b>costos de los productos vendidos</b> es de:</p>
            <h4 style="color: #C0392B;">${:,}</h4>
            <p style="font-size: 18px;">El total de <b>descuentos aplicados</b> es de:</p>
            <h4 style="color: #F39C12;">${:,}</h4>
        </div>
        """.format(int(total_ventas), int(total_costos), int(total_discount)),
        unsafe_allow_html=True
    )

# Información referente a las utilidades por año
utilidades_por_ano = FactSales.groupby('Year')['SalesAmount'].sum().reset_index()

# Información referente a las utilidades por mes
utilidades_por_mes = FactSales.groupby('YearMonth')['SalesAmount'].sum().reset_index()

c1, c2 = st.columns((1, 1))
with c1:
    # Visualización de las utilidades por año
    fig1 = px.bar(utilidades_por_ano, x='Year', y='SalesAmount', title='Utilidades por Año')
    st.plotly_chart(fig1)

with c2:
    # Visualización de las utilidades por mes
    fig2 = px.line(utilidades_por_mes, x='YearMonth', y='SalesAmount', title='Utilidades por Mes')
    st.plotly_chart(fig2)

# Gráfico circular de comparación de ventas, costos y descuentos
fig = go.Figure(data=[go.Pie(labels=['Ventas', 'Costos', 'Descuentos'],
                             values=[total_ventas, total_costos, total_discount])])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
fig.update_layout(title='Comparación de Ventas, Costos y Descuentos')
st.plotly_chart(fig)

# Comparacion de Promedio por orden vs Promedios normales
# Agrupar por numero de orden
order_quantity = FactSales.groupby('SalesOrderNumber')[
    ['OrderQuantity', "SalesAmount", 'DiscountAmount', 'TotalProductCost']].sum().reset_index()

# Promedios
promedio_unidades = FactSales['OrderQuantity'].mean()
promedio_ventas = FactSales['SalesAmount'].mean()
promedio_descuentos = FactSales['DiscountAmount'].mean()
promedio_costos = FactSales['TotalProductCost'].mean()

# Promedios por orden
promedio_unidades_orden = order_quantity['OrderQuantity'].mean()
promedio_ventas_orden = order_quantity['SalesAmount'].mean()
promedio_descuentos_orden = order_quantity['DiscountAmount'].mean()
promedio_costos_orden = order_quantity['TotalProductCost'].mean()

# Comparacion de promedios
st.subheader('Comparación de Promedios por Orden vs Promedios Normales')
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <p style="font-size: 18px;">Promedio de <b>Unidades por Orden</b></p>
            <h4 style="color: #27AE60;">{:.2f}</h4>
            <p style="font-size: 18px;">Promedio de <b>Ventas por Orden</b></p>
            <h4 style="color: #27AE60;">${:.2f}</h4>
            <p style="font-size: 18px;">Promedio de <b>Descuentos por Orden</b></p>
            <h4 style="color: #27AE60;">${:.2f}</h4>
            <p style="font-size: 18px;">Promedio de <b>Costos por Orden</b></p>
            <h4 style="color: #27AE60;">${:.2f}</h4>
        </div>
        """.format(promedio_unidades_orden, promedio_ventas_orden, promedio_descuentos_orden, promedio_costos_orden),
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <p style="font-size: 18px;">Promedio de <b>Unidades</b></p>
            <h4 style="color: #C0392B;">{:.2f}</h4>
            <p style="font-size: 18px;">Promedio de <b>Ventas</b></p>
            <h4 style="color: #C0392B;">${:.2f}</h4>
            <p style="font-size: 18px;">Promedio de <b>Descuentos</b></p>
            <h4 style="color: #C0392B;">${:.2f}</h4>
            <p style="font-size: 18px;">Promedio de <b>Costos</b></p>
            <h4 style="color: #C0392B;">${:.2f}</h4>
        </div>
        """.format(promedio_unidades, promedio_ventas, promedio_descuentos, promedio_costos),
        unsafe_allow_html=True
    )
