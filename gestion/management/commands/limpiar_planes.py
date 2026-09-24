from django.core.management.base import BaseCommand
from gestion.models import PlanDeEstudio

class Command(BaseCommand):
    help = 'Elimina todos los planes de estudio que no sean las 5 carreras principales'

    def handle(self, *args, **options):
        carreras_validas = [
            "sistemas",
            "sagradas",
            "producci",
            "locuci"
        ]

        planes = PlanDeEstudio.objects.all()
        borrados = 0
        for p in planes:
            keep = False
            nombre_norm = p.nombre.lower().replace('ó','o').replace('á','a').replace('í','i')
            for cv in carreras_validas:
                if cv in nombre_norm:
                    keep = True
                    break
            
            # Hay dos de locución, así que "locuci" salva a ambas.
            
            if not keep:
                self.stdout.write(self.style.ERROR(f"Borrando: {p.nombre}"))
                p.delete()
                borrados += 1
            else:
                self.stdout.write(self.style.SUCCESS(f"MANTENIENDO: {p.nombre}"))
                
        self.stdout.write(self.style.WARNING(f"\nTotal borrados: {borrados}"))