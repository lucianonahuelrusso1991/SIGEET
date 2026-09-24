from django.core.management.base import BaseCommand
from gestion.models import MesaExamen, Comision

class Command(BaseCommand):
    help = 'Asigna automaticamente el presidente a mesas sin docente, basandose en el profesor de la cursada de ese mismo anio.'

    def handle(self, *args, **kwargs):
        mesas_sin_docente = MesaExamen.objects.filter(presidente_mesa__isnull=True)
        actualizadas = 0
        omitidas = 0

        for mesa in mesas_sin_docente:
            # Buscar quien dicto la materia ese mismo ciclo lectivo
            comision = Comision.objects.filter(
                materia=mesa.materia, 
                ciclo_lectivo=mesa.ciclo_lectivo, 
                docente__isnull=False
            ).first()
            
            # Si no encontramos del mismo ciclo, quizas busquemos el titular historico mas reciente
            if not comision:
                comision = Comision.objects.filter(
                    materia=mesa.materia,
                    docente__isnull=False
                ).order_by('-ciclo_lectivo').first()
                
            if comision and comision.docente:
                mesa.presidente_mesa = comision.docente
                mesa.save()
                actualizadas += 1
            else:
                omitidas += 1
                
        self.stdout.write(self.style.SUCCESS(f'Exito: Se asigno profesor titular a {actualizadas} mesas historicas (No se encontraron datos para {omitidas}).'))