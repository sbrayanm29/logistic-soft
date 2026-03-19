import pandas as pd

def normalizar_articulo(col):

    col = col.astype(str)
    col = col.str.replace(".0", "", regex=False)
    col = col.str.strip()

    return col


def limpiar_columnas(df):

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace("á","a")
        .str.replace("é","e")
        .str.replace("í","i")
        .str.replace("ó","o")
        .str.replace("ú","u")
    )

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    return df