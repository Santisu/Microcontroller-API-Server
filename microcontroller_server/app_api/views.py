from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ComandoReadSerializer, ComandoWriteSerializer
from django.contrib.auth import get_user_model
from app_comando.models import Comando
from .models import Peticion

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
import time

User = get_user_model()

class CommandViewSet(viewsets.ModelViewSet): 
    queryset = Comando.objects.filter(ejecutado=False).order_by("fecha_y_hora")

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ComandoWriteSerializer
        if self.action == 'list':
            record = Peticion(
                user=self.request.user
            )
            record.save()

        return ComandoReadSerializer
    
@require_GET
def ntp_time(request):
    """Sends current time to the microcontroller client to set the time.

    Returns:
        Json: Json with current time
    """
    current_time = timezone.now().timestamp()
    time_tuple = time.localtime(current_time)
    time_json = {
        "year" : time_tuple[0],
        "month" : time_tuple[1],
        "day" : time_tuple[2],
        "hour" : time_tuple[3],
        "min" : time_tuple[4],
        "sec" : time_tuple[5],
        "wday" : time_tuple[6],
        "yday" : time_tuple[7],
        "is_dst" : time_tuple[8]
    }
    return JsonResponse(time_json)