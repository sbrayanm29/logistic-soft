import itertools
from itertools import combinations
import numpy as np

def analizar_diferencias_ia(df):

    resultados = {}

    columnas = [
        "COMPONENTE",
        "RESTRICCIONES",
        "RMA",
        "CUADRE",
        "RECIBOS",
        "AJUSTES"
    ]

    for idx, fila in df.iterrows():

        ps = float(fila.get("PS",0) or 0)
        jda = float(fila.get("JDA",0) or 0)

        diferencia = ps - jda

        # ❌ no analizar si no hay diferencia
        if diferencia == 0:
            continue

        valores = np.array([
            float(fila.get("COMPONENTE",0) or 0),
            float(fila.get("RESTRICCIONES",0) or 0),
            float(fila.get("RMA",0) or 0),
            float(fila.get("CUADRE",0) or 0),
            float(fila.get("RECIBOS",0) or 0),
            float(fila.get("AJUSTES",0) or 0)
        ])

        objetivo = abs(diferencia)

        mejor_error = objetivo
        mejor_combo = None

        for r in range(1, len(valores)+1):

            for combo in itertools.combinations(range(len(valores)), r):

                suma = valores[list(combo)].sum()

                error = abs(objetivo - suma)

                if error < mejor_error:

                    mejor_error = error
                    mejor_combo = combo

                if error == 0:
                    break

        if mejor_combo is None:
            continue

        explicacion = []
        detalle = []

        total = 0

        for i in mejor_combo:

            nombre = columnas[i]
            valor = valores[i]

            if valor == 0:
                continue

            explicacion.append(nombre)
            detalle.append(f"{nombre}: {valor}")

            total += valor

        detalle.append("")
        detalle.append(f"PS: {ps}")
        detalle.append(f"JDA: {jda}")
        detalle.append(f"Diferencia detectada: {diferencia}")
        detalle.append(f"Explicación encontrada: {total}")

        if diferencia < 0:
            detalle.append("")
            detalle.append("JDA tiene más inventario que PS")

        if diferencia > 0:
            detalle.append("")
            detalle.append("PS tiene más inventario que JDA")

        resultados[idx] = {
            "explicacion": " + ".join(explicacion),
            "detalle": "\n".join(detalle)
        }

    return resultados