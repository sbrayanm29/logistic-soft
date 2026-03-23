from django.urls import path
from .views import conciliar

urlpatterns = [
    path("api/guardar/", views.guardar_resultado),
]