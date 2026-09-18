import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_views = '''
# -----------------------------
# Trámites de Alumnos
# -----------------------------
@login_required
def solicitar_tramite_alumno(request):
    if not hasattr(request.user, 'perfil_alumno'):
        return redirect('dashboard')
        
    alumno = request.user.perfil_alumno
    
    if request.method == 'POST':
        from .models import SolicitudTramite, Materia
        tipo = request.POST.get('tipo_tramite')
        
        # Prevent spam (only 1 pending request per type)
        if SolicitudTramite.objects.filter(alumno=alumno, tipo=tipo, estado='PENDIENTE').exists():
            messages.warning(request, f'Ya tienes una solicitud de {tipo} pendiente de aprobación.')
            return redirect('dashboard')
            
        if tipo == 'REGULAR':
            SolicitudTramite.objects.create(alumno=alumno, tipo='REGULAR')
            messages.success(request, 'Constancia de Alumno Regular solicitada con éxito. Aguardá a que Bedelía la habilite.')
            
        elif tipo == 'EXAMEN':
            materia_id = request.POST.get('materia_id')
            fecha_examen = request.POST.get('fecha_examen')
            if not materia_id or not fecha_examen:
                messages.error(request, 'Para el certificado de examen debes seleccionar la materia y la fecha.')
                return redirect('dashboard')
                
            materia = get_object_or_404(Materia, id=materia_id)
            SolicitudTramite.objects.create(alumno=alumno, tipo='EXAMEN', materia=materia, fecha_examen=fecha_examen)
            messages.success(request, 'Certificado de Examen solicitado con éxito. Aguardá a que Bedelía lo habilite.')
            
    return redirect('dashboard')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def lista_tramites(request):
    from .models import SolicitudTramite
    
    pendientes = SolicitudTramite.objects.filter(estado='PENDIENTE').order_by('fecha_solicitud')
    historial = SolicitudTramite.objects.exclude(estado='PENDIENTE').order_by('-fecha_solicitud')[:100]
    
    return render(request, 'gestion/lista_tramites.html', {
        'pendientes': pendientes,
        'historial': historial
    })

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def autorizar_tramite(request, tramite_id):
    from .models import SolicitudTramite
    from django.utils import timezone
    
    tramite = get_object_or_404(SolicitudTramite, id=tramite_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aprobar':
            tramite.estado = 'APROBADO'
            tramite.fecha_aprobacion = timezone.now()
            tramite.save()
            messages.success(request, f'Trámite de {tramite.alumno} APROBADO.')
        elif accion == 'rechazar':
            tramite.estado = 'RECHAZADO'
            tramite.save()
            messages.success(request, f'Trámite de {tramite.alumno} RECHAZADO.')
            
    return redirect('lista_tramites')
'''

content += new_views

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added tramites views to views.py")
