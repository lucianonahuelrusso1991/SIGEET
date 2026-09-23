import os
import django
from django.core.management.base import BaseCommand
from gestion.models import Alumno

class Command(BaseCommand):
    help = 'Limpia y corrige los nombres y apellidos importados mal en la Fase 3'

    def handle(self, *args, **options):
        alumnos = Alumno.objects.all()
        fixed = 0
        for al in alumnos:
            # Si el apellido parece un slug (letras minusculas y guiones, sin espacios)
            # O si el nombre es la cadena entera y el apellido es un slug
            if '-' in al.apellido and al.apellido.islower():
                full_name = al.nombre.strip()
                ape = ""
                nom = ""
                
                if ',' in full_name:
                    parts = full_name.split(',', 1)
                    ape = parts[0].strip().title()
                    nom = parts[1].strip().title()
                else:
                    # Heuristica para casos sin coma
                    words = full_name.split()
                    if len(words) == 1:
                        ape = words[0].title()
                        nom = "-"
                    elif len(words) == 2:
                        ape = words[0].title()
                        nom = words[1].title()
                    elif len(words) == 3:
                        ape = words[0].title()
                        nom = " ".join(words[1:]).title()
                    elif len(words) >= 4:
                        ape = " ".join(words[:2]).title()
                        nom = " ".join(words[2:]).title()
                    else:
                        ape = full_name.title()
                        nom = "-"
                        
                al.apellido = ape[:99]
                al.nombre = nom[:99] if nom else "-"
                al.save()
                
                # Actualizar User
                if al.usuario:
                    al.usuario.last_name = al.apellido[:149]
                    al.usuario.first_name = al.nombre[:149]
                    al.usuario.save()
                    
                fixed += 1
                self.stdout.write(f"Corregido: {ape}, {nom}")

        self.stdout.write(self.style.SUCCESS(f"Se han corregido los nombres de {fixed} alumnos."))