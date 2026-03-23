
def detectar_columna_articulo(df):

    posibles = ["articulo", "numero", "codigo", "item", "sku", "producto"]

    for col in df.columns:
        for p in posibles:
            if p in col:
                return col

    return None

def detectar_columna_descripcion(df):

    posibles = [
        "descripcion",
        "descripción",
        "nombre articulo",
        "nombre del articulo",
        "articulo descripcion",
        "item description",
        "descripcion articulo"
    ]

    for col in df.columns:
        col_limpia = col.lower().strip()
        for p in posibles:
            if p in col_limpia:
                return col

    return None

def detectar_sistema(df):

    columnas = " ".join(df.columns)

    if "total libros" in columnas or "existencias fisicas" in columnas:
        return "PS"

    if "cantidad almacen" in columnas or "saldo" in columnas or "disponible" in columnas:
        return "JDA"

    return "DESCONOCIDO"

def detectar_tipo_archivo(df):

    columnas = [c.lower().strip() for c in df.columns]

    if "cantidad de recuentos" in columnas:
        return "AJUSTES"

    if "cantidad esperada" in columnas:
        return "RECIBOS"

    if "cant base" in columnas:
        return "RESTRICCIONES"

    if "exist fisica kit" in columnas and "cant participa" in columnas:
        return "COMPONENTES"

    if "id prod" in columnas and "cant dev" in columnas:
        return "RMA"

    if "cant. real" in columnas:
        return "CUADRE"

    if "total libros" in columnas:
        return "PS"

    if "cantidad almacen" in columnas:
        return "JDA"

    return "DESCONOCIDO"

def detectar_columna_cantidad(df):

    prioridad = [
        "total libros",
        "total_libros",
        "cantidad libros",
        "cantidad almacen",
        "cantidad esperada",
        "cant base",
        "cantidad"
    ]

    for p in prioridad:
        for col in df.columns:
            if p in col:
                return col

    return None
