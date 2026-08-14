import pandas as pd
from pandas import DataFrame


def load_csv(file_source: str) -> DataFrame:
    try:
        return pd.read_csv(file_source)
    except FileNotFoundError:
        return pd.DataFrame({"documento": [], "nombre": [], "edad": [], "ciudad": []})


def save_csv(df: DataFrame, source: str):
    df.to_csv(source, index=False)
    print("Datos guardados exitosamente.")
    return


def add_user(
    df: DataFrame, documento: int, nombre: str, edad: int, ciudad: str
) -> DataFrame:

    if df["documento"].eq(documento).any():
        print("El documento debe de ser único")
        return df

    df.loc[len(df)] = {
        "documento": documento,
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad,
    }
    print("Usuario creado exitosamente.")
    return df


def delete_user(df: DataFrame, documento: int) -> DataFrame:
    if not df["documento"].eq(documento).any():
        print("No hay usuario con ese documento.")
        return df
    
    df.drop(df[df["documento"] == documento].index, inplace=True)
    print("Usuario eliminado exitosamente.")
    return df


def list_users(df: DataFrame) -> None:

    if len(df) == 0:
        print("No hay registros.")
        return

    print("Listado de usuarios:")

    for documento, nombre, edad, ciudad in df[
        ["documento", "nombre", "edad", "ciudad"]
    ].itertuples(index=False, name=None):
        print(f"""
              Documento: {documento},
              Nombre: {nombre},
              Edad: {edad},
              Ciudad: {ciudad}
              """)
    return


def get_user(df: DataFrame, documento: int):
    user = df[df["documento"] == documento]

    if user.empty:
        print(f"Usuario con documento {documento} no encontrado.")
        return

    user = user.iloc[0]

    print(f"""
          Usuario:
            Documento: {user["documento"]}
            Nombre: {user["nombre"]}
            edad: {user["edad"]}
            ciudad: {user["ciudad"]}
          """)
