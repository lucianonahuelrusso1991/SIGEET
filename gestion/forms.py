from django import forms
from .models import JustificativoAsistencia

class JustificativoAsistenciaForm(forms.ModelForm):
    class Meta:
        model = JustificativoAsistencia
        fields = ['comision', 'fecha_ausencia', 'archivo']
        widgets = {
            'comision': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ausencia': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,.pdf'}),
        }
