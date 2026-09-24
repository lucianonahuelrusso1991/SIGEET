import os
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Elimina TODAS las comisiones y mesas de examen (y sus inscripciones/notas por CASCADE) para empezar de cero limpio.'

    def add_arguments(self, parser):
        parser.add_argument('--todo', action='store_true', help='Limpia absolutamente todo el historial')

    def handle(self, *args, **options):
        from gestion.models import Comision, MesaExamen
        
        if not options.get('todo'):
            self.stdout.write(self.style.ERROR("ATENCIÓN: Esto borrará TODAS las comisiones, mesas, inscripciones y notas del sistema."))
            self.stdout.write(self.style.ERROR("Debes agregar --todo al comando para confirmar la destrucción total."))
            return
            
        with transaction.atomic():
            c_count = Comision.objects.count()
            m_count = MesaExamen.objects.count()
            self.stdout.write(f"Borrando {c_count} comisiones y {m_count} mesas de TODOS los planes sin excepción...")
            
            Comision.objects.all().delete()
            MesaExamen.objects.all().delete()
                
        self.stdout.write(self.style.SUCCESS("Limpieza nuclear completada. Base de datos 100% en blanco y lista para inyectar."))