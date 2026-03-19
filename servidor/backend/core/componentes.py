import pandas as pd
from core.limpieza_datos import normalizar_articulo
from core.limpieza_datos import limpiar_columnas


def procesar_componentes(df):

    df = limpiar_columnas(df)

    col_componente = None
    col_exist = None
    col_participa = None

    for col in df.columns:
        if col == "componente":
            col_componente = col
            
        if "exist fisica kit" in col:
            col_exist = col

        if "cant participa" in col:
            col_participa = col

    if col_componente and col_exist and col_participa:

        df[col_componente] = normalizar_articulo(df[col_componente])

        df[col_exist] = pd.to_numeric(df[col_exist], errors="coerce").fillna(0)
        df[col_participa] = pd.to_numeric(df[col_participa], errors="coerce").fillna(0)

        df["resultado"] = df[col_exist] * df[col_participa]

        df_comp = (
            df.groupby(col_componente)["resultado"]
            .sum()
            .reset_index()
        )
        df_comp.columns = ["Articulo", "COMPONENTE"]
        return df_comp
    return None