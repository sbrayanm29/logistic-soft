from django.urls import path
from .views import conciliar

urlpatterns = [
    path('conciliar/', conciliar),
]