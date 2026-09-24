from django.core.management.base import BaseCommand
from gestion.models import Materia

class Command(BaseCommand):
    help = 'Marca automaticamente como promocionables las materias que no llevan final'

    def handle(self, *args, **kwargs):
        keywords = [
            'tecnologia', 'fonetica', 'practica profesionalizante', 'redaccion', 
            'expresion corporal', 'ingles', 'portugues', 'libretos', 'television', 
            'voz', 'doblaje', 'actuacion', 'taller'
        ]
        
        materias = Materia.objects.all()
        actualizadas = 0
        
        for mat in materias:
            nombre = mat.nombre.lower()
            # Special check for exact matches or contains
            if any(k in nombre for k in keywords):
                if mat.tipo_aprobacion != 'PROM':
                    mat.tipo_aprobacion = 'PROM'
                    mat.save(update_fields=['tipo_aprobacion'])
                    actualizadas += 1
                    
        self.stdout.write(self.style.SUCCESS(f'Exito: Se marcaron {actualizadas} materias como Promocionables.'))