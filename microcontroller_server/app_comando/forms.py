from django import forms
from .models import Comando
from django.utils import timezone

class ComandoForm(forms.ModelForm):
    class Meta:
        model = Comando
        fields = ['fecha_y_hora', 'accion']
        widgets = {
            'fecha_y_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'accion': forms.Select(),
        }
        
    def clean_fecha_y_hora(self):
        fecha_y_hora = self.cleaned_data.get('fecha_y_hora')

        if fecha_y_hora and fecha_y_hora < timezone.now():
            raise forms.ValidationError("La fecha y hora no puede ser anterior a la actual.")

        return fecha_y_hora