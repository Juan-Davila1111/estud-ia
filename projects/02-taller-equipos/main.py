import numpy as np
import pandas as pd
from rapidfuzz import process, utils  # ¡Mucho más rápido que Levenshtein a mano!

# -----------------------------------------------------------------------------
# 1. Cargar datos e Inicializar Catálogo
# -----------------------------------------------------------------------------
df = pd.read_csv("./data/dataframe.csv")
pd.set_option("display.max_rows", 300)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_seq_items', None)

catalogo = [
    "Bad Bunny",
    "Shakira",
    "Metallica",
    "Grupo Niche",
    "Carlos Vives",
    "Maluma",
    "Feid",
    "J Balvin",
    "Mozart",
]

# Mapeo precalculado: { 'bad bunny': 'Bad Bunny', 'shakira': 'Shakira' ... }
# Usamos el procesador de rapidfuzz que limpia el texto eficientemente
catalogo_normalizado = {utils.default_process(a): a for a in catalogo}


# -----------------------------------------------------------------------------
# 2. Funciones de Limpieza Optimizadas
# -----------------------------------------------------------------------------
def normalizar_columna_vectorizada(serie: pd.Series) -> pd.Series:
    """Normaliza una serie completa usando métodos vectorizados de Pandas."""
    return (
        serie.astype(str)
        .str.lower()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )


def corregir_artista(nombre: str) -> str:
    """Busca el match más cercano usando RapidFuzz en C (veloz)."""
    if pd.isna(nombre) or str(nombre).strip() == "":
        return np.nan

    nombre_limpio = utils.default_process(nombre)

    # Encuentra la mejor coincidencia en nuestro diccionario precalculado
    match, score, _ = process.extractOne(
        nombre_limpio, catalogo_normalizado.keys()
    )

    # Si el match es medianamente decente (score > 60), devolvemos el nombre real
    return catalogo_normalizado[match] if score > 60 else np.nan


# -----------------------------------------------------------------------------
# 3. Ejecución del Pipeline
# -----------------------------------------------------------------------------

# Columnas estándar
columnas_texto = [
    "ciudad",
    "genero_musical",
    "plataforma",
    "dispositivo",
    "nivel_educativo",
]
for col in columnas_texto:
    if col in df.columns:
        df[col] = normalizar_columna_vectorizada(df[col]).str.capitalize()

# Artistas favoritos (Corrección inteligente rápida)
if "artista_favorito" in df.columns:
    df["artista_favorito"] = df["artista_favorito"].apply(corregir_artista)

# Edad (Limpieza limpia con Regex vectorizado)
if "edad" in df.columns:
    # Reemplazos rápidos
    df["edad"] = df["edad"].astype(str).str.lower().replace({"veintiocho": "28"})

    # Extrae el primer grupo de números que encuentre en el string
    df["edad"] = df["edad"].str.extract(r"(\d+)").astype("Int64")

    # NOTA: Dejar como NaN es mejor que poner 0, pero si insisten en llenar:
    # df['edad'] = df['edad'].fillna(df['edad'].median()).astype(int)
    
print(df["edad"].value_counts())