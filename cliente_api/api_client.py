from core.conciliador import conciliar_archivos_backend

def enviar_archivos(rutas):
    try:
        resultado = conciliar_archivos_backend(rutas)
        return resultado.to_dict(orient="records") if resultado is not None else None
    except Exception as e:
        print("Error:", str(e))
        return None