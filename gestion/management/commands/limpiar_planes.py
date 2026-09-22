from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio

class Command(BaseCommand):
    help = 'Limpia los planes de estudio vigentes mandando las materias legacy al Plan Historico'

    def handle(self, *args, **options):
        plan_historico = PlanDeEstudio.objects.filter(nombre__icontains='Histórico').first()
        if not plan_historico:
            self.stdout.write("No se encontró el Plan Histórico.")
            return

        materias_movidas = 0
        for m in Materia.objects.exclude(plan=plan_historico):
            comisiones = m.comisiones.all()
            # Si tiene comisiones, y ABSOLUTAMENTE TODAS son históricas (1900),
            # significa que es una materia vieja inyectada por el importador.
            if comisiones.count() > 0 and all(c.ciclo_lectivo == 1900 for c in comisiones):
                m.plan = plan_historico
                m.save()
                materias_movidas += 1
                self.stdout.write(f"Movida al histórico: {m.nombre}")

        self.stdout.write(self.style.SUCCESS(f'Limpieza completada: {materias_movidas} materias legacy fueron devueltas al Plan Histórico.'))
