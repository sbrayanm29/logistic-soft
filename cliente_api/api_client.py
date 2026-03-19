import requests

URL = "http://127.0.0.1:8000/api/conciliar/"

def enviar_archivos(rutas):
    files = []

    for ruta in rutas:
        files.append(("archivos", open(ruta, "rb")))

    try:
        response = requests.post(URL, files=files)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error servidor:", response.text)
            return None

    except Exception as e:
        print("Error conexión:", str(e))
        return None