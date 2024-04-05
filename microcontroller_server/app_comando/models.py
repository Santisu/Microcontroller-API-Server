from django.db import models

# Create your models here.

class Comando(models.Model):
    ACTIONS = [
        ('action_1', 'Action 1'),
        ('action_2', 'Action 2'),
    ]

    fecha_y_hora = models.DateTimeField()
    accion = models.CharField(max_length=20, choices=ACTIONS)
    ejecutado = models.BooleanField(default=False)
    mes = models.IntegerField()
    dia = models.IntegerField()
    hora = models.IntegerField()
    minuto = models.IntegerField()

    def __str__(self):
        return f'{self.fecha_y_hora} - {self.accion}'

    def save(self, *args, **kwargs):
        # Parse date and time
        self.mes = self.fecha_y_hora.month
        self.dia = self.fecha_y_hora.day
        self.hora = self.fecha_y_hora.hour
        self.minuto = self.fecha_y_hora.minute

        super().save(*args, **kwargs)


