from django.contrib import admin
from .models import (
    Docente, Alumno, PlanDeEstudio, Materia, Correlatividad, 
    Comision, Inscripcion, Nota, PlanillaDiaria, RegistroAsistencia, 
    MesaExamen, InscripcionMesa, TicketReclamo
)

admin.site.register(Docente)
admin.site.register(Alumno)
admin.site.register(PlanDeEstudio)
admin.site.register(Materia)
admin.site.register(Correlatividad)
admin.site.register(Comision)
admin.site.register(Inscripcion)
admin.site.register(Nota)
admin.site.register(PlanillaDiaria)
admin.site.register(RegistroAsistencia)
admin.site.register(MesaExamen)
admin.site.register(InscripcionMesa)
admin.site.register(TicketReclamo)