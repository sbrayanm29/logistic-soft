from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.conciliador import conciliar_archivos_backend
import pandas as pd
import tempfile
import os

from core.conciliador import conciliar_archivos_backend  # IMPORTANTE

@api_view(['POST'])
def conciliar(request):
    archivos = request.FILES.getlist('archivos')
    
    rutas = []

    for archivo in archivos:
        temp = tempfile.NamedTemporaryFile(delete=False)
        for chunk in archivo.chunks():
            temp.write(chunk)
        temp.close()
        rutas.append(temp.name)

    # Ejecutar tu lógica
    resultado = conciliar_archivos_backend(rutas)

    # Convertir a JSON
    data = resultado.to_dict(orient="records")

    # Limpiar archivos temporales
    for ruta in rutas:
        os.remove(ruta)

    return Response(data)