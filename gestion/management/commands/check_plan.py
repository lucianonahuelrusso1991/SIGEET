from django.core.management.base import BaseCommand
from gestion.models import PlanDeEstudio

class Command(BaseCommand):
    def handle(self, *args, **options):
        p = PlanDeEstudio.objects.filter(nombre__icontains='Histórico').first()
        self.stdout.write(f"Plan Historico activo: {p.activo}")
