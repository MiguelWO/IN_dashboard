import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def get_data():
    SERVER = 'localhost'
    DATABASE = 'AdventureWorksDW2022'

    USERNAME = 'LAPTOP-4TDJEBQ5/wmigu'
    PASSWORD = '409779'

    connectionString = (
        f'DRIVER=ODBC Driver 17 for SQL Server;'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        'Trusted_Connection=yes;'
    )

    conn = pyodbc.connect(connectionString)

    tables = ["DimCurrency", "DimCustomer", "DimDate", "DimEmployee",
              "DimGeography", "DimProduct", "DimProductCategory", "DimProductSubcategory",
              "DimPromotion", "DimSalesTerritory", "FactInternetSales", "FactResellerSales"]

    for table in tables:
        df = pd.read_sql(f'SELECT * FROM {table}', conn)
        print(f"Table: {table}")
        print(df.head())
        print("\n")

        #     Guardar to CSV in folder data
        df.to_csv(f'data/{table}.csv', index=False)

    conn.close()


def main():
    get_data()


if __name__ == '__main__':
    main()
