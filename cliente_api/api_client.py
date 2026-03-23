from core.conciliador import conciliar_archivos_backend
import requests

URL_GUARDAR = "http://TU_IP/api/guardar/"


def conciliar_local(rutas):
    try:
        resultado = conciliar_archivos_backend(rutas)
        return resultado
    except Exception as e:
        print("Error:", str(e))
        return None


def enviar_resultado(resultado_df):
    try:
        data = resultado_df.to_dict(orient="records")

        response = requests.post(URL_GUARDAR, json=data)

        if response.status_code == 200:
            print("Guardado OK")
        else:
            print("Error servidor:", response.text)

    except Exception as e:
        print("Error conexión:", str(e))