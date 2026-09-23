from django.shortcuts import render
from .models import Habitacion


def inicio(request):
    habitaciones = Habitacion.objects.all()

    return render(request, 'reservas/inicio.html', {
        'habitaciones': habitaciones
    })