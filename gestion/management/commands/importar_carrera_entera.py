import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Ejecuta la importación segmentada para TODOS los años de una carrera (2015 a 2026)'

    def add_arguments(self, parser):
        parser.add_argument('--carrera_legacy', type=int, required=True)
        parser.add_argument('--plan_nuevo', type=int, required=True)

    def handle(self, *args, **options):
        carrera_legacy = options['carrera_legacy']
        plan_nuevo = options['plan_nuevo']

        self.stdout.write(self.style.WARNING(f"Iniciando importación COMPLETA para Legacy {carrera_legacy} -> Nuevo {plan_nuevo}"))
        
        # Iteramos desde 2015 hasta 2026
        for anio in range(2015, 2027):
            self.stdout.write(f"\n--- Procesando Año {anio} ---")
            try:
                call_command('importar_segmentado', carrera_legacy=carrera_legacy, plan_nuevo=plan_nuevo, anio=anio)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error en el año {anio}: {e}"))
                
        self.stdout.write(self.style.SUCCESS(f"\n>>> IMPORTACIÓN DE TODA LA CARRERA COMPLETADA <<<"))