from django.core.management.base import BaseCommand
from gestion.models import Comision

class Command(BaseCommand):
    help = 'Cierra comisiones antiguas (2025 o menores)'

    def handle(self, *args, **options):
        # Todos los años hasta 2025
        ciclos_viejos = [str(year) for year in range(2000, 2026)]
        
        comisiones = Comision.objects.filter(ciclo_lectivo__in=ciclos_viejos, cerrada=False)
        count = comisiones.count()
        comisiones.update(cerrada=True)
        
        self.stdout.write(self.style.SUCCESS(f"Se cerraron correctamente {count} comisiones de 2025 y aos anteriores."))