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
        
        restauradas_4 = 0
        restauradas_8 = 0
        
        for m in Materia.objects.filter(plan=plan_historico):
            # No usar id, usar si tiene comisiones modernas o si matchea fuerte
            comisiones = m.comisiones.all()
            es_fantasma = (comisiones.count() > 0 and all(c.ciclo_lectivo == 1900 for c in comisiones))
            
            # Si NO es fantasma (es decir, o tiene 0 comisiones, o tiene alguna de 2024), 
            # O matchea las keywords...
            # En realidad, si la movimos por error, la queremos restaurar SI matchea las keywords
            
            matched_4 = any(kw.lower() in m.nombre.lower() for kw in validas_plan_4)
            matched_8 = any(kw.lower() in m.nombre.lower() for kw in validas_plan_8)
            
            # Tambien excluir las en mayusculas completas (las de Ezequiel)
            if m.nombre.isupper():
                continue
                
            # Si matchea y no es mayuscula, probablemente sea legitima del usuario
            if matched_4 and not matched_8:
                m.plan = plan_4
                m.save()
                restauradas_4 += 1
                self.stdout.write(f"Restaurada a Plan 4: {m.nombre}")
            elif matched_8 and not matched_4:
                m.plan = plan_8
                m.save()
                restauradas_8 += 1
                self.stdout.write(f"Restaurada a Plan 8: {m.nombre}")

        # Reactivar planes por si se desactivaron
        if plan_4: plan_4.activo = True; plan_4.save()
        if plan_8: plan_8.activo = True; plan_8.save()

        self.stdout.write(self.style.SUCCESS(f'Restauración inteligente: {restauradas_4} a Plan 4 y {restauradas_8} a Plan 8.'))
