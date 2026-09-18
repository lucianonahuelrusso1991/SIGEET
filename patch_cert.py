import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_cert = '''def certificado_examen_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    # Buscamos la prxima mesa inscripta o la ltima
    from .models import InscripcionMesa
    from datetime import date
    ultima_mesa = InscripcionMesa.objects.filter(alumno=alumno).order_by('-mesa__fecha_hora').first()
    return render(request, 'gestion/alumnos/certificado_examen.html', {'alumno': alumno, 'fecha_actual': date.today(), 'ultima_mesa': ultima_mesa})'''

new_cert = '''def certificado_examen_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    from .models import InscripcionMesa, Materia
    from datetime import date
    
    materia_id = request.GET.get('materia_id')
    fecha_examen = request.GET.get('fecha')
    
    materia = None
    if materia_id:
        materia = Materia.objects.filter(id=materia_id).first()
        
    ultima_mesa = InscripcionMesa.objects.filter(alumno=alumno).order_by('-mesa__fecha_hora').first()
    
    return render(request, 'gestion/alumnos/certificado_examen.html', {
        'alumno': alumno, 
        'fecha_actual': date.today(), 
        'ultima_mesa': ultima_mesa,
        'materia_cert': materia,
        'fecha_cert': fecha_examen
    })'''

import re
pattern = r'def certificado_examen_alumno.*?return render\(.*?\)'
content = re.sub(pattern, new_cert, content, flags=re.DOTALL)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated certificado_examen_alumno view")
