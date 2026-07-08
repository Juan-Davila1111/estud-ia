"""
Limpieza y normalización de datos de una tienda de café.

Este script procesa el archivo `data/tienda_cafe.csv` y corrige
inconsistencias en las columnas `producto`, `precio` y `fecha`.

Utiliza la distancia de Levenshtein para agrupar valores escritos
de forma similar (ej: "Machiato" → "Macchiato") y normaliza
tildes, mayúsculas/minúsculas y formatos de fecha.
"""

import pandas as pd
from pandas import DataFrame
import numpy as np

df = pd.read_csv("./data/tienda_cafe.csv")


def distancia(a: str, b: str) -> int:
    """
    Calcula la distancia de Levenshtein entre dos cadenas.

    La distancia de Levenshtein es el número mínimo de operaciones
    (inserción, eliminación, sustitución) necesarias para transformar
    una cadena en otra.

    Args:
        a: Primera cadena.
        b: Segunda cadena.

    Returns:
        Distancia de Levenshtein (int).

    Example:
        >>> distancia("Latte", "Late")
        1
    """
    previo = np.arange(len(b) + 1)

    for i, ca in enumerate(a, 1):
        current = np.zeros(len(b) + 1)
        current[0] = i
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            current[j] = min(current[j - 1] + 1, previo[j] + 1, previo[j - 1] + cost)
        previo = current

    return previo[-1]


def limpiar(
    df: DataFrame, col: str, umbral: int = 10, distancia_max: int = 4
) -> DataFrame:
    """
    Limpia y normaliza una columna del DataFrame agrupando valores similares.

    El proceso sigue estos pasos:
    1. Calcula la frecuencia de cada valor único en la columna.
    2. Normaliza los valores (minúsculas, sin tildes, sin espacios).
    3. Agrupa variantes normalizadas y usa el valor más frecuente como
       representante.
    4. Reemplaza los valores originales por su versión normalizada.
    5. Identifica valores "raros" (baja frecuencia) y "frecuentes" (alta
       frecuencia).
    6. Para cada valor raro, calcula la distancia de Levenshtein contra
       los valores frecuentes; si está dentro de `distancia_max`, lo
       reemplaza por el más cercano.

    Args:
        df: DataFrame con los datos a limpiar.
        col: Nombre de la columna a procesar.
        umbral: Frecuencia mínima para considerar un valor como
            "frecuente" (default: 10).
        distancia_max: Distancia máxima de Levenshtein para considerar
            dos valores como el mismo (default: 4).

    Returns:
        DataFrame con la columna corregida.
    """
    tabla = df[col].value_counts().reset_index()
    tabla.columns = [col, "cuenta"]

    normalize = (
        tabla[col]
        .str.lower()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", "ignore")
        .str.decode("utf-8")
    )
    cantidad = (
        tabla.assign(normalize=normalize)
        .sort_values("cuenta", ascending=False)
        .groupby("normalize")[col]
        .first()
    )
    df[col] = df[col].replace(dict(zip(cantidad), normalize.map(cantidad)))
    frecuencia = tabla.loc[tabla["cuenta"] > umbral, col].to_numpy()
    raros = tabla.loc[tabla["cuenta"] < umbral, col].to_numpy()

    correciones = {}

    for i in raros:
        distancia = np.array([distancia(i, j) for j in frecuencia])
        if distancia.min() <= distancia_max:
            correciones[i] = frecuencia[distancia.argmin()]
    return df.replace({col: correciones})


for col in ["producto", "precio", "fecha"]:
    df = limpiar(df, col)

print(df["producto"].value_counts())
print(df["precio"].value_counts())
print(df["fecha"].value_counts())
