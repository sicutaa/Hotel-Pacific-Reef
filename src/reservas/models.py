from django.db import models


class Habitacion(models.Model):
    TIPO_HABITACION = [
        ('Turista', 'Turista'),
        ('Premium', 'Premium'),
    ]

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_HABITACION)
    precio_diario = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Disponible')


    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"

class Reserva(models.Model):
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    cantidad_noches = models.IntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_reserva = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Confirmada')

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva {self.id} - Habitación {self.habitacion.numero}"