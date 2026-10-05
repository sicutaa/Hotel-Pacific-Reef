from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path(
        'habitacion/<int:habitacion_id>/',
        views.detalle_habitacion,
        name='detalle_habitacion'
    ),
]