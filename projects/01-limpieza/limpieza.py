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
        distancias = np.array(
            [distancia(valor, frecuente) for frecuente in frecuencia]
        )

        if len(distancias) > 0 and distancias.min() <= distancia_max:
            correcciones[valor] = frecuencia[distancias.argmin()]

    df[col] = df[col].replace(correcciones)

    return df


for columna in ["producto", "metodo_pago", "ciudad"]:
    df = limpiar(df, columna)

print(df["producto"].value_counts())
print(df["metodo_pago"].value_counts())
print(df["ciudad"].value_counts())