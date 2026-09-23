from django.shortcuts import render
from .models import Habitacion


def inicio(request):
    habitaciones = Habitacion.objects.filter(estado='Disponible')

    fecha_entrada = request.GET.get('fecha_entrada')
    fecha_salida = request.GET.get('fecha_salida')

    if fecha_entrada and fecha_salida:
        habitaciones_ocupadas = Habitacion.objects.filter(
            reservas__estado='Confirmada',
            reservas__fecha_entrada__lt=fecha_salida,
            reservas__fecha_salida__gt=fecha_entrada
        )

        habitaciones = habitaciones.exclude(
            id__in=habitaciones_ocupadas
        )

    return render(request, 'reservas/inicio.html', {
        'habitaciones': habitaciones,
        'fecha_entrada': fecha_entrada,
        'fecha_salida': fecha_salida,
    })