from django.core.management.base import BaseCommand
from gestion.models import Inscripcion, Comision, Materia
from django.db.models import Q

class Command(BaseCommand):
    help = 'Convierte las inscripciones en estado APR a PROM si la materia o comision es promocionable.'

    def handle(self, *args, **kwargs):
        inscripciones_a_corregir = Inscripcion.objects.filter(
            Q(estado='APR') | Q(estado='REG', comision__cerrada=True),
            Q(comision__tipo_aprobacion='PROM') | Q(comision__materia__tipo_aprobacion='PROM')
        )
        
        corregidas = 0
        for insc in inscripciones_a_corregir:
            insc.estado = 'PROM'
            insc.save(update_fields=['estado'])
            corregidas += 1
            
        self.stdout.write(self.style.SUCCESS(f'Exito: Se han corregido {corregidas} materias promocionales que figuraban erronemante como regulares.'))