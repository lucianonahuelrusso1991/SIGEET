from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from datetime import date
from .models import Alumno, Docente, PlanDeEstudio, Materia, Comision, Inscripcion, Nota, PlanillaDiaria, RegistroAsistencia, Correlatividad, HorarioComision

@login_required
def dashboard(request):
    from .models import MesaExamen, Notificacion
    cant_alumnos = Alumno.objects.filter(estado_alumno='ACT').count()
    cant_docentes = Docente.objects.count()
    cant_comisiones = Comision.objects.filter(cerrada=False).count()
    cant_mesas = MesaExamen.objects.filter(cerrada=False).count()
    
    # Obtener notificaciones no leídas para el hero banner
    if request.user.is_authenticated:
        unread_notifications = Notificacion.objects.filter(usuario=request.user, leida=False).select_related('comunicado').order_by('-comunicado__fecha_creacion')
    else:
        unread_notifications = []

    # Bifurcación para panel de alumno
    if hasattr(request.user, 'perfil_alumno'):
        alumno = request.user.perfil_alumno
        
        # Calcular porcentaje de avance
        total_materias = alumno.plan.materias.count() if alumno.plan else 0
        total_acreditadas = alumno.equivalencias.count() + alumno.inscripciones.filter(estado='PROM').count() + alumno.mesas_inscriptas.filter(estado='APR').count()
        porcentaje_avance = (total_acreditadas / total_materias * 100) if total_materias > 0 else 0
        
        # Materias cursando
        cursando = alumno.inscripciones.filter(estado='REG', comision__cerrada=False)
        
        return render(request, 'gestion/alumnos/dashboard_alumno.html', {
            'alumno': alumno,
            'unread_notifications': unread_notifications,
            'porcentaje_avance': round(porcentaje_avance, 1),
            'cursando': cursando,
        })

    # Bifurcación para panel de docente
    if hasattr(request.user, 'perfil_docente'):
        docente = request.user.perfil_docente
        from django.db.models import Q
        
        # Comisiones asignadas activas
        comisiones_activas = Comision.objects.filter(Q(docente=docente) | Q(docente_auxiliar=docente), cerrada=False).select_related('materia')
        
        # Mesas de examen asignadas (como presidente o vocal) que no estén cerradas
        mesas_asignadas = MesaExamen.objects.filter(
            Q(presidente_mesa=docente) | Q(vocal_1=docente) | Q(vocal_2=docente),
            cerrada=False
        ).select_related('materia').order_by('fecha_hora')
        
        return render(request, 'gestion/docentes/dashboard_docente.html', {
            'docente': docente,
            'unread_notifications': unread_notifications,
            'comisiones': comisiones_activas,
            'mesas': mesas_asignadas,
        })

    return render(request, 'gestion/dashboard.html', {
        'cant_alumnos': cant_alumnos,
        'cant_docentes': cant_docentes,
        'cant_comisiones': cant_comisiones,
        'cant_mesas': cant_mesas,
        'unread_notifications': unread_notifications,
    })

from django.db.models import Q

@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all().order_by('apellido')
        
    return render(request, 'gestion/lista_alumnos.html', {
        'alumnos': alumnos,
    })

@login_required
def alta_alumno(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        plan_id = request.POST.get('plan')
        
        planes_disponibles = PlanDeEstudio.objects.all()
        
        if Alumno.objects.filter(dni=dni).exists():
            messages.error(request, f"Ya existe un alumno registrado con el DNI {dni}.")
            return render(request, 'gestion/alta_alumno.html', {'planes': planes_disponibles})
            
        if Alumno.objects.filter(email=email).exists():
            messages.error(request, f"Ya existe un alumno registrado con el email {email}.")
            return render(request, 'gestion/alta_alumno.html', {'planes': planes_disponibles})
        
        try:
            from django.contrib.auth.models import User, Group
            # Creamos el usuario (username=dni, pass=dni)
            usuario, creado = User.objects.get_or_create(username=dni, defaults={'email': email or f'{dni}@test.com'})
            if creado:
                usuario.set_password(dni)
                grp, _ = Group.objects.get_or_create(name='Estudiantes')
                usuario.groups.add(grp)
                usuario.save()
            
            plan = None
            if plan_id:
                plan = get_object_or_404(PlanDeEstudio, id=plan_id)
                
            estado = request.POST.get('estado_alumno', 'ACT')
            
            # Documentos booleanos
            doc_dni = request.POST.get('doc_dni') == 'on'
            doc_vacunas = request.POST.get('doc_vacunas') == 'on'
            doc_partida = request.POST.get('doc_partida') == 'on'
            doc_primaria = request.POST.get('doc_primaria') == 'on'
            doc_pase = request.POST.get('doc_pase') == 'on'
            
            # LÓGICA AUTOMÁTICA DE ESTADOS POR DOCUMENTACIÓN
            if not doc_dni or not doc_primaria:
                if estado == 'ACT':
                    estado = 'COND_DOC'
                    messages.info(request, "Sistema: El estado del alumno se estableció en 'Condicionado (Documentación)' por falta de DNI o Título.")
            else:
                if estado == 'COND_DOC':
                    estado = 'ACT'
                    messages.info(request, "Sistema: Documentación completa. El estado del alumno pasó a 'Activo'.")
                
            Alumno.objects.create(
                usuario=usuario, dni=dni, email=email, nombre=nombre, apellido=apellido,
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                telefono=request.POST.get('telefono'),
                celular=request.POST.get('celular'),
                direccion=request.POST.get('direccion'),
                nacionalidad=request.POST.get('nacionalidad', 'Argentina'),
                codigo_postal=request.POST.get('codigo_postal'),
                comuna_zona=request.POST.get('comuna_zona'),
                provincia=request.POST.get('provincia'),
                localidad=request.POST.get('localidad'),
                sexo=request.POST.get('sexo'),
                lugar_nacimiento=request.POST.get('lugar_nacimiento'),
                plan=plan,
                estado_alumno=estado,
                doc_dni=doc_dni,
                doc_vacunas=doc_vacunas,
                doc_partida=doc_partida,
                doc_primaria=doc_primaria,
                doc_pase=doc_pase
            )
            messages.success(request, f"¡Alumno {nombre} {apellido} creado! Puede ingresar con su email y DNI.")
            return redirect('lista_alumnos')
        except Exception as e:
            messages.error(request, f"Error al crear: {e}")
            
    planes = PlanDeEstudio.objects.all()
    return render(request, 'gestion/alta_alumno.html', {'planes': planes})

from datetime import timedelta, date

@login_required
def legajo_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    # 1. Porcentaje y avance
    total_materias = alumno.plan.materias.count() if alumno.plan else 0
    
    # 2. Acreditadas (Equivalencias + Finales + Promociones)
    acreditadas = []
    
    for eq in alumno.equivalencias.all():
        acreditadas.append({
            'materia': eq.materia,
            'tipo': 'Equivalencia',
            'nota': '-',
            'fecha': eq.fecha_otorgamiento,
            'detalle': f"Res: {eq.resolucion}"
        })
        
    for insc in alumno.inscripciones.filter(estado='PROM'):
        # Buscar la nota final o promedio si la hay
        nota_obj = insc.notas.last()
        nota_val = nota_obj.valor_nota if nota_obj else '-'
        acreditadas.append({
            'materia': insc.comision.materia,
            'tipo': 'Promoción',
            'nota': nota_val,
            'fecha': insc.comision.fecha_fin or date.today(),
            'detalle': f"Comisión: {insc.comision.ciclo_lectivo}"
        })
        
    for mesa_insc in alumno.mesas_inscriptas.filter(estado='APR'):
        acreditadas.append({
            'materia': mesa_insc.mesa.materia,
            'tipo': 'Final',
            'nota': mesa_insc.nota_final,
            'fecha': mesa_insc.mesa.fecha_hora.date(),
            'detalle': f"Libro: {mesa_insc.mesa.libro or '-'} Folio: {mesa_insc.mesa.folio or '-'}"
        })
        
    total_acreditadas = len(acreditadas)
    porcentaje_avance = (total_acreditadas / total_materias * 100) if total_materias > 0 else 0
    
    # Ordenar acreditadas por fecha descendente
    acreditadas.sort(key=lambda x: x['fecha'], reverse=True)
    
    # 3. Cursando (Activas)
    cursando = alumno.inscripciones.filter(estado='REG', comision__cerrada=False)
    
    # 4. Regulares (Final Pendiente) y Libres/Recursar
    regulares_db = alumno.inscripciones.filter(estado='REG', comision__cerrada=True)
    libres_db = list(alumno.inscripciones.filter(estado='LIB'))
    
    regulares = []
    recursar = libres_db.copy()
    
    def sumar_años(d, anios):
        try:
            return d.replace(year=d.year + anios)
        except ValueError:
            return d + timedelta(days=365 * anios)
            
    hoy = date.today()
    
    for reg in regulares_db:
        # Calcular fecha vencimiento
        fecha_fin_cursada = reg.comision.fecha_fin or reg.fecha_inscripcion
        fecha_vencimiento = sumar_años(fecha_fin_cursada, 3)
        vencida_por_tiempo = hoy > fecha_vencimiento
        
        # Calcular intentos (Mesas REP)
        intentos = reg.alumno.mesas_inscriptas.filter(mesa__materia=reg.comision.materia, estado='REP').count()
        vencida_por_intentos = intentos >= 3
        
        item = {
            'inscripcion': reg,
            'materia': reg.comision.materia,
            'vencimiento': fecha_vencimiento,
            'intentos': intentos,
            'vencida': vencida_por_tiempo or vencida_por_intentos,
            'motivo_vencida': 'Por Tiempo' if vencida_por_tiempo else ('Por Intentos' if vencida_por_intentos else '')
        }
        
        if item['vencida']:
            recursar.append(reg) # Se manda a recursar
        else:
            regulares.append(item)
            
    # Agregar materias que reprobó final y quedó libre directo (si existiera el caso, aunque suele estar en LIB)
    
    context = {
        'alumno': alumno,
        'total_materias': total_materias,
        'total_acreditadas': total_acreditadas,
        'materias_faltantes': total_materias - total_acreditadas,
        'porcentaje_avance': int(porcentaje_avance),
        'acreditadas': acreditadas,
        'cursando': cursando,
        'regulares': regulares,
        'recursar': recursar
    }
    
    return render(request, 'gestion/legajo_alumno.html', context)

@login_required
def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    planes = PlanDeEstudio.objects.all()
    
    if request.method == 'POST':
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        
        # Validar duplicados ignorando al propio alumno
        if Alumno.objects.exclude(id=alumno.id).filter(dni=dni).exists():
            messages.error(request, f"Ya existe OTRO alumno registrado con el DNI {dni}.")
            return render(request, 'gestion/editar_alumno.html', {'alumno': alumno, 'planes': planes})
            
        if email and Alumno.objects.exclude(id=alumno.id).filter(email=email).exists():
            messages.error(request, f"Ya existe OTRO alumno registrado con el email {email}.")
            return render(request, 'gestion/editar_alumno.html', {'alumno': alumno, 'planes': planes})
            
        alumno.dni = dni
        alumno.nombre = request.POST.get('nombre')
        alumno.apellido = request.POST.get('apellido')
        
        fecha_nac = request.POST.get('fecha_nacimiento')
        if fecha_nac:
            alumno.fecha_nacimiento = fecha_nac
            
        plan_id = request.POST.get('plan')
        if plan_id:
            alumno.plan = get_object_or_404(PlanDeEstudio, id=plan_id)
        else:
            alumno.plan = None
            
        alumno.telefono = request.POST.get('telefono')
        alumno.celular = request.POST.get('celular')
        alumno.direccion = request.POST.get('direccion')
        alumno.nacionalidad = request.POST.get('nacionalidad', 'Argentina')
        alumno.codigo_postal = request.POST.get('codigo_postal')
        alumno.comuna_zona = request.POST.get('comuna_zona')
        alumno.provincia = request.POST.get('provincia')
        alumno.localidad = request.POST.get('localidad')
        alumno.sexo = request.POST.get('sexo')
        alumno.lugar_nacimiento = request.POST.get('lugar_nacimiento')
        alumno.email = email
        alumno.estado_alumno = request.POST.get('estado_alumno', alumno.estado_alumno)
        
        # Documentos booleanos
        doc_dni = request.POST.get('doc_dni') == 'on'
        doc_vacunas = request.POST.get('doc_vacunas') == 'on'
        doc_partida = request.POST.get('doc_partida') == 'on'
        doc_primaria = request.POST.get('doc_primaria') == 'on'
        doc_pase = request.POST.get('doc_pase') == 'on'
        
        estado = request.POST.get('estado_alumno', alumno.estado_alumno)
        
        # LÓGICA AUTOMÁTICA DE ESTADOS POR DOCUMENTACIÓN
        if not doc_dni or not doc_primaria:
            if estado == 'ACT':
                estado = 'COND_DOC'
                messages.info(request, "Sistema: El estado del alumno se estableció en 'Condicionado (Documentación)' por falta de DNI o Título.")
        else:
            if estado == 'COND_DOC':
                estado = 'ACT'
                messages.info(request, "Sistema: Documentación completa. El estado del alumno pasó a 'Activo'.")
        
        alumno.doc_dni = doc_dni
        alumno.doc_vacunas = doc_vacunas
        alumno.doc_partida = doc_partida
        alumno.doc_primaria = doc_primaria
        alumno.doc_pase = doc_pase
        alumno.estado_alumno = estado
        
        try:
            alumno.save()
            # Actualizamos el email en el usuario vinculado si existe
            if alumno.usuario:
                alumno.usuario.email = alumno.email
                alumno.usuario.username = alumno.email
                alumno.usuario.save()
            messages.success(request, f"¡Datos de {alumno.nombre} actualizados con éxito!")
            return redirect('legajo_alumno', alumno_id=alumno.id)
        except Exception as e:
            messages.error(request, f"Error al actualizar: {e}")
            
    return render(request, 'gestion/editar_alumno.html', {'alumno': alumno, 'planes': planes})

@login_required
def constancia_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    return render(request, 'gestion/constancia_impresion.html', {'alumno': alumno})

@login_required
def boletin_alumno(request, alumno_id, ciclo_lectivo):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    return render(request, 'gestion/boletin_impresion.html', {'alumno': alumno})

@login_required
def lista_docentes(request):
    docentes = Docente.objects.all()
    return render(request, 'gestion/lista_docentes.html', {'docentes': docentes})

@login_required
def alta_docente(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        
        if Docente.objects.filter(dni=dni).exists():
            messages.error(request, f"Ya existe un docente registrado con el DNI {dni}.")
            return render(request, 'gestion/alta_docente.html')
            
        if email and Docente.objects.filter(email=email).exists():
            messages.error(request, f"Ya existe un docente registrado con el email {email}.")
            return render(request, 'gestion/alta_docente.html')
        
        try:
            from django.contrib.auth.models import User, Group
            # Siempre usamos el DNI como nombre de usuario para evitar confusiones
            username_base = dni
            usuario, creado = User.objects.get_or_create(username=username_base, defaults={'email': email or ''})
            if creado:
                usuario.set_password(dni)
                grp, _ = Group.objects.get_or_create(name='Docentes')
                usuario.groups.add(grp)
                usuario.save()
            
            # Fetch date to properly assign None if empty string
            fecha_nac = request.POST.get('fecha_nacimiento')
            fecha_nacimiento = fecha_nac if fecha_nac else None
            
            Docente.objects.create(
                usuario=usuario, dni=dni, email=email, nombre=nombre, apellido=apellido,
                telefono=request.POST.get('telefono'),
                fecha_nacimiento=fecha_nacimiento,
                celular=request.POST.get('celular'),
                direccion=request.POST.get('direccion'),
                nacionalidad=request.POST.get('nacionalidad') or 'Argentina',
                codigo_postal=request.POST.get('codigo_postal'),
                comuna_zona=request.POST.get('comuna_zona'),
                provincia=request.POST.get('provincia'),
                localidad=request.POST.get('localidad'),
                sexo=request.POST.get('sexo'),
                lugar_nacimiento=request.POST.get('lugar_nacimiento')
            )
            messages.success(request, f"¡Docente {nombre} {apellido} creado! Puede ingresar con su email/DNI.")
            return redirect('lista_docentes')
        except Exception as e:
            messages.error(request, f"Error al crear: {e}")
            
    # Para los selects del template:
    provincias = Docente.PROVINCIAS
    sexo_choices = Docente.SEXO_CHOICES
    return render(request, 'gestion/alta_docente.html', {'provincias': provincias, 'sexo_choices': sexo_choices})

@login_required
def editar_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    
    if request.method == 'POST':
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        
        # Check uniqueness excluding the current teacher
        if Docente.objects.filter(dni=dni).exclude(id=docente_id).exists():
            messages.error(request, f"Ya existe otro docente registrado con el DNI {dni}.")
            return render(request, 'gestion/editar_docente.html', {'docente': docente, 'provincias': Docente.PROVINCIAS, 'sexo_choices': Docente.SEXO_CHOICES})
            
        if email and Docente.objects.filter(email=email).exclude(id=docente_id).exists():
            messages.error(request, f"Ya existe otro docente registrado con el email {email}.")
            return render(request, 'gestion/editar_docente.html', {'docente': docente, 'provincias': Docente.PROVINCIAS, 'sexo_choices': Docente.SEXO_CHOICES})
            
        try:
            # Update User if email changed
            if docente.usuario and docente.email != email and email:
                usuario = docente.usuario
                usuario.email = email
                usuario.username = email
                usuario.save()
                
            # Update Docente
            docente.dni = dni
            docente.email = email
            docente.nombre = nombre
            docente.apellido = apellido
            docente.telefono = telefono
            
            fecha_nac = request.POST.get('fecha_nacimiento')
            docente.fecha_nacimiento = fecha_nac if fecha_nac else None
            
            docente.celular = request.POST.get('celular')
            docente.direccion = request.POST.get('direccion')
            docente.nacionalidad = request.POST.get('nacionalidad') or 'Argentina'
            docente.codigo_postal = request.POST.get('codigo_postal')
            docente.comuna_zona = request.POST.get('comuna_zona')
            docente.provincia = request.POST.get('provincia')
            docente.localidad = request.POST.get('localidad')
            docente.sexo = request.POST.get('sexo')
            docente.lugar_nacimiento = request.POST.get('lugar_nacimiento')
            
            docente.save()
            
            messages.success(request, "¡Datos del docente actualizados correctamente!")
            return redirect('lista_docentes')
        except Exception as e:
            messages.error(request, f"Error al actualizar: {e}")
            
    return render(request, 'gestion/editar_docente.html', {'docente': docente, 'provincias': Docente.PROVINCIAS, 'sexo_choices': Docente.SEXO_CHOICES})

@login_required
def legajo_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    return render(request, 'gestion/legajo_docente.html', {'docente': docente})

@login_required
def lista_comisiones(request):
    comisiones = Comision.objects.all().order_by('-ciclo_lectivo', 'materia__nombre')
    
    query = request.GET.get('q', '')
    plan_id = request.GET.get('plan', '')
    ciclo = request.GET.get('ciclo', '')
    
    if query:
        comisiones = comisiones.filter(materia__nombre__icontains=query)
    if plan_id:
        comisiones = comisiones.filter(materia__plan_id=plan_id)
    if ciclo:
        comisiones = comisiones.filter(ciclo_lectivo=ciclo)
        
    planes = PlanDeEstudio.objects.all().order_by('nombre')
    ciclos_disponibles = Comision.objects.values_list('ciclo_lectivo', flat=True).distinct().order_by('-ciclo_lectivo')
    
    return render(request, 'gestion/lista_comisiones.html', {
        'comisiones': comisiones,
        'planes': planes,
        'ciclos': ciclos_disponibles,
        'q': query,
        'plan_id': int(plan_id) if plan_id else '',
        'ciclo_sel': int(ciclo) if ciclo else '',
    })

@login_required
def apertura_masiva(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        ciclo_lectivo = request.POST.get('ciclo_lectivo')
        cuatrimestre = request.POST.get('cuatrimestre')
        materias_ids = request.POST.getlist('materias')
        
        if not (plan_id and ciclo_lectivo and cuatrimestre and materias_ids):
            messages.error(request, "Por favor complete todos los campos y seleccione al menos una materia.")
            return redirect('apertura_masiva')
            
        plan = get_object_or_404(PlanDeEstudio, id=plan_id)
        
        # Validar ciclo lectivo
        try:
            ciclo_lectivo = int(ciclo_lectivo)
        except ValueError:
            messages.error(request, "Año lectivo inválido.")
            return redirect('apertura_masiva')

        creadas = 0
        omitidas = 0
        
        for m_id in materias_ids:
            materia = get_object_or_404(Materia, id=m_id)
            # Evitar duplicados
            if not Comision.objects.filter(materia=materia, ciclo_lectivo=ciclo_lectivo, cuatrimestre=cuatrimestre).exists():
                Comision.objects.create(
                    materia=materia,
                    ciclo_lectivo=ciclo_lectivo,
                    cuatrimestre=cuatrimestre,
                    tipo_aprobacion='FIN', # Default
                    modalidad='P', # Default
                    inscripciones_abiertas=True,
                    cerrada=False
                )
                creadas += 1
            else:
                omitidas += 1
                
        if creadas > 0:
            messages.success(request, f"¡Éxito! Se abrieron {creadas} comisiones para el {cuatrimestre} {ciclo_lectivo} del plan {plan.nombre}.")
        if omitidas > 0:
            messages.warning(request, f"Se omitieron {omitidas} materias porque ya tenían una comisión abierta para ese período.")
            
        return redirect('lista_comisiones')

    planes = PlanDeEstudio.objects.all()
    
    # Preparar datos JSON para el front-end
    planes_data = {}
    for plan in planes:
        materias_agrupadas = {}
        for m in plan.materias.order_by('año_dictado', 'nombre'):
            if m.año_dictado not in materias_agrupadas:
                materias_agrupadas[m.año_dictado] = []
            materias_agrupadas[m.año_dictado].append({
                'id': m.id,
                'nombre': m.nombre,
                'cuatrimestre_dictado': m.cuatrimestre_dictado,
            })
        planes_data[plan.id] = materias_agrupadas

    return render(request, 'gestion/apertura_masiva.html', {
        'planes': planes,
        'planes_json': json.dumps(planes_data),
        'proximo_año': date.today().year + 1
    })

@login_required
def alta_comision(request):
    materias = Materia.objects.all().order_by('año_dictado', 'nombre')
    docentes = Docente.objects.all().order_by('apellido')
    
    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        docente_id = request.POST.get('docente')
        docente_aux_id = request.POST.get('docente_auxiliar')
        ciclo = request.POST.get('ciclo_lectivo')
        cuatrimestre = request.POST.get('cuatrimestre')
        tipo_aprobacion = request.POST.get('tipo_aprobacion')
        modalidad = request.POST.get('modalidad', 'P')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        semana_inicio_bimodal = request.POST.get('semana_inicio_bimodal') if modalidad == 'B' else None
        horarios_seleccionados = request.POST.getlist('horarios')
        
        try:
            materia = get_object_or_404(Materia, id=materia_id)
            docente = Docente.objects.filter(id=docente_id).first() if docente_id else None
            docente_aux = Docente.objects.filter(id=docente_aux_id).first() if docente_aux_id else None
            
            comision = Comision.objects.create(
                materia=materia,
                docente=docente,
                docente_auxiliar=docente_aux,
                ciclo_lectivo=ciclo,
                cuatrimestre=cuatrimestre,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo_aprobacion=tipo_aprobacion,
                modalidad=modalidad,
                semana_inicio_bimodal=semana_inicio_bimodal
            )
            
            from datetime import datetime
            for hor in horarios_seleccionados:
                dia_str, h_ini_str, h_fin_str = hor.split('_')
                h_ini = datetime.strptime(h_ini_str, '%H:%M').time()
                h_fin = datetime.strptime(h_fin_str, '%H:%M').time()
                HorarioComision.objects.create(
                    comision=comision,
                    dia=dia_str,
                    hora_inicio=h_ini,
                    hora_fin=h_fin
                )
                
            messages.success(request, f"¡Comisión para {materia.nombre} abierta con éxito!")
            return redirect('lista_comisiones')
        except Exception as e:
            messages.error(request, f"Error al crear comisión: {e}")
            
    return render(request, 'gestion/alta_comision.html', {
        'planes': PlanDeEstudio.objects.prefetch_related('materias').all(),
        'docentes': docentes,
        'ciclo_actual': date.today().year
    })

@login_required
def detalle_comision(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    
    # Validar permisos
    is_authorized = False
    if request.user.is_staff or request.user.is_superuser:
        is_authorized = True
    elif hasattr(request.user, 'perfil_docente'):
        if comision.docente == request.user.perfil_docente or comision.docente_auxiliar == request.user.perfil_docente:
            is_authorized = True
            
    if not is_authorized:
        messages.error(request, 'No tienes permiso para acceder a esta comisión.')
        return redirect('dashboard')
        
    return render(request, 'gestion/detalle_comision.html', {'comision': comision})

@login_required
def inscribir_alumno_comision(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    
    if not comision.inscripciones_abiertas:
        messages.error(request, 'Las inscripciones para esta comisión están cerradas.')
        return redirect('detalle_comision', comision_id=comision.id)
    
    # Excluir alumnos que ya están inscriptos en esta comisión y filtrar por Plan de Estudios
    alumnos_inscriptos = comision.alumnos_inscriptos.values_list('alumno_id', flat=True)
    alumnos_disponibles = Alumno.objects.filter(
        plan=comision.materia.plan
    ).exclude(
        id__in=alumnos_inscriptos
    ).order_by('apellido')
    
    if request.method == 'POST':
        alumnos_seleccionados = request.POST.getlist('alumnos_ids')
        
        exitosos = 0
        fallidos = 0
        
        for alumno_id in alumnos_seleccionados:
            alumno = Alumno.objects.get(id=alumno_id)
            
            if alumno.estado_alumno in ['INA', 'EGR', 'COND_PAG']:
                messages.warning(request, f"ATENCIÓN: {alumno.apellido}, {alumno.nombre} tiene estado '{alumno.get_estado_alumno_display()}'. Fue inscripto porque tenés permisos de Admin, pero verificá su situación.")
            
            # Validación de Correlatividades
            correlativas = Correlatividad.objects.filter(materia=comision.materia)
            puede_cursar = True
            faltan = []
            
            for corr in correlativas:
                # Buscamos inscripciones previas del alumno a la materia requerida
                inscripciones_previas = Inscripcion.objects.filter(alumno=alumno, comision__materia=corr.requisito)
                
                if corr.tipo == 'CUR':
                    # Requiere cursada regularizada o aprobada
                    cumple = inscripciones_previas.filter(estado__in=['REG', 'APR', 'PROM']).exists()
                    if not cumple:
                        puede_cursar = False
                        faltan.append(f"{corr.requisito.nombre} (Regularizada)")
                elif corr.tipo == 'APR':
                    # Requiere final aprobado o promoción
                    cumple = inscripciones_previas.filter(estado__in=['APR', 'PROM']).exists()
                    if not cumple:
                        puede_cursar = False
                        faltan.append(f"{corr.requisito.nombre} (Aprobada)")
                        
            if puede_cursar or request.POST.get('force') == 'true':
                Inscripcion.objects.create(alumno=alumno, comision=comision, estado='REG')
                exitosos += 1
                if not puede_cursar:
                    messages.warning(request, f"Excepción administrativa: {alumno.apellido}, {alumno.nombre} inscripto sin correlativas.")
            else:
                fallidos += 1
                messages.error(request, f"{alumno.apellido}, {alumno.nombre} NO cumple las correlativas. Le falta: {', '.join(faltan)}", extra_tags=f"force_comision,{comision.id},{alumno.id}")
                
        if exitosos > 0:
            messages.success(request, f"Se inscribieron {exitosos} alumnos a {comision.materia.nombre}.")
            
        return redirect('detalle_comision', comision_id=comision.id)
        
    return render(request, 'gestion/inscribir_alumno_comision.html', {
        'comision': comision,
        'alumnos': alumnos_disponibles
    })

@login_required
def lista_comisiones_asistencia(request):
    comisiones = Comision.objects.all()
    return render(request, 'gestion/asistencia_comisiones.html', {'comisiones': comisiones})

@login_required
def cargar_asistencia(request, comision_id):
    from .services import generar_planilla_del_dia
    from datetime import datetime
    comision = get_object_or_404(Comision, id=comision_id)
    
    is_authorized = False
    if request.user.is_staff or request.user.is_superuser:
        is_authorized = True
    elif hasattr(request.user, 'perfil_docente'):
        if comision.docente == request.user.perfil_docente or comision.docente_auxiliar == request.user.perfil_docente:
            is_authorized = True
            
    if not is_authorized:
        messages.error(request, 'No tienes permiso para cargar asistencia en esta comisión.')
        return redirect('dashboard')
    
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        try:
            fecha_elegida = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_elegida = date.today()
    else:
        fecha_elegida = date.today()
        
    # Validar que los docentes no puedan editar asistencias muy antiguas (ej: más de 30 días)
    if not (request.user.is_staff or request.user.is_superuser):
        dias_diferencia = (date.today() - fecha_elegida).days
        if dias_diferencia > 30 or dias_diferencia < 0:
            messages.error(request, 'No tienes permiso para modificar o crear asistencias fuera del mes actual. Contacta a secretaría.')
            return redirect('detalle_comision', comision_id=comision.id)

    se_pudo_crear, mensaje_estado = generar_planilla_del_dia(comision, fecha_elegida)
    planilla = PlanillaDiaria.objects.filter(comision=comision, fecha=fecha_elegida).first()
    
    if request.method == 'POST' and planilla:
        for registro in planilla.registros.all():
            nuevo_estado = request.POST.get(f'asistencia_{registro.id}')
            if nuevo_estado:
                registro.estado = nuevo_estado
                registro.save()
        messages.success(request, f"¡Asistencia del {fecha_elegida.strftime('%d/%m/%Y')} guardada con éxito!")
        return redirect('detalle_comision', comision_id=comision.id)

    return render(request, 'gestion/asistencia_form.html', {
        'planilla': planilla, 
        'comision': comision,
        'fecha_elegida': fecha_elegida,
        'se_pudo_crear': se_pudo_crear,
        'mensaje_estado': mensaje_estado
    })

@login_required
def cargar_notas(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    
    is_authorized = False
    if request.user.is_staff or request.user.is_superuser:
        is_authorized = True
    elif hasattr(request.user, 'perfil_docente'):
        if comision.docente == request.user.perfil_docente or comision.docente_auxiliar == request.user.perfil_docente:
            is_authorized = True
            
    if not is_authorized:
        messages.error(request, 'No tienes permiso para cargar notas en esta comisión.')
        return redirect('dashboard')
    
    if comision.cerrada:
        messages.error(request, 'La comisión está cerrada. No se pueden modificar las notas.')
        return redirect('detalle_comision', comision_id=comision.id)
        
    # Obtener todas las inscripciones, no solo las regulares, porque el docente podría querer
    # agregar una nota a un alumno que ya está Libre o Promocionado.
    inscripciones = Inscripcion.objects.filter(comision=comision).prefetch_related('notas')
    
    if request.method == 'POST':
        instancia_post = request.POST.get('instancia')
        cerrar_cursada = request.POST.get('cerrar_cursada') == 'on'
        
        if not instancia_post:
            messages.error(request, 'Debes indicar el nombre de la Instancia de evaluación.')
            return redirect('cargar_notas', comision_id=comision.id)

        notas_guardadas = 0
        for insc in inscripciones:
            nota_valor = request.POST.get(f'nota_{insc.id}')
            if nota_valor:
                # Crear una nueva nota siempre, construyendo el historial
                Nota.objects.create(
                    inscripcion=insc,
                    instancia=instancia_post,
                    valor_nota=nota_valor
                )
                notas_guardadas += 1
            
            # Si se solicita cerrar la cursada, se calcula el estado automáticamente
            if cerrar_cursada:
                todas_las_notas = insc.notas.all()
                if todas_las_notas.exists():
                    promedio = sum([n.valor_nota for n in todas_las_notas]) / todas_las_notas.count()
                    todas_mayor_o_igual_7 = all(n.valor_nota >= 7 for n in todas_las_notas)
                    
                    if todas_mayor_o_igual_7:
                        if comision.tipo_aprobacion == 'PROM':
                            nuevo_estado = 'PROM'
                        else:
                            nuevo_estado = 'REG'
                    else:
                        if promedio >= 4:
                            nuevo_estado = 'REG'
                        else:
                            nuevo_estado = 'LIB'
                    
                    insc.estado = nuevo_estado
                    insc.save()
                
        if cerrar_cursada:
            comision.cerrada = True
            comision.save()
            messages.success(request, f"¡Notas de '{instancia_post}' guardadas y cursada CERRADA automáticamente para los alumnos evaluados!")
        else:
            messages.success(request, f"¡Se guardaron {notas_guardadas} notas para la instancia '{instancia_post}'!")
            
        return redirect('detalle_comision', comision_id=comision.id)

    return render(request, 'gestion/cargar_notas.html', {
        'comision': comision,
        'inscripciones': inscripciones,
        'estados': Inscripcion.ESTADOS_POSIBLES
    })

@login_required
def eliminar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    comision_id = nota.inscripcion.comision.id
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada correctamente.')
    return redirect('detalle_comision', comision_id=comision_id)

@login_required
def detalle_plan(request, plan_id):
    plan = get_object_or_404(PlanDeEstudio, id=plan_id)
    return render(request, 'gestion/detalle_plan.html', {'plan': plan})

from django.views.decorators.csrf import csrf_exempt
from .services_ia import procesar_mensaje_chatbot

def api_chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '')
            alumno_id = data.get('alumno_id', 1) 
            respuesta_ia = procesar_mensaje_chatbot(mensaje, alumno_id)
            return JsonResponse({'respuesta': respuesta_ia})
        except Exception as e:
            return JsonResponse({'respuesta': f"Error interno: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Solo POST permitido'}, status=405)

@login_required
def calendario_general(request):
    from .models import HorarioComision, EventoInstitucional, PlanDeEstudio, MesaExamen
    horarios = HorarioComision.objects.all().select_related('comision__materia', 'comision__docente')
    
    eventos = []
    
    for h in horarios:
        dia_fc = int(h.dia) 
        prof = f"Prof. {h.comision.docente.apellido}" if h.comision.docente else "A designar"
        
        evento = {
            'title': f"{h.comision.materia.nombre} ({prof})",
            'startTime': h.hora_inicio.strftime('%H:%M'),
            'endTime': h.hora_fin.strftime('%H:%M'),
            'daysOfWeek': [dia_fc],
            'url': f"/comisiones/{h.comision.id}/",
            'extendedProps': {
                'plan_id': h.comision.materia.plan_id,
                'tipo': 'CLASE'
            }
        }
        
        if h.comision.fecha_inicio:
            evento['startRecur'] = h.comision.fecha_inicio.strftime('%Y-%m-%d')
        if h.comision.fecha_fin:
            # Fullcalendar endRecur es exclusivo, sumamos 1 día para incluir el último
            fecha_fin = h.comision.fecha_fin + timedelta(days=1)
            evento['endRecur'] = fecha_fin.strftime('%Y-%m-%d')
            
        eventos.append(evento)

    institucionales = EventoInstitucional.objects.all()
    for evt in institucionales:
        e = {
            'title': evt.titulo,
            'start': evt.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S') if not evt.todo_el_dia else evt.fecha_inicio.strftime('%Y-%m-%d'),
            'allDay': evt.todo_el_dia,
            'extendedProps': {
                'tipo': evt.tipo,
                'descripcion': evt.descripcion
            }
        }
        if evt.fecha_fin:
            if evt.todo_el_dia:
                # Fullcalendar allDay end es exclusivo
                fecha_fin = evt.fecha_fin + timedelta(days=1)
                e['end'] = fecha_fin.strftime('%Y-%m-%d')
            else:
                e['end'] = evt.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S')
                
        if evt.tipo == 'FERIADO':
            e['color'] = '#dc3545'
        elif evt.tipo == 'EXAMEN':
            e['color'] = '#ffc107'
            e['textColor'] = '#000'
        else:
            e['color'] = '#17a2b8'
            
        eventos.append(e)

    # MESAS DE EXAMEN
    mesas = MesaExamen.objects.all().select_related('materia', 'presidente_mesa')
    for m in mesas:
        prof = f"Prof. {m.presidente_mesa.apellido}" if m.presidente_mesa else "A designar"
        e = {
            'title': f"MESA: {m.materia.nombre} ({prof})",
            'start': m.fecha_hora.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': (m.fecha_hora + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S'), # Asumimos 2 horas por mesa
            'allDay': False,
            'url': f"/mesas/{m.id}/",
            'color': '#6f42c1', # Púrpura para mesas de examen
            'textColor': '#fff',
            'extendedProps': {
                'plan_id': m.materia.plan_id,
                'tipo': 'MESA_EXAMEN',
                'descripcion': f"Turno: {m.get_turno_display()}"
            }
        }
        eventos.append(e)

    planes = PlanDeEstudio.objects.all().order_by('nombre')
        
    return render(request, 'gestion/calendario.html', {
        'eventos_json': json.dumps(eventos),
        'planes': planes
    })

@login_required
def alta_evento_calendario(request):
    from .models import EventoInstitucional
    if request.method == 'POST':
        try:
            titulo = request.POST.get('titulo')
            tipo = request.POST.get('tipo')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            todo_el_dia = request.POST.get('todo_el_dia') == 'on'
            descripcion = request.POST.get('descripcion', '')

            if not titulo or not fecha_inicio:
                return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)

            evt = EventoInstitucional(
                titulo=titulo,
                tipo=tipo,
                fecha_inicio=fecha_inicio,
                todo_el_dia=todo_el_dia,
                descripcion=descripcion
            )
            if fecha_fin:
                evt.fecha_fin = fecha_fin
            evt.save()

            return JsonResponse({'success': True, 'msg': 'Evento creado correctamente.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def calendario_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    # Comisiones a las que está inscripto
    inscripciones = Inscripcion.objects.filter(alumno=alumno, estado='REG')
    comisiones_ids = inscripciones.values_list('comision_id', flat=True)
    
    from .models import HorarioComision
    horarios = HorarioComision.objects.filter(comision_id__in=comisiones_ids).select_related('comision__materia', 'comision__docente')
    
    eventos = []
    for h in horarios:
        prof = f"Prof. {h.comision.docente.apellido}" if h.comision.docente else "A designar"
        eventos.append({
            'title': f"{h.comision.materia.nombre} ({prof})",
            'startTime': h.hora_inicio.strftime('%H:%M'),
            'endTime': h.hora_fin.strftime('%H:%M'),
            'daysOfWeek': [int(h.dia)],
            'url': f"/comisiones/{h.comision.id}/"
        })
        
    return render(request, 'gestion/calendario_personalizado.html', {
        'eventos_json': json.dumps(eventos),
        'titulo': f'Calendario Académico - {alumno.nombre} {alumno.apellido}'
    })

@login_required
def calendario_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    
    from .models import HorarioComision
    horarios = HorarioComision.objects.filter(Q(comision__docente=docente) | Q(comision__docente_auxiliar=docente)).select_related('comision__materia')
    
    eventos = []
    for h in horarios:
        eventos.append({
            'title': f"{h.comision.materia.nombre} - Com. {h.comision.id}",
            'startTime': h.hora_inicio.strftime('%H:%M'),
            'endTime': h.hora_fin.strftime('%H:%M'),
            'daysOfWeek': [int(h.dia)],
            'url': f"/comisiones/{h.comision.id}/"
        })
        
    return render(request, 'gestion/calendario_personalizado.html', {
        'eventos_json': json.dumps(eventos),
        'titulo': f'Calendario Docente - Prof. {docente.apellido}'
    })

@login_required
def imprimir_lista_asistencia(request, comision_id):
    from datetime import timedelta
    comision = get_object_or_404(Comision, id=comision_id)
    inscripciones = Inscripcion.objects.filter(comision=comision).select_related('alumno').order_by('alumno__apellido')
    
    fechas_clases = []
    
    if comision.fecha_inicio and comision.fecha_fin:
        # Obtenemos los días de la semana en los que hay clase (1=Lunes, 2=Martes... 6=Sábado)
        # Convertimos al formato isoweekday() de Python (1=Lunes ... 7=Domingo)
        dias_clase = list(comision.horarios.values_list('dia', flat=True).distinct())
        dias_clase_iso = [int(d) for d in dias_clase]
        
        # Calcular todas las fechas entre inicio y fin que caigan en los dias_clase
        fecha_actual = comision.fecha_inicio
        
        # Para modalidad bimodal, determinamos en qué semana de calendario empieza.
        # Asumimos que la "semana 1" de la materia es la semana de fecha_inicio.
        # Podemos usar el número de semana ISO para saber si una semana es par o impar relativo al inicio.
        iso_semana_inicio = comision.fecha_inicio.isocalendar()[1]
        
        while fecha_actual <= comision.fecha_fin:
            if fecha_actual.isoweekday() in dias_clase_iso:
                modalidad_clase = comision.get_modalidad_display()
                
                if comision.modalidad == 'B':
                    iso_semana_actual = fecha_actual.isocalendar()[1]
                    diferencia_semanas = iso_semana_actual - iso_semana_inicio
                    # Si diferencia es par, es la misma modalidad que la semana_inicio_bimodal
                    if diferencia_semanas % 2 == 0:
                        es_presencial = (comision.semana_inicio_bimodal == 'P')
                    else:
                        es_presencial = (comision.semana_inicio_bimodal == 'V')
                        
                    modalidad_clase = 'Presencial' if es_presencial else 'Virtual'

                fechas_clases.append({
                    'fecha': fecha_actual,
                    'modalidad': modalidad_clase
                })
            fecha_actual += timedelta(days=1)
            
    return render(request, 'gestion/imprimir_lista_asistencia.html', {
        'comision': comision,
        'inscripciones': inscripciones,
        'fechas_clases': fechas_clases
    })

@login_required
def editar_comision(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    
    if request.method == 'POST':
        docente_id = request.POST.get('docente')
        docente_aux_id = request.POST.get('docente_auxiliar')
        ciclo = request.POST.get('ciclo_lectivo')
        cuatrimestre = request.POST.get('cuatrimestre')
        tipo_aprobacion = request.POST.get('tipo_aprobacion')
        modalidad = request.POST.get('modalidad', 'P')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        semana_inicio_bimodal = request.POST.get('semana_inicio_bimodal') if modalidad == 'B' else None
        horarios_seleccionados = request.POST.getlist('horarios')
        
        try:
            docente = Docente.objects.filter(id=docente_id).first() if docente_id else None
            docente_aux = Docente.objects.filter(id=docente_aux_id).first() if docente_aux_id else None
            
            comision.docente = docente
            comision.docente_auxiliar = docente_aux
            comision.ciclo_lectivo = ciclo
            comision.cuatrimestre = cuatrimestre
            comision.fecha_inicio = fecha_inicio if fecha_inicio else None
            comision.fecha_fin = fecha_fin if fecha_fin else None
            comision.tipo_aprobacion = tipo_aprobacion
            comision.modalidad = modalidad
            comision.semana_inicio_bimodal = semana_inicio_bimodal
            comision.save()
            
            # Recrear horarios
            comision.horarios.all().delete()
            from datetime import datetime
            for hor in horarios_seleccionados:
                dia_str, h_ini_str, h_fin_str = hor.split('_')
                h_ini = datetime.strptime(h_ini_str, '%H:%M').time()
                h_fin = datetime.strptime(h_fin_str, '%H:%M').time()
                HorarioComision.objects.create(
                    comision=comision,
                    dia=dia_str,
                    hora_inicio=h_ini,
                    hora_fin=h_fin
                )
                
            messages.success(request, 'Comisión actualizada correctamente.')
            return redirect('detalle_comision', comision_id=comision.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')
            
    docentes = Docente.objects.all().order_by('apellido')
    
    # Formatear horarios actuales para los checkboxes "dia_hini_hfin"
    horarios_actuales = [
        f"{h.dia}_{h.hora_inicio.strftime('%H:%M')}_{h.hora_fin.strftime('%H:%M')}"
        for h in comision.horarios.all()
    ]
    
    return render(request, 'gestion/editar_comision.html', {
        'comision': comision,
        'docentes': docentes,
        'horarios_actuales': horarios_actuales
    })

@login_required
def toggle_inscripcion_comision(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    comision.inscripciones_abiertas = not comision.inscripciones_abiertas
    comision.save()
    estado = "abiertas" if comision.inscripciones_abiertas else "cerradas"
    messages.success(request, f'Las inscripciones ahora están {estado}.')
    return redirect('detalle_comision', comision_id=comision.id)

@login_required
def cerrar_comision(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    comision.cerrada = True
    comision.inscripciones_abiertas = False
    comision.save()
    messages.success(request, 'La comisión ha sido cerrada definitivamente. Ya no se pueden cargar notas ni asistencias.')
    return redirect('detalle_comision', comision_id=comision.id)

@login_required
def eliminar_comision(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    if request.method == 'POST':
        comision.delete()
        messages.success(request, 'La comisión y todos sus datos han sido eliminados correctamente.')
        return redirect('lista_comisiones')
    return redirect('detalle_comision', comision_id=comision.id)

@login_required
def acta_volante(request, comision_id):
    comision = get_object_or_404(Comision, id=comision_id)
    inscripciones = Inscripcion.objects.filter(comision=comision).select_related('alumno').order_by('alumno__apellido')
    
    # Preprocesar datos para el acta volante (Promoción o Final)
    datos_acta = []
    from decimal import Decimal
    
    for insc in inscripciones:
        notas = insc.notas.all()
        promociona = False
        condicion = "Regular"
        nota_definitiva = ""
        
        # Lógica de Promoción: todas las notas >= 7 (según indicaciones del usuario)
        if comision.tipo_aprobacion == 'PROM' and notas.exists():
            todas_mayores_7 = all(n.valor_nota >= Decimal('7.00') for n in notas)
            if todas_mayores_7:
                promociona = True
                condicion = "Promocionado"
                # Calculamos promedio para la nota final de promoción
                nota_definitiva = sum(n.valor_nota for n in notas) / notas.count()
                nota_definitiva = round(nota_definitiva, 2)
            else:
                condicion = "Regular (Va a Final)"
                
        datos_acta.append({
            'alumno': insc.alumno,
            'notas': notas,
            'condicion': condicion,
            'nota_definitiva': nota_definitiva
        })
        
    return render(request, 'gestion/acta_volante.html', {
        'comision': comision,
        'datos_acta': datos_acta,
        'fecha_actual': date.today()
    })

# ==========================================
# GESTIÓN DE MESAS DE EXAMEN (FINALES)
# ==========================================

@login_required
def lista_mesas(request):
    from .models import MesaExamen
    # Obtener todas las mesas agrupadas por ciclo lectivo y ordenadas por fecha
    mesas = MesaExamen.objects.all().order_by('-ciclo_lectivo', 'fecha_hora')
    return render(request, 'gestion/lista_mesas.html', {'mesas': mesas})

@login_required
def alta_mesa(request):
    from .models import Materia, MesaExamen, Docente
    from datetime import datetime
    
    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        turno = request.POST.get('turno')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        
        presidente_id = request.POST.get('presidente')
        vocal_1_id = request.POST.get('vocal_1')
        vocal_2_id = request.POST.get('vocal_2')
        
        ciclo = request.POST.get('ciclo_lectivo', date.today().year)
        
        try:
            materia = get_object_or_404(Materia, id=materia_id)
            fecha_hora_str = f"{fecha} {hora}"
            fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
            
            presidente = Docente.objects.get(id=presidente_id) if presidente_id else None
            vocal_1 = Docente.objects.get(id=vocal_1_id) if vocal_1_id else None
            vocal_2 = Docente.objects.get(id=vocal_2_id) if vocal_2_id else None
            
            mesa = MesaExamen.objects.create(
                materia=materia,
                turno=turno,
                fecha_hora=fecha_hora,
                presidente_mesa=presidente,
                vocal_1=vocal_1,
                vocal_2=vocal_2,
                ciclo_lectivo=ciclo
            )
            messages.success(request, 'Mesa de examen creada con éxito.')
            return redirect('detalle_mesa', mesa_id=mesa.id)
        except Docente.DoesNotExist:
            messages.error(request, 'Error: Docente no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al crear mesa: {str(e)}')
            
    planes = PlanDeEstudio.objects.prefetch_related('materias').all()
    docentes = Docente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'gestion/alta_mesa.html', {
        'planes': planes, 
        'ciclo_actual': date.today().year,
        'docentes': docentes
    })

@login_required
def eliminar_mesa(request, mesa_id):
    from .models import MesaExamen
    mesa = get_object_or_404(MesaExamen, id=mesa_id)
    
    if request.method == 'POST':
        mesa.delete()
        messages.success(request, 'La mesa de examen ha sido eliminada con éxito.')
        return redirect('lista_mesas')
        
    return render(request, 'gestion/eliminar_mesa.html', {'mesa': mesa})

@login_required
def detalle_mesa(request, mesa_id):
    from .models import MesaExamen
    mesa = get_object_or_404(MesaExamen, id=mesa_id)
    return render(request, 'gestion/detalle_mesa.html', {'mesa': mesa})

from datetime import timedelta, date

@login_required
def inscribir_alumno_mesa(request, mesa_id):
    from .models import MesaExamen, InscripcionMesa, Correlatividad
    mesa = get_object_or_404(MesaExamen, id=mesa_id)
    
    if mesa.cerrada:
        messages.error(request, 'La mesa está cerrada. No se pueden inscribir más alumnos.')
        return redirect('detalle_mesa', mesa_id=mesa.id)
        
    inscriptos_mesa = mesa.inscriptos.values_list('alumno_id', flat=True)

    # Filtrar estrictamente solo alumnos que tengan la cursada Regular y la comisión ya esté CERRADA
    inscripciones_validas = Inscripcion.objects.filter(
        comision__materia=mesa.materia,
        comision__cerrada=True,
        estado='REG'
    )
    alumnos_ids_cursada = inscripciones_validas.values_list('alumno_id', flat=True)
    
    # Obtener los alumnos básicos disponibles (sin contar los que ya están en esta mesa)
    alumnos_candidatos = Alumno.objects.filter(id__in=alumnos_ids_cursada).exclude(id__in=inscriptos_mesa).order_by('apellido')
    
    # Filtrar en python a los candidatos para remover a los que NO cumplen correlativas
    correlatividades = mesa.materia.correlativas_requeridas.all()
    alumnos_disponibles = []
    
    for alum in alumnos_candidatos:
        cumple_todas = True
        for corr in correlatividades:
            req_mat = corr.requisito
            tipo = corr.tipo
            
            tiene_eq = alum.equivalencias.filter(materia=req_mat).exists()
            tiene_prom = alum.inscripciones.filter(comision__materia=req_mat, estado='PROM').exists()
            tiene_final = alum.mesas_inscriptas.filter(mesa__materia=req_mat, estado='APR').exists()
            cumple_aprobado = tiene_eq or tiene_prom or tiene_final
            
            if tipo == 'APR' and not cumple_aprobado:
                cumple_todas = False
                break
                
            if tipo == 'CUR':
                tiene_cursada = alum.inscripciones.filter(comision__materia=req_mat, estado__in=['REG', 'PROM'], comision__cerrada=True).exists()
                if not (cumple_aprobado or tiene_cursada):
                    cumple_todas = False
                    break
                    
        if cumple_todas:
            alumnos_disponibles.append(alum)
    
    if request.method == 'POST':
        alumno_id = request.POST.get('alumno')
        if alumno_id:
            alumno = get_object_or_404(Alumno, id=alumno_id)
            override_admin = request.POST.get('override_admin') == 'on' or request.POST.get('force') == 'true'
            
            if alumno.estado_alumno in ['INA', 'EGR', 'COND_PAG', 'COND_DOC']:
                messages.warning(request, f"ATENCIÓN: El estado del alumno es '{alumno.get_estado_alumno_display()}'.")
                
            errores_validacion = []
            
            # 1. Validación de Cursada Regular
            inscripcion_cursada = Inscripcion.objects.filter(
                alumno=alumno, 
                comision__materia=mesa.materia,
                estado__in=['REG', 'PROM']
            ).first()
            
            if not inscripcion_cursada:
                errores_validacion.append("No tiene la cursada Regularizada de esta materia.")
            else:
                # 2. Validación de Vencimientos (Si tiene cursada)
                # Intentos
                intentos = InscripcionMesa.objects.filter(alumno=alumno, mesa__materia=mesa.materia, estado='REP').count()
                if intentos >= 3:
                    errores_validacion.append("Ha agotado los 3 intentos para rendir este final.")
                    
                # Tiempo (3 años)
                fecha_fin_cursada = inscripcion_cursada.comision.fecha_fin or inscripcion_cursada.fecha_inscripcion
                try:
                    fecha_vencimiento = fecha_fin_cursada.replace(year=fecha_fin_cursada.year + 3)
                except ValueError:
                    fecha_vencimiento = fecha_fin_cursada + timedelta(days=365*3)
                    
                if date.today() > fecha_vencimiento:
                    errores_validacion.append("Se han vencido los 3 años de regularidad para rendir el final.")
                    
            # 3. Validación de Correlativas
            correlatividades = mesa.materia.correlativas_requeridas.all()
            for corr in correlatividades:
                req_mat = corr.requisito
                tipo = corr.tipo
                
                tiene_eq = alumno.equivalencias.filter(materia=req_mat).exists()
                tiene_prom = alumno.inscripciones.filter(comision__materia=req_mat, estado='PROM').exists()
                tiene_final = alumno.mesas_inscriptas.filter(mesa__materia=req_mat, estado='APR').exists()
                
                cumple_aprobado = tiene_eq or tiene_prom or tiene_final
                
                if tipo == 'APR' and not cumple_aprobado:
                    errores_validacion.append(f"Falta FINAL APROBADO de correlativa: {req_mat.nombre}.")
                elif tipo == 'CUR' and not cumple_aprobado:
                    tiene_reg = alumno.inscripciones.filter(comision__materia=req_mat, estado='REG').exists()
                    if not tiene_reg:
                        errores_validacion.append(f"Falta CURSADA REGULAR de correlativa: {req_mat.nombre}.")

            # Ejecutar decisión
            if errores_validacion and not override_admin:
                for error in errores_validacion:
                    messages.error(request, f"{alumno.apellido}: {error}", extra_tags=f"force_mesa,{mesa.id},{alumno.id}")
            else:
                InscripcionMesa.objects.create(alumno=alumno, mesa=mesa)
                if override_admin and errores_validacion:
                    messages.warning(request, f'Alumno inscripto bajo excepción administrativa ignorando bloqueos.')
                else:
                    messages.success(request, f'Alumno {alumno.apellido} inscripto correctamente a la mesa de examen.')
                    
            return redirect('detalle_mesa', mesa_id=mesa.id)
            
    return render(request, 'gestion/inscribir_mesa.html', {
        'mesa': mesa,
        'alumnos': alumnos_disponibles
    })

@login_required
def cargar_notas_mesa(request, mesa_id):
    from .models import MesaExamen, InscripcionMesa
    mesa = get_object_or_404(MesaExamen, id=mesa_id)
    
    is_authorized = False
    if request.user.is_staff or request.user.is_superuser:
        is_authorized = True
    elif hasattr(request.user, 'perfil_docente'):
        docente = request.user.perfil_docente
        if mesa.presidente_mesa == docente or mesa.vocal_1 == docente or mesa.vocal_2 == docente:
            is_authorized = True
            
    if not is_authorized:
        messages.error(request, 'No tienes permiso para cargar notas en esta mesa de examen.')
        return redirect('dashboard')
    
    if mesa.cerrada:
        messages.error(request, 'La mesa está cerrada, ya no se pueden modificar actas ni notas.')
        return redirect('detalle_mesa', mesa_id=mesa.id)
        
    inscriptos = mesa.inscriptos.all().select_related('alumno').order_by('alumno__apellido')
    
    if request.method == 'POST':
        for insc in inscriptos:
            nota_str = request.POST.get(f'nota_{insc.id}')
            
            if not nota_str or nota_str.strip() == '':
                # Sin nota = Ausente
                insc.nota_final = None
                insc.estado = 'AUS'
            else:
                try:
                    nota = float(nota_str)
                    insc.nota_final = nota
                    if nota >= 4:
                        insc.estado = 'APR'
                    else:
                        insc.estado = 'REP'
                except ValueError:
                    continue # ignorar notas invalidas
                
            insc.save()
            
        messages.success(request, 'Notas de la mesa guardadas correctamente. Los estados se calcularon automáticamente.')
        return redirect('detalle_mesa', mesa_id=mesa.id)
        
    return render(request, 'gestion/cargar_notas_mesa.html', {'mesa': mesa, 'inscriptos': inscriptos})

@login_required
def cerrar_mesa(request, mesa_id):
    from .models import MesaExamen
    mesa = get_object_or_404(MesaExamen, id=mesa_id)
    
    # Verificar que no haya inscriptos PENDIENTES
    inscriptos_pendientes = mesa.inscriptos.filter(estado='PEND').count()
    
    if request.method == 'POST':
        if inscriptos_pendientes > 0:
            messages.error(request, f'No se puede cerrar la mesa. Hay {inscriptos_pendientes} alumno(s) sin calificar o sin ausente asignado.')
            return redirect('cerrar_mesa', mesa_id=mesa.id)
            
        libro = request.POST.get('libro')
        folio = request.POST.get('folio')
        mesa.libro = libro
        mesa.folio = folio
        mesa.cerrada = True
        mesa.save()
        messages.success(request, 'Mesa cerrada definitivamente y asignada a Libro/Folio.')
        return redirect('detalle_mesa', mesa_id=mesa.id)
        
    return render(request, 'gestion/cerrar_mesa.html', {
        'mesa': mesa,
        'inscriptos_pendientes': inscriptos_pendientes
    })

@login_required
def acta_examen(request, mesa_id):
    from .models import MesaExamen
    mesa = get_object_or_404(MesaExamen, id=mesa_id)
    inscriptos = mesa.inscriptos.all().select_related('alumno').order_by('alumno__apellido')
    
    # Función para convertir número a letra (básica para el acta)
    def nota_a_letras(nota_num):
        if nota_num is None: return "-"
        nota_entera = int(nota_num)
        letras = {
            1: 'Uno', 2: 'Dos', 3: 'Tres', 4: 'Cuatro', 5: 'Cinco',
            6: 'Seis', 7: 'Siete', 8: 'Ocho', 9: 'Nueve', 10: 'Diez'
        }
        return letras.get(nota_entera, str(nota_entera))
        
    datos_acta = []
    for insc in inscriptos:
        datos_acta.append({
            'alumno': insc.alumno,
            'nota_num': insc.nota_final if insc.estado in ['APR', 'REP'] else 'Ausente',
            'nota_letra': nota_a_letras(insc.nota_final) if insc.estado in ['APR', 'REP'] else '-',
            'estado': insc.get_estado_display()
        })
        
    return render(request, 'gestion/acta_examen.html', {
        'mesa': mesa,
        'datos_acta': datos_acta,
        'fecha_actual': date.today()
    })

# ==========================================
# HISTORIAL Y EQUIVALENCIAS (ANALÍTICO)
# ==========================================

@login_required
def alta_equivalencia(request, alumno_id):
    from .models import Alumno, Equivalencia, Materia
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if not alumno.plan:
        messages.error(request, "El alumno no tiene un plan de estudio asignado. Asígnele uno primero.")
        return redirect('legajo_alumno', alumno_id=alumno.id)
        
    materias_plan = alumno.plan.materias.all().order_by('año_dictado', 'nombre')
    
    # Excluir materias que ya tienen equivalencia
    equiv_existentes = Equivalencia.objects.filter(alumno=alumno).values_list('materia_id', flat=True)
    materias_disponibles = materias_plan.exclude(id__in=equiv_existentes)
    
    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        resolucion = request.POST.get('resolucion')
        institucion = request.POST.get('institucion')
        fecha = request.POST.get('fecha', date.today())
        nota = request.POST.get('nota')
        
        try:
            materia = get_object_or_404(Materia, id=materia_id)
            Equivalencia.objects.create(
                alumno=alumno,
                materia=materia,
                resolucion=resolucion,
                institucion_origen=institucion,
                fecha_otorgamiento=fecha,
                nota=nota if nota else None
            )
            messages.success(request, f'Equivalencia otorgada en {materia.nombre}.')
            return redirect('legajo_alumno', alumno_id=alumno.id)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            
    return render(request, 'gestion/alta_equivalencia.html', {
        'alumno': alumno,
        'materias': materias_disponibles
    })

@login_required
def analitico_alumno(request, alumno_id):
    if hasattr(request.user, 'perfil_alumno'):
        from django.contrib import messages
        messages.error(request, 'No tienes permiso para imprimir analíticos parciales oficiales. Por favor solicítalo en secretaría.')
        return redirect('dashboard')
        
    from .models import Alumno, Equivalencia, Inscripcion, InscripcionMesa
    alumno = get_object_or_404(Alumno, id=alumno_id)
    
    if not alumno.plan:
        messages.error(request, "El alumno no tiene plan de estudio para generar un analítico.")
        return redirect('legajo_alumno', alumno_id=alumno.id)
        
    # Recopilar todo el plan
    materias_plan = alumno.plan.materias.all().order_by('año_dictado', 'nombre')
    
    # Traer todos los registros aprobatorios del alumno
    equivalencias = Equivalencia.objects.filter(alumno=alumno)
    finales_aprobados = InscripcionMesa.objects.filter(alumno=alumno, estado='APR').select_related('mesa')
    cursadas_promocionadas = Inscripcion.objects.filter(alumno=alumno, estado='PROM').select_related('comision')
    
    # Crear diccionarios para búsqueda rápida por materia_id
    dict_equiv = {eq.materia_id: eq for eq in equivalencias}
    dict_finales = {fin.mesa.materia_id: fin for fin in finales_aprobados}
    dict_promociones = {cur.comision.materia_id: cur for cur in cursadas_promocionadas}
    
    # Construir las filas del analítico
    filas_analitico = []
    
    for materia in materias_plan:
        # Prioridad 1: Equivalencia
        if materia.id in dict_equiv:
            eq = dict_equiv[materia.id]
            filas_analitico.append({
                'materia': materia,
                'condicion': 'Equivalencia',
                'nota': eq.nota if eq.nota else '-',
                'fecha': eq.fecha_otorgamiento.strftime('%d/%m/%Y'),
                'libro_folio': f'Res: {eq.resolucion}'
            })
        # Prioridad 2: Final Aprobado
        elif materia.id in dict_finales:
            fin = dict_finales[materia.id]
            filas_analitico.append({
                'materia': materia,
                'condicion': 'Examen Final',
                'nota': fin.nota_final,
                'fecha': fin.mesa.fecha_hora.strftime('%d/%m/%Y'),
                'libro_folio': f'L:{fin.mesa.libro or "-"} F:{fin.mesa.folio or "-"}'
            })
        # Prioridad 3: Promoción
        elif materia.id in dict_promociones:
            cur = dict_promociones[materia.id]
            filas_analitico.append({
                'materia': materia,
                'condicion': 'Promoción Directa',
                'nota': 'PROM',
                'fecha': cur.comision.fecha_fin.strftime('%d/%m/%Y') if cur.comision.fecha_fin else '-',
                'libro_folio': '-'
            })
        # Prioridad 4: Pendiente
        else:
            filas_analitico.append({
                'materia': materia,
                'condicion': 'Pendiente',
                'nota': '',
                'fecha': '',
                'libro_folio': ''
            })
            
    return render(request, 'gestion/analitico_alumno.html', {
        'alumno': alumno,
        'plan': alumno.plan,
        'filas': filas_analitico,
        'fecha_actual': date.today()
    })

# ==========================================
# 8. COMUNICACIONES Y NOTIFICACIONES
# ==========================================

@login_required
def redactar_comunicado(request):
    from .models import Comunicado, PlanDeEstudio, Comision, Docente
    from .services import enviar_comunicado

    es_admin = request.user.is_superuser or request.user.is_staff
    docente = None
    if not es_admin:
        try:
            docente = request.user.perfil_docente
        except:
            messages.error(request, 'No tienes permisos para enviar comunicados.')
            return redirect('dashboard')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        mensaje = request.POST.get('mensaje')
        tipo_destinatario = request.POST.get('tipo_destinatario')
        plan_id = request.POST.get('plan_estudio')
        comision_id = request.POST.get('comision')

        # Validación estricta para Docentes
        if not es_admin:
            tipo_destinatario = 'COMISION'
            if not comision_id:
                messages.error(request, 'Debes seleccionar una comisión.')
                return redirect('redactar_comunicado')
            comision = Comision.objects.filter(Q(docente=docente) | Q(docente_auxiliar=docente), id=comision_id, cerrada=False).first()
            if not comision:
                messages.error(request, 'Comisión inválida o cerrada.')
                return redirect('redactar_comunicado')
            plan_obj = None
        else:
            plan_obj = PlanDeEstudio.objects.get(id=plan_id) if plan_id else None
            comision = Comision.objects.get(id=comision_id) if comision_id else None

        comunicado = Comunicado.objects.create(
            titulo=titulo,
            mensaje=mensaje,
            autor=request.user,
            tipo_destinatario=tipo_destinatario,
            plan_estudio=plan_obj,
            comision=comision
        )
        
        enviar_comunicado(comunicado)
        messages.success(request, '¡Comunicado enviado con éxito a todos los destinatarios!')
        return redirect('dashboard')

    planes = PlanDeEstudio.objects.all() if es_admin else []
    comisiones = Comision.objects.filter(cerrada=False) if es_admin else Comision.objects.filter(Q(docente=docente) | Q(docente_auxiliar=docente), cerrada=False)

    return render(request, 'gestion/comunicaciones/redactar.html', {
        'es_admin': es_admin,
        'planes': planes,
        'comisiones': comisiones,
        'opciones_destinatario': Comunicado.DESTINATARIOS_CHOICES
    })

@login_required
def mis_notificaciones(request):
    from .models import Notificacion
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-comunicado__fecha_creacion')
    return render(request, 'gestion/comunicaciones/inbox.html', {
        'notificaciones': notificaciones
    })

@login_required
def leer_notificacion(request, notificacion_id):
    from .models import Notificacion
    from django.utils.timezone import now
    
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    if not notificacion.leida:
        notificacion.leida = True
        notificacion.fecha_lectura = now()
        notificacion.save()
        
    return render(request, 'gestion/comunicaciones/leer_notificacion.html', {
        'notificacion': notificacion
    })

@login_required
def resetear_password_alumno(request, alumno_id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('dashboard')
        
    alumno = get_object_or_404(Alumno, id=alumno_id)
    if alumno.usuario:
        alumno.usuario.set_password(alumno.dni)
        alumno.usuario.save()
        messages.success(request, f'Se ha reseteado la contraseña del alumno {alumno.nombre} {alumno.apellido} a su DNI ({alumno.dni}).')
    else:
        messages.error(request, 'El alumno no tiene un usuario asociado.')
        
    return redirect('legajo_alumno', alumno_id=alumno.id)

@login_required
def perfil_alumno(request):
    if not hasattr(request.user, 'perfil_alumno'):
        messages.error(request, 'No tienes un perfil de alumno asociado.')
        return redirect('dashboard')
        
    alumno = request.user.perfil_alumno
    
    if request.method == 'POST':
        # Cambio de contraseña
        nueva_clave = request.POST.get('nueva_clave')
        confirmar_clave = request.POST.get('confirmar_clave')
        
        if nueva_clave and nueva_clave == confirmar_clave:
            request.user.set_password(nueva_clave)
            request.user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña actualizada correctamente.')
            
        # Actualización de datos
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        direccion = request.POST.get('direccion')
        
        if email: 
            request.user.email = email
            request.user.save()
            alumno.email = email
        if celular: alumno.celular = celular
        if direccion: alumno.direccion = direccion
        alumno.save()
        
        messages.success(request, 'Datos de contacto actualizados.')
        return redirect('perfil_alumno')
        
    return render(request, 'gestion/alumnos/perfil_alumno.html', {'alumno': alumno})

@login_required
def libro_matriz_alumno(request):
    if not hasattr(request.user, 'perfil_alumno'):
        return redirect('dashboard')
    
    from .models import Alumno, Equivalencia, Inscripcion, InscripcionMesa
    from datetime import date
    alumno = request.user.perfil_alumno
    
    if not alumno.plan:
        from django.contrib import messages
        messages.error(request, "No tienes plan de estudio asignado.")
        return redirect('dashboard')
        
    # Recopilar todo el plan
    materias_plan = alumno.plan.materias.all().order_by('año_dictado', 'nombre')
    
    # Traer todos los registros aprobatorios
    equivalencias = Equivalencia.objects.filter(alumno=alumno)
    finales_aprobados = InscripcionMesa.objects.filter(alumno=alumno, estado='APR').select_related('mesa')
    cursadas_promocionadas = Inscripcion.objects.filter(alumno=alumno, estado='PROM').select_related('comision')
    
    dict_equiv = {eq.materia_id: eq for eq in equivalencias}
    dict_finales = {fin.mesa.materia_id: fin for fin in finales_aprobados}
    dict_promociones = {cur.comision.materia_id: cur for cur in cursadas_promocionadas}
    
    filas_analitico = []
    
    for materia in materias_plan:
        if materia.id in dict_equiv:
            eq = dict_equiv[materia.id]
            filas_analitico.append({
                'materia': materia, 'condicion': 'Equivalencia', 'nota': eq.nota if eq.nota else '-',
                'fecha': eq.fecha_otorgamiento.strftime('%d/%m/%Y'), 'libro_folio': f'Res: {eq.resolucion}'
            })
        elif materia.id in dict_finales:
            fin = dict_finales[materia.id]
            filas_analitico.append({
                'materia': materia, 'condicion': 'Examen Final', 'nota': fin.nota_final,
                'fecha': fin.mesa.fecha_hora.strftime('%d/%m/%Y'), 'libro_folio': f'L:{fin.mesa.libro or "-"} F:{fin.mesa.folio or "-"}'
            })
        elif materia.id in dict_promociones:
            cur = dict_promociones[materia.id]
            filas_analitico.append({
                'materia': materia, 'condicion': 'Promoción Directa', 'nota': 'PROM',
                'fecha': cur.comision.fecha_fin.strftime('%d/%m/%Y') if cur.comision.fecha_fin else '-', 'libro_folio': 'S/Libro'
            })
        else:
            filas_analitico.append({
                'materia': materia, 'condicion': 'Pendiente', 'nota': '-', 'fecha': '-', 'libro_folio': '-'
            })
            
    return render(request, 'gestion/alumnos/libro_matriz.html', {
        'alumno': alumno, 'plan': alumno.plan, 'filas': filas_analitico, 'fecha_actual': date.today()
    })

@login_required
def alumno_inscripcion_cursada(request):
    if not hasattr(request.user, 'perfil_alumno'):
        messages.error(request, 'Acceso denegado. Esta sección es solo para alumnos.')
        return redirect('dashboard')
        
    alumno = request.user.perfil_alumno
    if not alumno.plan:
        messages.error(request, 'No tienes un plan de estudios asignado.')
        return redirect('dashboard')
        
    # Obtener comisiones abiertas del plan del alumno
    comisiones_abiertas = Comision.objects.filter(
        materia__plan=alumno.plan, 
        inscripciones_abiertas=True, 
        cerrada=False
    ).select_related('materia', 'docente', 'docente_auxiliar').order_by('materia__año_dictado', 'materia__nombre')
    
    # Procesar petición POST (Inscripción)
    if request.method == 'POST':
        action = request.POST.get('action')
        comision_id = request.POST.get('comision_id')
        
        try:
            comision = Comision.objects.get(id=comision_id, inscripciones_abiertas=True, cerrada=False)
            
            if action == 'inscribir':
                # Validar que no esté inscripto a otra comisión de la misma materia en el mismo ciclo
                ya_inscripto = Inscripcion.objects.filter(
                    alumno=alumno,
                    comision__materia=comision.materia,
                    comision__ciclo_lectivo=comision.ciclo_lectivo
                ).exists()
                
                if ya_inscripto:
                    messages.error(request, f'Ya estás inscripto en una comisión de {comision.materia.nombre} este año.')
                else:
                    # Chequeo rápido de correlativas (si se implementara acá a futuro). 
                    # El template ya desactiva el botón, pero hacemos una validación básica en backend.
                    # Se requiere iterar Correlatividad
                    from .models import Correlatividad, InscripcionMesa, Equivalencia
                    correlativas = Correlatividad.objects.filter(materia=comision.materia)
                    cumple_todas = True
                    motivo_rechazo = ""
                    
                    for corr in correlativas:
                        req_materia = corr.requisito
                        if corr.tipo == 'CUR':
                            # Necesita Regular, Aprobada o Promocionada
                            tiene_cursada = Inscripcion.objects.filter(
                                alumno=alumno, comision__materia=req_materia, estado__in=['REG', 'APR', 'PROM']
                            ).exists()
                            tiene_equiv = Equivalencia.objects.filter(alumno=alumno, materia=req_materia).exists()
                            if not (tiene_cursada or tiene_equiv):
                                cumple_todas = False
                                motivo_rechazo = f"Falta cursada de {req_materia.nombre}."
                                break
                        elif corr.tipo == 'APR':
                            # Necesita Promocionada, Final Aprobado o Equivalencia
                            tiene_prom = Inscripcion.objects.filter(
                                alumno=alumno, comision__materia=req_materia, estado='PROM'
                            ).exists()
                            tiene_final = InscripcionMesa.objects.filter(
                                alumno=alumno, mesa__materia=req_materia, estado='APR'
                            ).exists()
                            tiene_equiv = Equivalencia.objects.filter(alumno=alumno, materia=req_materia).exists()
                            if not (tiene_prom or tiene_final or tiene_equiv):
                                cumple_todas = False
                                motivo_rechazo = f"Falta final de {req_materia.nombre}."
                                break
                                
                    if cumple_todas:
                        Inscripcion.objects.create(alumno=alumno, comision=comision, estado='REG')
                        messages.success(request, f'Te inscribiste correctamente en {comision.materia.nombre}.')
                    else:
                        messages.error(request, f'No cumples con las correlativas: {motivo_rechazo}')
                        
        except Comision.DoesNotExist:
            messages.error(request, 'La comisión no existe o ya cerró su inscripción.')
            
        return redirect('alumno_inscripcion_cursada')

    # Preparar datos para el template
    inscripciones_actuales = Inscripcion.objects.filter(alumno=alumno).values_list('comision_id', flat=True)
    
    from .models import Correlatividad, InscripcionMesa, Equivalencia
    
    # Agrupar comisiones por año y evaluar correlativas
    comisiones_por_año = {}
    for com in comisiones_abiertas:
        año = com.materia.año_dictado
        if año not in comisiones_por_año:
            comisiones_por_año[año] = []
            
        # Evaluar correlatividades para mostrar en UI
        correlativas = Correlatividad.objects.filter(materia=com.materia)
        cumple_correlativas = True
        motivo = ""
        
        for corr in correlativas:
            req_materia = corr.requisito
            if corr.tipo == 'CUR':
                tiene_cursada = Inscripcion.objects.filter(alumno=alumno, comision__materia=req_materia, estado__in=['REG', 'APR', 'PROM']).exists()
                tiene_equiv = Equivalencia.objects.filter(alumno=alumno, materia=req_materia).exists()
                if not (tiene_cursada or tiene_equiv):
                    cumple_correlativas = False
                    motivo = f"Requiere cursar {req_materia.nombre}"
                    break
            elif corr.tipo == 'APR':
                tiene_prom = Inscripcion.objects.filter(alumno=alumno, comision__materia=req_materia, estado='PROM').exists()
                tiene_final = InscripcionMesa.objects.filter(alumno=alumno, mesa__materia=req_materia, estado='APR').exists()
                tiene_equiv = Equivalencia.objects.filter(alumno=alumno, materia=req_materia).exists()
                if not (tiene_prom or tiene_final or tiene_equiv):
                    cumple_correlativas = False
                    motivo = f"Requiere aprobar final de {req_materia.nombre}"
                    break
                    
        ya_inscripto_a_otra_comision = Inscripcion.objects.filter(
            alumno=alumno, comision__materia=com.materia, comision__ciclo_lectivo=com.ciclo_lectivo
        ).exclude(comision_id=com.id).exists()
        
        comisiones_por_año[año].append({
            'comision': com,
            'esta_inscripto': com.id in inscripciones_actuales,
            'ya_inscripto_otra': ya_inscripto_a_otra_comision,
            'cumple_correlativas': cumple_correlativas,
            'motivo_correlativa': motivo
        })
        
    return render(request, 'gestion/alumnos/inscripcion_cursada.html', {
        'comisiones_por_año': dict(sorted(comisiones_por_año.items())),
        'alumno': alumno,
    })

@login_required
def alumno_inscripcion_finales(request):
    if not hasattr(request.user, 'perfil_alumno'):
        messages.error(request, 'Acceso denegado. Esta sección es solo para alumnos.')
        return redirect('dashboard')
        
    alumno = request.user.perfil_alumno
    if not alumno.plan:
        messages.error(request, 'No tienes un plan de estudios asignado.')
        return redirect('dashboard')
        
    # Obtener mesas abiertas del plan del alumno
    from .models import MesaExamen, InscripcionMesa, Correlatividad, Equivalencia, Inscripcion
    
    mesas_abiertas = MesaExamen.objects.filter(
        materia__plan=alumno.plan, 
        inscripciones_abiertas=True, 
        cerrada=False
    ).select_related('materia', 'presidente_mesa', 'vocal_1', 'vocal_2').order_by('turno', 'fecha_hora')
    
    # Procesar petición POST (Inscripción)
    if request.method == 'POST':
        action = request.POST.get('action')
        mesa_id = request.POST.get('mesa_id')
        
        try:
            mesa = MesaExamen.objects.get(id=mesa_id, inscripciones_abiertas=True, cerrada=False)
            
            if action == 'inscribir':
                # Validar inscripción única en este turno y materia
                ya_inscripto = InscripcionMesa.objects.filter(
                    alumno=alumno,
                    mesa__materia=mesa.materia,
                    mesa__turno=mesa.turno,
                    mesa__ciclo_lectivo=mesa.ciclo_lectivo
                ).exists()
                
                if ya_inscripto:
                    messages.error(request, f'Ya estás inscripto en un llamado de {mesa.materia.nombre} para este turno.')
                else:
                    # Validar Cursada Regular (debe haber finalizado la cursada)
                    tiene_cursada = Inscripcion.objects.filter(
                        alumno=alumno, comision__materia=mesa.materia, estado__in=['REG', 'APR'], comision__cerrada=True
                    ).exists()
                    tiene_equiv = Equivalencia.objects.filter(alumno=alumno, materia=mesa.materia).exists()
                    
                    if not (tiene_cursada or tiene_equiv):
                        messages.error(request, 'Debes tener la cursada regularizada o aprobada para rendir el final.')
                    else:
                        # Validar Correlativas de Final (APR)
                        correlativas = Correlatividad.objects.filter(materia=mesa.materia, tipo='APR')
                        cumple_todas = True
                        motivo_rechazo = ""
                        
                        for corr in correlativas:
                            req_materia = corr.requisito
                            tiene_prom = Inscripcion.objects.filter(alumno=alumno, comision__materia=req_materia, estado='PROM').exists()
                            tiene_final = InscripcionMesa.objects.filter(alumno=alumno, mesa__materia=req_materia, estado='APR').exists()
                            tiene_equiv_req = Equivalencia.objects.filter(alumno=alumno, materia=req_materia).exists()
                            
                            if not (tiene_prom or tiene_final or tiene_equiv_req):
                                cumple_todas = False
                                motivo_rechazo = f"Falta final de {req_materia.nombre}."
                                break
                                
                        if cumple_todas:
                            InscripcionMesa.objects.create(alumno=alumno, mesa=mesa, estado='PEND')
                            messages.success(request, f'Te inscribiste correctamente al final de {mesa.materia.nombre}.')
                        else:
                            messages.error(request, f'No cumples con las correlativas: {motivo_rechazo}')
                        
        except MesaExamen.DoesNotExist:
            messages.error(request, 'La mesa de examen no existe o ya cerró su inscripción.')
            
        return redirect('alumno_inscripcion_finales')

    # Preparar datos para el template
    inscripciones_actuales = InscripcionMesa.objects.filter(alumno=alumno).values_list('mesa_id', flat=True)
    
    # Agrupar mesas por Turno
    mesas_por_turno = {}
    for mesa in mesas_abiertas:
        turno = mesa.get_turno_display()
        if turno not in mesas_por_turno:
            mesas_por_turno[turno] = []
            
        # Evaluar Cursada
        tiene_cursada = Inscripcion.objects.filter(alumno=alumno, comision__materia=mesa.materia, estado__in=['REG', 'APR'], comision__cerrada=True).exists()
        tiene_equiv = Equivalencia.objects.filter(alumno=alumno, materia=mesa.materia).exists()
        
        cumple_requisitos = True
        motivo = ""
        
        if not (tiene_cursada or tiene_equiv):
            cumple_requisitos = False
            motivo = "Requiere cursada regular"
        else:
            # Evaluar Correlativas
            correlativas = Correlatividad.objects.filter(materia=mesa.materia, tipo='APR')
            for corr in correlativas:
                req_materia = corr.requisito
                tiene_prom = Inscripcion.objects.filter(alumno=alumno, comision__materia=req_materia, estado='PROM').exists()
                tiene_final = InscripcionMesa.objects.filter(alumno=alumno, mesa__materia=req_materia, estado='APR').exists()
                tiene_equiv_req = Equivalencia.objects.filter(alumno=alumno, materia=req_materia).exists()
                if not (tiene_prom or tiene_final or tiene_equiv_req):
                    cumple_requisitos = False
                    motivo = f"Requiere aprobar final de {req_materia.nombre}"
                    break
                    
        ya_inscripto_a_otra_mesa = InscripcionMesa.objects.filter(
            alumno=alumno, mesa__materia=mesa.materia, mesa__turno=mesa.turno, mesa__ciclo_lectivo=mesa.ciclo_lectivo
        ).exclude(mesa_id=mesa.id).exists()
        
        mesas_por_turno[turno].append({
            'mesa': mesa,
            'esta_inscripto': mesa.id in inscripciones_actuales,
            'ya_inscripto_otra': ya_inscripto_a_otra_mesa,
            'cumple_requisitos': cumple_requisitos,
            'motivo_bloqueo': motivo
        })
        
    return render(request, 'gestion/alumnos/inscripcion_finales.html', {
        'mesas_por_turno': mesas_por_turno,
        'alumno': alumno,
    })