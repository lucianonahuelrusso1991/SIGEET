from django.core.management.base import BaseCommand
from gestion.models import Alumno

class Command(BaseCommand):
    def handle(self, *args, **options):
        micieli = Alumno.objects.filter(dni='30149595').first()
        if micieli:
            for c in micieli.carreras.all():
                self.stdout.write(f"Micieli esta en: {c.nombre} (Activo: {c.activo})")
        else:
            self.stdout.write("Micieli no encontrada.")
