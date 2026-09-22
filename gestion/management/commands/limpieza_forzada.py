from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio

class Command(BaseCommand):
    def handle(self, *args, **options):
        plan_historico = PlanDeEstudio.objects.filter(nombre__icontains='Histórico').first()
        plan_4 = PlanDeEstudio.objects.filter(id=4).first()
        plan_8 = PlanDeEstudio.objects.filter(id=8).first()
        
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

        movidas = 0
        if plan_4:
            for m in Materia.objects.filter(plan=plan_4):
                if normalizar(m.nombre) not in norm_plan_4:
                    m.plan = plan_historico
                    m.save()
                    movidas += 1
                    self.stdout.write(f"Movida al historico (desde P4): {m.nombre}")
                    
        if plan_8:
            for m in Materia.objects.filter(plan=plan_8):
                if normalizar(m.nombre) not in norm_plan_8:
                    m.plan = plan_historico
                    m.save()
                    movidas += 1
                    self.stdout.write(f"Movida al historico (desde P8): {m.nombre}")

        # Tambien, forzar que el plan historico no sea activo por las dudas
        if plan_historico and plan_historico.activo:
            plan_historico.activo = False
            plan_historico.save()
            self.stdout.write("Plan Histórico seteado a inactivo.")

        self.stdout.write(self.style.SUCCESS(f'Limpieza forzada completada: {movidas} materias expulsadas al Plan Histórico.'))
