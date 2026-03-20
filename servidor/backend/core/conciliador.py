import pandas as pd
import numpy as np

from .limpieza_datos import limpiar_columnas
from .deteccion_archivos import detectar_tipo_archivo
from .deteccion_archivos import detectar_sistema
from .limpieza_datos import normalizar_articulo
from .componentes import procesar_componentes
from .deteccion_archivos import detectar_columna_articulo
from .deteccion_archivos import detectar_columna_cantidad
from .deteccion_archivos import detectar_columna_descripcion


def conciliar_archivos_backend(archivos):
        
        from .ia_diferencias import analizar_diferencias_ia
        
        print("Iniciando conciliacion...")

        datos = []
      
        restricciones_df = None
        ajustes_df = None
        recibos_df = None
        componentes_df = None
        rma_df = None
        cuadre_df = None

        for i, archivo in enumerate(archivos):
            print("Procesando:", archivo)
            try:
                df = pd.read_excel(archivo, engine="xlrd")
            except:
                try:
                    df = pd.read_excel(archivo, engine="openpyxl")
                except:
                    try:
                        df = pd.read_csv(archivo)
                    except:
                        raise Exception(f"No se pudo leer el archivo: {archivo}")
                
            df = limpiar_columnas(df) 
            tipo = detectar_tipo_archivo(df) 
            sistema = detectar_sistema(df)
                
            if tipo == "RESTRICCIONES":
                restricciones_df = df
                continue
            if tipo == "AJUSTES":
                ajustes_df = df
                continue
            if tipo == "RECIBOS":
                recibos_df = df
                continue
            if tipo == "RMA":
                rma_df = df
                continue
            if tipo == "CUADRE":
                cuadre_df = df
                continue
            if tipo == "COMPONENTES":
                componentes_df = procesar_componentes(df)
                continue
                        
            col_articulo = detectar_columna_articulo(df)
            col_cantidad = detectar_columna_cantidad(df)
            col_descripcion = detectar_columna_descripcion(df)
            
            print("Columna articulo:", col_articulo)
            print("Columna cantidad:", col_cantidad)

            
            if col_articulo and col_cantidad:
                columnas = [col_articulo, col_cantidad]
                if sistema == "PS" and col_descripcion:
                    columnas.append(col_descripcion)
                df_temp = df[columnas].copy()
                df_temp[col_articulo] = normalizar_articulo(df_temp[col_articulo])
                if sistema == "PS" and col_descripcion:
                    df_temp.columns = ["Articulo", sistema, "Descripcion"]
                else:
                    df_temp.columns = ["Articulo", sistema]
                df_temp[sistema] = pd.to_numeric(df_temp[sistema], errors="coerce").fillna(0)
                if "Descripcion" in df_temp.columns:
                    df_temp = df_temp.groupby("Articulo", as_index=False).agg({
                        sistema: "sum",
                        "Descripcion": "first"})
                else:
                    df_temp = df_temp.groupby("Articulo", as_index=False).sum()
                datos.append(df_temp)
                
        if len(datos) < 2:
            print("No hay suficientes archivos para conciliar")
            return None

        base = datos[0]

        base["Articulo"] = normalizar_articulo(base["Articulo"])
        
        if componentes_df is not None:
            componentes_df["Articulo"] = normalizar_articulo(componentes_df["Articulo"])

        for df in datos[1:]:
            base = base.merge(df, on="Articulo", how="outer")

        base = base.fillna(0)

        if restricciones_df is not None:
            restricciones_df = limpiar_columnas(restricciones_df)
            col_art_r = detectar_columna_articulo(restricciones_df)
            restricciones_df[col_art_r] = normalizar_articulo(
                restricciones_df[col_art_r]
            )
            restricciones_df["cant base"] = pd.to_numeric(
                restricciones_df["cant base"], errors="coerce"
            ).fillna(0)
            restricciones_df = (
                restricciones_df
                .groupby(col_art_r)["cant base"]
                .sum()
                .reset_index()
            )
            restricciones_df.columns = ["Articulo", "RESTRICCIONES"]

        if restricciones_df is not None:
            base = base.merge(
                restricciones_df,
                on="Articulo",
                how="left"
            )
            base["RESTRICCIONES"] = base["RESTRICCIONES"].fillna(0)
        else:
            base["RESTRICCIONES"] = 0

        if "PS" in base.columns:
            base["PS"] = pd.to_numeric(base["PS"], errors="coerce").fillna(0)
        if "JDA" in base.columns:
            base["JDA"] = pd.to_numeric(base["JDA"], errors="coerce").fillna(0)
        if componentes_df is not None:
            base = base.merge(componentes_df, on="Articulo", how="left")
            base["COMPONENTE"] = base["COMPONENTE"].fillna(0)
        else:
            base["COMPONENTE"] = 0
        if "PS" in base.columns and "JDA" in base.columns:
            base["DIFERENCIA"] = (
                base["COMPONENTE"]
                + base["PS"]
                - base["RESTRICCIONES"]
                - base["JDA"]
            )
            base["NOVEDAD"] = ""
            if ajustes_df is not None:
                ajustes_df = limpiar_columnas(ajustes_df)
                ajustes_df["numero de articulo"] = normalizar_articulo(
                    ajustes_df["numero de articulo"]
                )
                ajustes_df["cantidad"] = pd.to_numeric(
                    ajustes_df["cantidad"], errors="coerce"
                ).fillna(0)
                ajustes_df["cantidad de recuentos"] = pd.to_numeric(
                    ajustes_df["cantidad de recuentos"], errors="coerce"
                ).fillna(0)
            if recibos_df is not None:
                recibos_df = limpiar_columnas(recibos_df)
                recibos_df["numero de articulo"] = normalizar_articulo(
                    recibos_df["numero de articulo"]
                )
                recibos_df["cantidad esperada"] = pd.to_numeric(
                    recibos_df["cantidad esperada"], errors="coerce"
                ).fillna(0)
            if rma_df is not None:
                rma_df = limpiar_columnas(rma_df)
                rma_df["id prod"] = normalizar_articulo(rma_df["id prod"])
                rma_df["cant dev"] = pd.to_numeric(
                    rma_df["cant dev"], errors="coerce"
                ).fillna(0)
                rma_df = (
                    rma_df
                    .groupby("id prod")["cant dev"]
                    .sum()
                    .reset_index()
                )
                rma_df.columns = ["Articulo","RMA"]
            if cuadre_df is not None:
                cuadre_df = limpiar_columnas(cuadre_df)
                cuadre_df["articulo"] = normalizar_articulo(cuadre_df["articulo"])
                cuadre_df["cant. real"] = pd.to_numeric(
                    cuadre_df["cant. real"], errors="coerce"
                ).fillna(0)
                cuadre_df = (
                    cuadre_df
                    .groupby("articulo")["cant. real"]
                    .sum()
                    .reset_index()
                )
                cuadre_df.columns = ["Articulo","CUADRE"]

            rma_dict = dict(zip(rma_df["Articulo"], rma_df["RMA"])) if rma_df is not None else {}
            cuadre_dict = dict(zip(cuadre_df["Articulo"], cuadre_df["CUADRE"])) if cuadre_df is not None else {}
            for i in base.index:
                art = base.at[i, "Articulo"]
                dif = base.at[i, "DIFERENCIA"]
                if dif == 0:
                    continue
                # DIFERENCIA viene de PS
                if dif > 0:
                    if art in rma_dict and rma_dict[art] == abs(dif):
                         base.at[i,"NOVEDAD"] = "Diferencia encontrada en RMA"
                         continue
                    if cuadre_df is not None:
                            c = cuadre_df[
                                (cuadre_df["Articulo"] == art)
                                &
                                (cuadre_df["CUADRE"] == abs(dif))
                            ]
                            if not c.empty:
                                base.at[i,"NOVEDAD"] = "Diferencia encontrada en Cuadre Inventario"
                                continue
                # DIFERENCIA viene de JDA
                else:
                    if ajustes_df is not None:
                        a = ajustes_df[
                            (ajustes_df["numero de articulo"] == art)
                            &
                            (
                                (ajustes_df["cantidad"] == dif)
                                |
                                (ajustes_df["cantidad de recuentos"] == dif)
                            )
                        ]
                        if not a.empty:
                            base.at[i,"NOVEDAD"] = "Diferencia encontrada en Ajustes"
                            continue
                        if recibos_df is not None:
                            r = recibos_df[
                                (recibos_df["numero de articulo"] == art)
                                &
                                (recibos_df["cantidad esperada"] == abs(dif))
                            ]
                            if not r.empty:
                                base.at[i,"NOVEDAD"] = "Diferencia encontrada en Recibos"
                                continue
        
        if "DIFERENCIA" in base.columns:
            resultados_ia = analizar_diferencias_ia(base)

            for i in base.index:
                if i in resultados_ia:
                    base.at[i, "NOVEDAD"] = "Novedad encontrada"
        return base
