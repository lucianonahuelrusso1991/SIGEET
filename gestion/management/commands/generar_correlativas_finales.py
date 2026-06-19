from django.core.management.base import BaseCommand
from gestion.models import Correlatividad

class Command(BaseCommand):
    help = 'Clona las correlativas de cursada (CUR) y las convierte también en correlativas de final (APR)'

    def handle(self, *args, **kwargs):
        correlativas_cursada = Correlatividad.objects.filter(tipo='CUR')
        creadas = 0
        existentes = 0
        
        for corr in correlativas_cursada:
            obj, created = Correlatividad.objects.get_or_create(
                materia=corr.materia,
                requisito=corr.requisito,
                tipo='APR'
            )
            if created:
                creadas += 1
            else:
                existentes += 1
                
        self.stdout.write(self.style.SUCCESS(f'Proceso terminado. Se crearon {creadas} nuevas correlativas de final (APR). {existentes} ya existían.'))
