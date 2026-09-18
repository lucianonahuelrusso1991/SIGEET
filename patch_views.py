import re

with open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace lista_preinscriptos
old_lista = '''def lista_preinscriptos(request):
    from .models import InscripcionCarrera
    planes_ids = obtener_planes_visibles(request.user)
    
    if planes_ids is not None:
        aspirantes = Alumno.objects.filter(estado_alumno='ASP', inscripciones_carreras__plan_id__in=planes_ids).distinct().order_by('-id')
        aspirantes_internos = InscripcionCarrera.objects.filter(estado='PREINSCRIPTO', plan_id__in=planes_ids).select_related('alumno', 'plan').order_by('-id')
    else:
        aspirantes = Alumno.objects.filter(estado_alumno='ASP').order_by('-id')
        aspirantes_internos = InscripcionCarrera.objects.filter(estado='PREINSCRIPTO').select_related('alumno', 'plan').order_by('-id')
        
    return render(request, 'gestion/lista_preinscriptos.html', {
        'aspirantes': aspirantes,
        'aspirantes_internos': aspirantes_internos
    })'''

new_lista = '''def lista_preinscriptos(request):
    from .models import InscripcionCarrera
    planes_ids = obtener_planes_visibles(request.user)
    
    if planes_ids is not None:
        aspirantes = Alumno.objects.filter(estado_alumno='ASP', inscripciones_carreras__plan_id__in=planes_ids).distinct().order_by('-id')
        aspirantes_esperando_correo = Alumno.objects.filter(estado_alumno='ESP_CORREO', inscripciones_carreras__plan_id__in=planes_ids).distinct().order_by('-id')
        aspirantes_internos = InscripcionCarrera.objects.filter(estado='PREINSCRIPTO', plan_id__in=planes_ids).select_related('alumno', 'plan').order_by('-id')
    else:
        aspirantes = Alumno.objects.filter(estado_alumno='ASP').order_by('-id')
        aspirantes_esperando_correo = Alumno.objects.filter(estado_alumno='ESP_CORREO').order_by('-id')
        aspirantes_internos = InscripcionCarrera.objects.filter(estado='PREINSCRIPTO').select_related('alumno', 'plan').order_by('-id')
        
    return render(request, 'gestion/lista_preinscriptos.html', {
        'aspirantes': aspirantes,
        'aspirantes_esperando_correo': aspirantes_esperando_correo,
        'aspirantes_internos': aspirantes_internos,
        'es_tutor': es_solo_tutor(request.user),
    })'''

content = content.replace(old_lista, new_lista)

with open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("lista_preinscriptos updated successfully")
