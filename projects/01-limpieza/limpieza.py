"""
Limpieza y normalización de datos de una tienda de café.

Este script procesa el archivo `data/tienda_cafe.csv` y corrige
inconsistencias en las columnas `producto`, `precio` y `fecha`.

Utiliza la distancia de Levenshtein para agrupar valores escritos
de forma similar (ej: "Machiato" → "Macchiato") y normaliza
tildes, mayúsculas/minúsculas y formatos de texto.
"""

import pandas as pd
from pandas import DataFrame
import numpy as np

df = pd.read_csv("./data/tienda_cafe.csv")
pd.set_option("display.max_rows", 300)


def distancia(a: str, b: str) -> int:
    """
    Calcula la distancia de Levenshtein entre dos cadenas.

    La distancia de Levenshtein es el número mínimo de operaciones
    (inserción, eliminación y sustitución) necesarias para transformar
    una cadena en otra.

    Args:
        a: Primera cadena.
        b: Segunda cadena.

    Returns:
        Distancia de Levenshtein.

    Example:
        >>> distancia("Latte", "Late")
        1
    """
    previo = np.arange(len(b) + 1)

    for i, ca in enumerate(a, 1):
        actual = np.zeros(len(b) + 1, dtype=int)
        actual[0] = i

        for j, cb in enumerate(b, 1):
            costo = 0 if ca == cb else 1
            actual[j] = min(
                actual[j - 1] + 1,
                previo[j] + 1,
                previo[j - 1] + costo,
            )

        previo = actual

    return int(previo[-1])


def limpiar(
    df: DataFrame,
    col: str,
    umbral: int = 10,
    distancia_max: int = 4,
) -> DataFrame:
    """
    Limpia y normaliza una columna del DataFrame agrupando valores similares.

    El proceso realiza:

    1. Calcula la frecuencia de cada valor.
    2. Normaliza los textos (minúsculas, sin tildes y sin espacios).
    3. Conserva la variante más frecuente de cada grupo.
    4. Corrige valores poco frecuentes usando la distancia de
       Levenshtein.

    Args:
        df: DataFrame a procesar.
        col: Columna a limpiar.
        umbral: Frecuencia mínima para considerar un valor frecuente.
        distancia_max: Distancia máxima permitida para corregir un valor.

    Returns:
        DataFrame con la columna corregida.
    """

    # Convertir la columna a texto
    df[col] = df[col].astype(str)

    # Tabla de frecuencias
    tabla = df[col].value_counts().reset_index()
    tabla.columns = [col, "cuenta"]

    # Normalización
    normalize = (
        tabla[col]
        .str.lower()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", "ignore")
        .str.decode("utf-8")
    )

    # Valor más frecuente por cada texto normalizado
    cantidad = (
        tabla.assign(normalize=normalize)
        .sort_values("cuenta", ascending=False)
        .groupby("normalize")[col]
        .first()
    )

    # Normalizar la columna del DataFrame
    df[col] = (
        df[col]
        .str.lower()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", "ignore")
        .str.decode("utf-8")
    )

    # Reemplazar por el valor más frecuente
    df[col] = df[col].replace(cantidad.to_dict())

    # Recalcular frecuencias
    tabla = df[col].value_counts().reset_index()
    tabla.columns = [col, "cuenta"]

    frecuencia = tabla.loc[tabla["cuenta"] >= umbral, col].to_numpy()
    raros = tabla.loc[tabla["cuenta"] < umbral, col].to_numpy()

    correcciones = {}

    # Corregir valores poco frecuentes
    for valor in raros:
        distancias = np.array([distancia(valor, frecuente) for frecuente in frecuencia])

        if len(distancias) > 0 and distancias.min() <= distancia_max:
            correcciones[valor] = frecuencia[distancias.argmin()]

    df[col] = df[col].replace(correcciones)

    return df


for columna in ["producto", "metodo_pago", "ciudad"]:
    df = limpiar(df, columna)

meses = {
    "Ene": "Jan",
    "Feb": "Feb",
    "Mar": "Mar",
    "Abr": "Apr",
    "May": "May",
    "Jun": "Jun",
    "Jul": "Jul",
    "Ago": "Aug",
    "Sep": "Sep",
    "Oct": "Oct",
    "Nov": "Nov",
    "Dic": "Dec",
}

fecha_texto = df["fecha"].astype("string").replace(meses, regex=True)

formatos_conocidos = [
    # Día-Mes-Año
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d.%m.%Y",
    # Día-Mes-Año (año de 2 dígitos)
    "%d/%m/%y",
    "%d-%m-%y",
    "%d.%m.%y",
    # Año-Mes-Día
    "%Y/%m/%d",
    "%Y-%m-%d",
    "%Y.%m.%d",
    # Año-Mes-Día (año de 2 dígitos)
    "%y/%m/%d",
    "%y-%m-%d",
    "%y.%m.%d",
    # Día-Mes(abreviado)-Año
    "%d-%b-%Y",
    "%d/%b/%Y",
    "%d.%b.%Y",
    # Día-Mes(abreviado)-Año (2 dígitos)
    "%d-%b-%y",
    "%d/%b/%y",
    "%d.%b.%y",
    # Día-Mes(nombre completo)-Año
    "%d-%B-%Y",
    "%d/%B/%Y",
    # Año-Mes(abreviado)-Día
    "%Y-%b-%d",
    "%Y/%b/%d",
]

fechas_limpias = pd.Series(pd.NaT, dtype="datetime64[ns]", index=df.index)

for formato in formatos_conocidos:
    fechas_limpias.fillna(pd.to_datetime(fecha_texto, format=formato, errors="coerce"))

digitos = fecha_texto.str.isdigit().fillna(False)
pendientes = fechas_limpias.isna() & digitos

fechas_pendientes = fecha_texto[pendientes]

largo = fechas_pendientes.str.len()
years = fechas_pendientes[-4:]
resto = fechas_pendientes.str[:-4]

construida = pd.Series(pd.NaT, index=fechas_pendientes.index, dtype="datetime64[ns]")

m8 = largo == 8
construida.loc[m8] = pd.to_datetime(
    dict(
        year=years[m8].astype(int),
        month=resto[m8].str[2:].astype(int),
        day=resto[m8].str[:2].astype(int),
    ),
    errors="coerce",
).values

m6 = largo == 6
construida.loc[m6] = pd.to_datetime(
    dict(
        year=years[m6].astype(int),
        month=resto[m6].str[1:].astype(int),
        day=resto[m6].str[:1].astype(int),
    ),
    errors="coerce",
).values

m7 = largo == 7
intento_dia2 = pd.to_datetime(
    dict(
        year=years[m7].astype(int),
        month=resto[m7].str[2:].astype(int),
        day=resto[m7].str[:2].astype(int),
    ),
    errors="coerce",
)

intento_dia1 = pd.to_datetime(
    dict(
        year=years[m7].astype(int),
        month=resto[m7].str[1:].astype(int),
        day=resto[m7].str[:1].astype(int),
    ),
    errors="coerce",
)


construida.loc[m7] = intento_dia2.fillna(intento_dia1).values

fechas_limpias.loc[pendientes] = construida.values


df["fecha"] = fechas_limpias

# print(df["fecha"].value_counts())

df["calificacion"] = df["calificacion"].replace(
    {"★★★★": "4", "bueno": "3", "cinco": "5", "5 estrellas": "5"}
)

# print(df["calificacion"].head(100))


def limpiar_hora(hora):
    if pd.isna(hora):
        return hora

    hora = str(hora).strip().lower()
    if "am" in hora or "pm" in hora:
        if "am" in hora and int(hora.split(":")[0] == 12):
            hora = hora.replace("12", "00")
    elif "pm" in hora and int(hora.split(":")[0]) != 12:
        hora = str(int(hora.split(":")[0]) + 12) + ":" + hora.split(":")[1]
    hora = hora.replace("am", "").replace("pm", "").replace(".", ":").replace(",", ":")
    if ":" not in hora:
        hora = hora[:-2] + ":" + hora[-2:]
    return hora


df["hora"] = df["hora"].apply(limpiar_hora)

df["hora"] = pd.to_datetime(df["hora"], format="%H:%M", errors="coerce").dt.time
print(df["hora"].value_counts())

df.to_csv('./data/tienda_cafe_limpia.csv', index=False)