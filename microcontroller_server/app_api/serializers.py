from rest_framework import serializers
from app_comando.models import Comando

class ComandoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comando
        fields = ('id', 'mes', 'dia', 'hora', 'minuto', 'accion', 'ejecutado')

class ComandoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comando
        fields = ('id', 'ejecutado')