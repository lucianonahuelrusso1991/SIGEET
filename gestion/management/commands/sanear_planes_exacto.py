from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio

class Command(BaseCommand):
    def handle(self, *args, **options):
        plan_historico = PlanDeEstudio.objects.filter(nombre__icontains='Histórico').first()
        plan_4 = PlanDeEstudio.objects.filter(id=4).first()
        plan_8 = PlanDeEstudio.objects.filter(id=8).first()
        
        # 1. Mandar TODO lo de Plan 4 y Plan 8 al Historico (limpieza total)
        for m in Materia.objects.filter(plan__in=[plan_4, plan_8]):
            m.plan = plan_historico
            m.save()
            
        # 2. Restaurar SOLO los IDs precisos a Plan 4
        ids_plan_4 = list(range(102, 136))
        # Agregar IDs extras si el usuario creó más, pero estos son los 14 originales
        
        restauradas_4 = 0
        for m in Materia.objects.filter(id__in=ids_plan_4):
            m.plan = plan_4
            m.save()
            restauradas_4 += 1
            self.stdout.write(f"Restaurada a Plan 4 exacta: {m.nombre} (ID: {m.id})")
            
        # 3. Restaurar SOLO los IDs precisos a Plan 8
        ids_plan_8 = list(range(242, 275))
        restauradas_8 = 0
        for m in Materia.objects.filter(id__in=ids_plan_8):
            m.plan = plan_8
            m.save()
            restauradas_8 += 1
            self.stdout.write(f"Restaurada a Plan 8 exacta: {m.nombre} (ID: {m.id})")
            
        # 4. Qué pasa si el usuario creó materias NUEVAS en produccion despues del volcado? (ID > 791)
        # Vamos a usar nombres exactos para rescatar cualquier otra materia legitima
        validas_plan_4 = [
            "Taller integral de la Voz I", "Teorías de la comunicación", "Televisión II", 
            "Taller integral de la Voz II", "Inglés", "Portugués", "Tecnología II", 
            "Fonética Alemana", "Locución III", "Taller integral de la Voz III", 
            "Doblaje", "Oratoria", "Periodismo", "Legislación de Medios Audiovisuales"
        ]
        
        validas_plan_8 = [
            "Expresión Corporal", "EDI 1", "Locución, Interpretación y Lectura", "EDI 2",
            "Práctica Profesionalizante en Conducción para Radio", "Práctica Profesionalizante en Conducción para Televisión",
            "Libretos y Guiones", "Práctica Profesionalizante en Podcast y Producción de Contenidos Digitales",
            "Pronunciación de Inglés", "Comunicación Convergente", "Locución para Medios Digitales",
            "Técnica Vocal Avanzada", "Práctica Profesionalizante en Radio y Streaming",
            "Plataformas Digitales y Nuevas Tendencias Audiovisuales", "Pronunciación de Alemán y Portugués",
            "Técnicas de Doblaje", "Taller Integrador de Locución", "Taller Integrador de la Voz",
            "Taller Integrador de Contenidos Sonoros", "Proyecto Integrador en Locución para Plataformas Audiovisuales",
            "Doblaje y Locución de Personajes", "EDI 3"
        ]
        
        def normalizar(n):
            import unicodedata
            s = n.lower().strip()
            return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
            
        norm_plan_4 = [normalizar(n) for n in validas_plan_4]
        norm_plan_8 = [normalizar(n) for n in validas_plan_8]

        for m in Materia.objects.filter(plan=plan_historico, id__gt=791):
            n = normalizar(m.nombre)
            if n in norm_plan_4:
                m.plan = plan_4
                m.save()
                self.stdout.write(f"Rescatada a Plan 4 nueva: {m.nombre}")
            elif n in norm_plan_8:
                m.plan = plan_8
                m.save()
                self.stdout.write(f"Rescatada a Plan 8 nueva: {m.nombre}")

        self.stdout.write(self.style.SUCCESS('Saneamiento de IDs exacto completado.'))
