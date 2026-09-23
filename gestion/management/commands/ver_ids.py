from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio

class Command(BaseCommand):
    def handle(self, *args, **options):
        # find the max ID of subjects before importing fase1
        pass
