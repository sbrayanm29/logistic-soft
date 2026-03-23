from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.conciliador import conciliar_archivos_backend
import pandas as pd
import tempfile
import os

from django.http import JsonResponse
import json

def guardar_resultado(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # aquí guardas en DB
        print("Recibido:", len(data))

        return JsonResponse({"status": "ok"})