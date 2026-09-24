import os
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Elimina comisiones y mesas de examen (y sus inscripciones/notas por CASCADE) para empezar de cero limpio.'

    def add_arguments(self, parser):
        parser.add_argument('--plan', type=int, help='ID del plan a limpiar (ej: 1, 5). Si no se pasa, limpia todos excepto el 8.')
        parser.add_argument('--force', action='store_true', help='Fuerza la eliminación')

    def handle(self, *args, **options):
        from gestion.models import Comision, MesaExamen
        
        plan_id = options.get('plan')
        force = options.get('force')
        
        if not force:
            self.stdout.write(self.style.ERROR("ATENCIÓN: Esto borrará comisiones, mesas, inscripciones y notas."))
            self.stdout.write(self.style.ERROR("Debes agregar --force al comando para confirmar."))
            return
            
        with transaction.atomic():
            if plan_id:
                coms = Comision.objects.filter(materia__plan__id=plan_id)
                mesas = MesaExamen.objects.filter(materia__plan__id=plan_id)
                self.stdout.write(f"Borrando {coms.count()} comisiones y {mesas.count()} mesas del Plan {plan_id}...")
                coms.delete()
                mesas.delete()
            else:
                coms = Comision.objects.exclude(materia__plan__id=8)
                mesas = MesaExamen.objects.exclude(materia__plan__id=8)
                self.stdout.write(f"Borrando {coms.count()} comisiones y {mesas.count()} mesas de TODOS los planes (excepto Plan 8)...")
                coms.delete()
                mesas.delete()
                
        self.stdout.write(self.style.SUCCESS("Limpieza completada con éxito. Base de datos lista para inyectar desde cero."))