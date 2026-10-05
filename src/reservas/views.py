from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Habitacion, Reserva


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
def detalle_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    return render(request, 'reservas/detalle_habitacion.html', {
        'habitacion': habitacion,
    })
def registrar_reserva(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    error = None

    if request.method == 'POST':
        fecha_entrada_texto = request.POST.get('fecha_entrada')
        fecha_salida_texto = request.POST.get('fecha_salida')
        accion = request.POST.get('accion')

        try:
            fecha_entrada = datetime.strptime(
                fecha_entrada_texto,
                '%Y-%m-%d'
            ).date()

            fecha_salida = datetime.strptime(
                fecha_salida_texto,
                '%Y-%m-%d'
            ).date()

            if fecha_salida <= fecha_entrada:
                error = 'La fecha de salida debe ser posterior a la fecha de entrada.'

            else:
                reserva_existente = Reserva.objects.filter(
                    habitacion=habitacion,
                    estado='Confirmada',
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada
                ).exists()

                if reserva_existente:
                    error = 'La habitación no está disponible para las fechas seleccionadas.'

                else:
                    cantidad_noches = (fecha_salida - fecha_entrada).days
                    monto_total = habitacion.precio_diario * cantidad_noches
                    monto_reserva = monto_total * 30 / 100

                    if accion == 'confirmar':
                        reserva = Reserva.objects.create(
                            habitacion=habitacion,
                            fecha_entrada=fecha_entrada,
                            fecha_salida=fecha_salida,
                            cantidad_noches=cantidad_noches,
                            monto_total=monto_total,
                            monto_reserva=monto_reserva,
                            estado='Confirmada'
                        )

                        return render(request, 'reservas/reserva_confirmada.html', {
                            'reserva': reserva,
                            'habitacion': habitacion,
                        })

                    return render(request, 'reservas/registrar_reserva.html', {
                        'habitacion': habitacion,
                        'fecha_entrada': fecha_entrada,
                        'fecha_salida': fecha_salida,
                        'cantidad_noches': cantidad_noches,
                        'monto_total': monto_total,
                        'monto_reserva': monto_reserva,
                    })

        except (ValueError, TypeError):
            error = 'Las fechas ingresadas no son válidas.'

    return render(request, 'reservas/registrar_reserva.html', {
        'habitacion': habitacion,
        'error': error,
    })