import codecs
import re

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_constancia = '''def constancia_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    return render(request, 'gestion/constancia_impresion.html', {'alumno': alumno})'''

new_constancia = '''@login_required
def constancia_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    # Check permission
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin and getattr(request.user, 'perfil_alumno', None) != alumno:
        messages.error(request, 'No tienes permiso para ver esta constancia.')
        return redirect('dashboard')
        
    if not es_admin:
        from .models import SolicitudTramite
        tramites = SolicitudTramite.objects.filter(alumno=alumno, tipo='REGULAR', estado='APROBADO')
        vigente = any(t.esta_vigente for t in tramites)
        if not vigente:
            messages.error(request, 'No tienes un trámite de Constancia de Alumno Regular aprobado y vigente (7 días hábiles). Por favor, solicítalo en Autogestión.')
            return redirect('dashboard')
            
    return render(request, 'gestion/constancia_impresion.html', {'alumno': alumno})'''

content = content.replace(old_constancia, new_constancia)

old_cert_ex = '''def certificado_examen_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    from .models import InscripcionMesa, Materia
    from datetime import date'''

new_cert_ex = '''def certificado_examen_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin and getattr(request.user, 'perfil_alumno', None) != alumno:
        messages.error(request, 'No tienes permiso para ver este certificado.')
        return redirect('dashboard')
        
    if not es_admin:
        from .models import SolicitudTramite
        tramites = SolicitudTramite.objects.filter(alumno=alumno, tipo='EXAMEN', estado='APROBADO')
        vigente = any(t.esta_vigente for t in tramites)
        if not vigente:
            messages.error(request, 'No tienes un trámite de Certificado de Examen aprobado y vigente (7 días hábiles). Por favor, solicítalo en Autogestión.')
            return redirect('dashboard')

    from .models import InscripcionMesa, Materia
    from datetime import date'''

content = content.replace(old_cert_ex, new_cert_ex)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
