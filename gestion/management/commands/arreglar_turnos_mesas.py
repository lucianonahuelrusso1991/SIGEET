from django.core.management.base import BaseCommand
from gestion.models import MesaExamen

class Command(BaseCommand):
    help = 'Recalcula el turno y ciclo lectivo de las mesas de examen historicas segun su fecha.'

    def handle(self, *args, **kwargs):
        mesas = MesaExamen.objects.all()
        actualizadas = 0

        for mesa in mesas:
            if not mesa.fecha_hora:
                continue
                
            mes = mesa.fecha_hora.month
            anio = mesa.fecha_hora.year
            
            # Logica de turnos argentinos
            if mes in [1, 2, 3, 4]:
                mesa.turno = 'FEB_MAR'
                mesa.ciclo_lectivo = anio - 1
            elif mes in [5, 6, 7, 8, 9]:
                mesa.turno = 'JUL_AGO'
                mesa.ciclo_lectivo = anio
            else:  # 10, 11, 12
                mesa.turno = 'NOV_DIC'
                mesa.ciclo_lectivo = anio
                
            mesa.save()
            actualizadas += 1
            
        self.stdout.write(self.style.SUCCESS(f'Exito: Se actualizaron los turnos y ciclos lectivos de {actualizadas} mesas historicas.'))