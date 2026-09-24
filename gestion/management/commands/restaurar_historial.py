import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Restaura TODAS las inscripciones (cursadas y finales) de todas las carreras activas luego de un borrado de comisiones.'

    def handle(self, *args, **options):
        # Mapeo de Carrera_Legacy_ID -> Nuevo_Plan_ID
        carreras = [
            (13, 1), # Analisis
            (9, 2),  # Ciencias Sagradas
            (5, 3),  # Locucion
            (11, 4), # Psico
            (12, 5)  # Turismo
        ]
        
        anios = list(range(2021, 2027)) # 2021 a 2026

        self.stdout.write(self.style.WARNING("INICIANDO RESTAURACION MASIVA DE HISTORIAL (CURSADAS Y FINALES)"))
        
        for legacy, nuevo in carreras:
            self.stdout.write(self.style.SUCCESS(f"\n--- Restaurando Carrera Legacy {legacy} -> Plan Nuevo {nuevo} ---"))
            for anio in anios:
                self.stdout.write(f"Procesando ao {anio}...")
                try:
                    call_command('importar_segmentado', carrera_legacy=legacy, plan_nuevo=nuevo, anio=anio)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error procesando ao {anio}: {e}"))
                    
        self.stdout.write(self.style.SUCCESS("\nRESTAURACION MASIVA COMPLETADA. LOS ALUMNOS DEBERIAN TENER SUS CURSADAS Y FINALES."))