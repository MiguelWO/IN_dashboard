from sqlalchemy import create_engine
import pandas as pd


def get_data():
    SERVER = 'localhost'
    DATABASE = 'AdventureWorksDW2022'

    connection_string = f"mssql+pyodbc://{SERVER}/{DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"

    engine = create_engine(connection_string)

    tables = ["DimCurrency", "DimCustomer", "DimDate", "DimEmployee",
              "DimGeography", "DimProduct", "DimProductCategory", "DimProductSubcategory",
              "DimPromotion", "DimSalesTerritory", "FactInternetSales", "FactResellerSales"]

    for table in tables:
        df = pd.read_sql(f'SELECT * FROM {table}', engine)
        print(f"Table: {table}")
        print(df.head())
        print("\n")

        #     Guardar to CSV in folder data
        df.to_csv(f'data/{table}.csv', index=False)

    engine.dispose()


def main():
    get_data()


if __name__ == '__main__':
    main()
