import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    layout="wide",
    page_title="Informacion de Productos",
    page_icon="📊",
    initial_sidebar_state="expanded")

# Title
st.title(':bar_chart: Informacion de Productos')
st.markdown('<style>body{background-color: #f0f0f5;}</style>', unsafe_allow_html=True)

FactInternetSales = pd.read_csv('data/FactInternetSales.csv')
FactResellerSales = pd.read_csv('data/FactResellerSales.csv')
DimProduct = pd.read_csv('data/DimProduct.csv')
DimProductCategory = pd.read_csv('data/DimProductCategory.csv')
DimProductSubcategory = pd.read_csv('data/DimProductSubcategory.csv')
DimSalesTerritory = pd.read_csv('data/DimSalesTerritory.csv')

# Merge de las tablas FactInternetSales y FactResellerSales
FactSales = pd.concat([FactInternetSales, FactResellerSales])

# Crear nuevas columnas de tiempo
FactSales['OrderDate'] = pd.to_datetime(FactSales['OrderDate'])
FactSales['Year'] = FactSales['OrderDate'].dt.year
FactSales['Month'] = FactSales['OrderDate'].dt.month
FactSales['YearMonth'] = FactSales['OrderDate'].dt.to_period('M').astype(str)

# Merge con las tablas de producto, subcategoría, categoría y territorio
FactSales = FactSales.merge(DimProduct, on='ProductKey') \
    .merge(DimProductSubcategory, on='ProductSubcategoryKey') \
    .merge(DimProductCategory, on='ProductCategoryKey') \
    .merge(DimSalesTerritory, on='SalesTerritoryKey')

regions = FactSales['SalesTerritoryRegion'].unique()
countries = FactSales['SalesTerritoryCountry'].unique()
years = FactSales['Year'].unique()
months = FactSales['Month'].unique()

# Filtros Interactivos
st.sidebar.title('Filtros')
region = st.sidebar.multiselect('Selecciona una Región', regions, default=regions)
country = st.sidebar.multiselect('Selecciona un País', countries, default=countries)
selected_year = st.sidebar.multiselect('Selecciona un Año', options=years, default=years)
selected_month = st.sidebar.multiselect('Selecciona un Mes', options=months, default=months)

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

productos_por_categoria = FactSales_filtered.groupby(['EnglishProductCategoryName', 'EnglishProductSubcategoryName'])[
    'SalesAmount'].sum().reset_index()
productos_por_categoria = productos_por_categoria.sort_values(by='SalesAmount', ascending=False).reset_index(drop=True)

c1, c2 = st.columns((0.5, 0.5), gap="large")
with c1:
    # Plot del total de productos por categoría vendidos
    fig = px.bar(productos_por_categoria, x='EnglishProductCategoryName', y='SalesAmount', text='SalesAmount',
                 color='EnglishProductCategoryName',
                 title='Total de productos por categoría vendidos')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)
with c2:
    # Plot del total de productos por subcategoría vendidos en tree map
    fig = px.treemap(productos_por_categoria, path=['EnglishProductCategoryName', 'EnglishProductSubcategoryName'],
                     values='SalesAmount',
                     title='Total de productos por subcategoría vendidos')
    st.plotly_chart(fig)

# Tabla resumen ordenada por producto más vendido
# Aplicar formato condicional para resaltar el producto más vendido (puedes usar una escala de colores).
FactSales['Profit'] = FactSales['SalesAmount'] - FactSales['TotalProductCost']
productos_por_subcategoria = FactSales_filtered.groupby('EnglishProductName')[
    ['SalesAmount', 'Profit', 'OrderQuantity']].sum().reset_index()
productos_por_subcategoria = productos_por_subcategoria.sort_values(by='SalesAmount', ascending=False)

# Aplicar formato condicional para resaltar el producto más vendido
fig = px.bar(productos_por_subcategoria.head(10), x='EnglishProductName', y='SalesAmount', text='SalesAmount',
             color='SalesAmount',
             title='Productos más vendidos')
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig)

# Tabla resumen ordenada por producto más vendido
st.subheader('Productos más vendidos')
st.dataframe(productos_por_subcategoria.head(15))
# Separador
st.markdown(
    """
    <style>
        .separator {
            margin-top: 20px;
            margin-bottom: 20px;
            padding: 0;
            height: 1px;
            background-color: #e6e6e6;
            border: none;
        }
    </style>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)

# Gráfico de composición por territorio de ventas del total de ventas generadas (torta, anillo, treemap)
ventas_por_territorio = FactSales.groupby('SalesTerritoryCountry')['SalesAmount'].sum().reset_index()
ventas_por_territorio = ventas_por_territorio.sort_values(by='SalesAmount', ascending=False)

c1, c2 = st.columns((0.5, 0.5), gap="large")
with c1:
    # Plot del total de ventas por territorio
    fig = px.pie(ventas_por_territorio, values='SalesAmount', names='SalesTerritoryCountry',
                 title='Total de ventas por territorio')
    st.plotly_chart(fig)

ventas_por_territorio = FactSales.groupby(['SalesTerritoryGroup', 'SalesTerritoryRegion', 'SalesTerritoryCountry'])[
    'SalesAmount'].sum().reset_index()
ventas_por_territorio = ventas_por_territorio.sort_values(by='SalesAmount', ascending=False)

with c2:
    # Plot del total de ventas por territorio teniendo en cuenta el grupo, region y pais
    fig = px.treemap(ventas_por_territorio, path=['SalesTerritoryGroup', "SalesTerritoryCountry", 'SalesTerritoryRegion'],
                     values='SalesAmount',
                     title='Total de ventas por territorio')
    st.plotly_chart(fig)

st.markdown('---')

# Gráfico de comparación en el tiempo de las ventas por categoría
ventas_por_categoria = FactSales.groupby(['YearMonth', 'EnglishProductCategoryName'])['SalesAmount'].sum().reset_index()
ventas_por_categoria = ventas_por_categoria.sort_values(by='YearMonth', ascending=True)

# Plot del total de ventas por mes y categoría
fig = px.line(ventas_por_categoria, x='YearMonth', y='SalesAmount', color='EnglishProductCategoryName',
              title='Total de ventas por mes y categoría')
st.plotly_chart(fig)

# Gráfico de comparación en el tiempo de las ventas por subcategoría
ventas_por_subcategoria = FactSales.groupby(['YearMonth', 'EnglishProductSubcategoryName'])[
    'SalesAmount'].sum().reset_index()
ventas_por_subcategoria = ventas_por_subcategoria.sort_values(by='YearMonth', ascending=True)

# Plot del total de ventas por mes y subcategoría
fig = px.line(ventas_por_subcategoria, x='YearMonth', y='SalesAmount', color='EnglishProductSubcategoryName',
              title='Total de ventas por mes y subcategoría')
st.plotly_chart(fig)

st.markdown(
    """
    <style>
        .separator {
            margin-top: 20px;
            margin-bottom: 20px;
            padding: 0;
            height: 1px;
            background-color: #e6e6e6;
            border: none;
        }
    </style>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)
# Gráfico de comparación de las ventas por territorio y categoría
ventas_por_territorio_categoria = FactSales.groupby(['SalesTerritoryCountry', 'EnglishProductCategoryName'])[
    'SalesAmount'].sum().reset_index()
ventas_por_territorio_categoria = ventas_por_territorio_categoria.sort_values(by='SalesAmount', ascending=False)

st.subheader('Ventas por Territorio y Categoría')
c1, c2 = st.columns((0.5, 0.5), gap="large")
with c1 :
    fig = px.treemap(ventas_por_territorio_categoria, path=['SalesTerritoryCountry', 'EnglishProductCategoryName'],
                     values='SalesAmount',
                     title='Total de ventas por territorio y categoría')
    st.plotly_chart(fig)

# # Plot del total de ventas por territorio y categoría
# fig = px.bar(ventas_por_territorio_categoria, x='SalesTerritoryCountry', y='SalesAmount', text='SalesAmount',
#              color='EnglishProductCategoryName',
#              title='Total de ventas por territorio y categoría')
# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
# fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
# st.plotly_chart(fig)

# Gráfico de comparación de las ventas por territorio y subcategoría
ventas_por_territorio_subcategoria = FactSales.groupby(['SalesTerritoryCountry', 'EnglishProductSubcategoryName'])[
    'SalesAmount'].sum().reset_index()
ventas_por_territorio_subcategoria = ventas_por_territorio_subcategoria.sort_values(by='SalesAmount', ascending=False)

with c2:
    # Plot del total de ventas por territorio y subcategoría
    fig = px.bar(ventas_por_territorio_subcategoria, x='SalesTerritoryCountry', y='SalesAmount', text='SalesAmount',
                 color='EnglishProductSubcategoryName',
                 title='Total de ventas por territorio y subcategoría')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)
