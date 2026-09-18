import codecs
import re

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_ctx = '''        return render(request, 'gestion/alumnos/dashboard_alumno.html', {
            'alumno': alumno,
            'carreras_info': carreras_info,
            'cursando': cursando,
            'cursadas_aprobadas': cursadas_aprobadas,
            'unread_notifications': unread_notifications,
        })'''

new_ctx = '''        from .models import SolicitudTramite, Materia
        tramites = SolicitudTramite.objects.filter(alumno=alumno).order_by('-fecha_solicitud')
        
        # Get all materias from student's plans to show in the Examen form
        planes_ids = alumno.carreras.values_list('id', flat=True)
        materias_plan = Materia.objects.filter(plan_id__in=planes_ids).order_by('nombre')
        
        return render(request, 'gestion/alumnos/dashboard_alumno.html', {
            'alumno': alumno,
            'carreras_info': carreras_info,
            'cursando': cursando,
            'cursadas_aprobadas': cursadas_aprobadas,
            'unread_notifications': unread_notifications,
            'tramites': tramites,
            'materias_plan': materias_plan,
        })'''

content = content.replace(old_ctx, new_ctx)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dashboard context")
