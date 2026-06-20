from django import forms
from .models import JustificativoAsistencia
from .models import JustificativoAsistencia, ProgramaComision

class JustificativoAsistenciaForm(forms.ModelForm):
    class Meta:
        model = JustificativoAsistencia
        fields = ['comision', 'fecha_ausencia', 'archivo']
        widgets = {
            'comision': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ausencia': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,application/pdf'}),
        }

class ProgramaComisionForm(forms.ModelForm):
    class Meta:
        model = ProgramaComision
        fields = ['archivo']
        widgets = {
            'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'})
        }
