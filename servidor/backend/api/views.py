from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.conciliador import conciliar_archivos_backend
import pandas as pd
import tempfile
import os

from core.conciliador import conciliar_archivos_backend  # IMPORTANTE

@api_view(['POST'])
def conciliar(request):
    return Response({
        "mensaje": "Procesamiento ahora es local"
    })