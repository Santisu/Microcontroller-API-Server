from django.db import models

# Create your models here.

class Peticion(models.Model):
    """Client petition record

        fecha_y_hora: moment when the request was made
        user: microcontroller client that made the request
    """
    fecha_y_hora = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.fecha_y_hora} - {self.user}'