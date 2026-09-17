from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alumno, Docente, Inscripcion, Comision
from .services.google_classroom import invitar_alumno_a_aula, invitar_equipo_docente

@receiver(post_save, sender=Alumno)
def sync_alumno_classroom(sender, instance, created, **kwargs):
    # Si tiene correo institucional pioix.edu.ar, intentamos invitarlo a las aulas de sus materias inscriptas
    if instance.correo_institucional and instance.correo_institucional.lower().endswith('@pioix.edu.ar'):
        inscripciones = Inscripcion.objects.filter(alumno=instance, estado='REG').select_related('comision__materia')
        for insc in inscripciones:
            if insc.comision.materia.google_classroom_id:
                invitar_alumno_a_aula(insc.comision.materia, instance)

@receiver(post_save, sender=Docente)
def sync_docente_classroom(sender, instance, created, **kwargs):
    if instance.correo_institucional and instance.correo_institucional.lower().endswith('@pioix.edu.ar'):
        # Materias donde dicta clases
        from django.db.models import Q
        comisiones = Comision.objects.filter(Q(docente=instance) | Q(docente_auxiliar=instance)).select_related('materia')
        materias_ya_procesadas = set()
        
        for comision in comisiones:
            materia = comision.materia
            if materia.id not in materias_ya_procesadas and materia.google_classroom_id:
                invitar_equipo_docente(materia, comision.docente)
                materias_ya_procesadas.add(materia.id)
                
        # Materias donde coordina
        for plan in instance.carreras_coordinadas.all():
            for materia in plan.materias.all():
                if materia.google_classroom_id and materia.id not in materias_ya_procesadas:
                    invitar_equipo_docente(materia, None) # Invita solo a coordinadores
                    materias_ya_procesadas.add(materia.id)

@receiver(post_save, sender=Inscripcion)
def sync_inscripcion_classroom(sender, instance, created, **kwargs):
    if created and instance.estado == 'REG':
        alumno = instance.alumno
        materia = instance.comision.materia
        if alumno.correo_institucional and alumno.correo_institucional.lower().endswith('@pioix.edu.ar'):
            if materia.google_classroom_id:
                invitar_alumno_a_aula(materia, alumno)
