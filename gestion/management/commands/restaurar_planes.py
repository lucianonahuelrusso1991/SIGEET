from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio

class Command(BaseCommand):
    def handle(self, *args, **options):
        plan_historico = PlanDeEstudio.objects.filter(nombre__icontains='Histórico').first()
        plan_4 = PlanDeEstudio.objects.filter(id=4).first()
        plan_8 = PlanDeEstudio.objects.filter(id=8).first()
        
        validas_plan_4 = [
            "Voz I", "comunicación", "Televisión II", 
            "Voz II", "Inglés", "Portugués", "Tecnología II", 
            "Alemana", "Locución III", "Voz III", 
            "Doblaje", "Oratoria", "Periodismo", "Legislación"
        ]
        
        validas_plan_8 = [
            "Expresión Corporal", "EDI 1", "Interpretación y Lectura", "EDI 2",
            "Conducción para Radio", "Conducción para Televisión",
            "Libretos", "Podcast",
            "Pronunciación de Inglés", "Convergente", "Medios Digitales",
            "Técnica Vocal", "Radio y Streaming",
            "Plataformas Digitales", "Alemán y Portugués",
            "Técnicas de Doblaje", "Integrador de Locución", "Integrador de la Voz",
            "Contenidos Sonoros", "Proyecto Integrador",
            "Personajes", "EDI 3"
        ]
        
        # Primero, buscamos en el plan historico aquellas que el usuario creó manualmente (tienen ciclo_lectivo != 1900 o son legitimas)
        # O simplemente usando icontains con la lista de palabras clave
        
        restauradas_4 = 0
        restauradas_8 = 0
        
        for m in Materia.objects.filter(plan=plan_historico):
            # Si la materia fue creada por el usuario (id bajo) o simplemente matchea la palabra clave
            if m.id < 500: # Asumiendo que las importadas tienen ID > 500
                # Buscar a que plan pertenece
                matched_4 = any(kw.lower() in m.nombre.lower() for kw in validas_plan_4)
                matched_8 = any(kw.lower() in m.nombre.lower() for kw in validas_plan_8)
                
                if matched_4 and not matched_8:
                    m.plan = plan_4
                    m.save()
                    restauradas_4 += 1
                elif matched_8 and not matched_4:
                    m.plan = plan_8
                    m.save()
                    restauradas_8 += 1

        self.stdout.write(self.style.SUCCESS(f'Restauración completada: {restauradas_4} a Plan 4 y {restauradas_8} a Plan 8.'))
