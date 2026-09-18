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

from .models import Alumno

class PreinscripcionForm(forms.ModelForm):
    class Meta:
        model = Alumno
        exclude = ['usuario', 'estado_alumno', 'doc_dni', 'doc_vacunas', 'doc_partida', 'doc_primaria', 'doc_pase', 'correo_institucional']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna_zona': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-select'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'plan': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        return normalize_alumno_data(cleaned_data)

class RevisarPreinscriptoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        exclude = ['usuario', 'estado_alumno', 'doc_vacunas', 'doc_partida', 'doc_pase'] # Quitados del form de bedelía
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
            'correo_institucional': forms.EmailInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna_zona': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-select'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'plan': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'doc_dni': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_primaria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        return normalize_alumno_data(cleaned_data)

import re

def normalize_alumno_data(cleaned_data):
    # Only numbers for DNI
    if 'dni' in cleaned_data and cleaned_data['dni']:
        cleaned_data['dni'] = re.sub(r'\D', '', str(cleaned_data['dni']))
    
    # Title case for text fields
    text_fields = ['nombre', 'apellido', 'direccion', 'localidad', 'nacionalidad', 'comuna_zona', 'lugar_nacimiento']
    for field in text_fields:
        if field in cleaned_data and cleaned_data[field]:
            cleaned_data[field] = cleaned_data[field].title()
    
    return cleaned_data
