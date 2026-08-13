import pandas as pd
from pandas import DataFrame

products_source = "./data/data-source/productos_petshop.csv"
products_output_source = "./data/data-output/productos.csv"

clients_source = "./data/data-source/clientes_petshop.csv"
clients_output_source = "./data/data-output/clientes.csv"

sales_source = "./data/data-source/ventas_petshop.csv"
sales_output_source = "./data/data-output/sales.csv"

def capitalize_column(df: DataFrame, column: str) -> DataFrame: 
    df[column] = df[column].str.capitalize()
    return df

def save_csv(df: DataFrame, source_destination: str) -> None:
    df.to_csv(source_destination, index=False)
    print("Datos guardados exitosamente.")
    
def fill_nulls_from_column(df: DataFrame, column: str, value) -> DataFrame:
    df[column] = df[column].fillna(value)
    return df

products = pd.read_csv(products_source)
products = capitalize_column(products, "categoria")


clients = pd.read_csv(clients_source)
clients = capitalize_column(clients, "ciudad")
clients = fill_nulls_from_column(clients, "ciudad", "Ciudad no especificada")
clients = fill_nulls_from_column(clients, "email", "Sin correo")

sales = pd.read_csv(sales_source)
sales = fill_nulls_from_column(sales, "cantidad", 0)
sales["cantidad"] = sales["cantidad"].astype(int)
sales = sales[sales["cantidad"] > 0]

save_csv(products, products_output_source)
save_csv(clients, clients_output_source)
save_csv(sales, sales_output_source)