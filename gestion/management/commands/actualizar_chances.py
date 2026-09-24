from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime
from gestion.models import Inscripcion

class Command(BaseCommand):
    help = 'Actualiza las chances restantes y el vencimiento de cursadas basandose en 3 turnos por ao.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Turnos en el ao: Marzo (3), Agosto (8), Diciembre (12)
        # Aproximamos el inicio del turno al da 1 del mes para la lgica.
        
        inscripciones = Inscripcion.objects.all().select_related("comision")
        actualizadas = 0
        vencidas = 0
        
        for insc in inscripciones:
            comision = insc.comision
            try:
                anio_ciclo = int(comision.ciclo_lectivo)
            except ValueError:
                continue
                
            cuatrimestre = comision.cuatrimestre
            
            # Determinar cuando termina la cursada
            if cuatrimestre == "1":
                # 1er cuatrimestre termina a fin de julio
                fecha_fin = datetime.date(anio_ciclo, 7, 31)
            else:
                # Anual o 2do cuatrimestre termina a fin de noviembre
                fecha_fin = datetime.date(anio_ciclo, 11, 30)
                
            # Generar lista de turnos desde el ao de la cursada hasta el futuro
            turnos_futuros = []
            for y in range(anio_ciclo, anio_ciclo + 6):
                turnos_futuros.append(datetime.date(y, 3, 1))
                turnos_futuros.append(datetime.date(y, 8, 1))
                turnos_futuros.append(datetime.date(y, 12, 1))
                
            # Filtrar turnos que ocurrieron DESPUES de terminar la cursada
            turnos_validos = [t for t in turnos_futuros if t > fecha_fin]
            
            # El turno 10 es el vencimiento
            if len(turnos_validos) >= 10:
                fecha_vencimiento = turnos_validos[9] # Indice 9 = 10mo turno
            else:
                fecha_vencimiento = turnos_validos[-1] # Fallback (no deberia pasar con +6 aos)
                
            # Contar cuantos turnos ya pasaron hasta HOY
            turnos_pasados = len([t for t in turnos_validos if t <= today])
            
            chances_restantes = 10 - turnos_pasados
            if chances_restantes < 0:
                chances_restantes = 0
                
            insc.chances_restantes = chances_restantes
            insc.vencimiento_cursada = fecha_vencimiento
            
            # Si se le acabaron las chances y estaba REG, deberia pasar a LIB? 
            # (Lo dejamos como REG pero con 0 chances para que bedelia lo vea vencido, 
            # o lo pasamos a VENCIDO/LIBRE segn convenga. Por ahora solo actualizamos chances)
            
            insc.save(update_fields=['chances_restantes', 'vencimiento_cursada'])
            actualizadas += 1
            if chances_restantes == 0:
                vencidas += 1
                
        self.stdout.write(self.style.SUCCESS(f"Se actualizaron {actualizadas} inscripciones. ({vencidas} ya estn vencidas con 0 chances)."))
