import re

with open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_validar = '''def validar_preinscripto(request, alumno_id):
    if es_solo_tutor(request.user): return redirect('lista_preinscriptos')
    from django.contrib.auth.models import User
    from .forms import RevisarPreinscriptoForm
    alumno = get_object_or_404(Alumno, id=alumno_id, estado_alumno='ASP')
    
    if request.method == 'POST':
        form = RevisarPreinscriptoForm(request.POST, instance=alumno)
        if form.is_valid():
            alumno = form.save(commit=False)
            
            # Crear usuario de django
            if not alumno.usuario:
                if User.objects.filter(username=alumno.dni).exists():
                    messages.error(request, f"Ya existe un usuario con DNI {alumno.dni}. Revise si el DNI es correcto.")
                    return redirect('lista_preinscriptos')
                    
                user = User.objects.create_user(username=alumno.dni, password=alumno.dni)
                user.first_name = alumno.nombre
                user.last_name = alumno.apellido
                user.save()
                alumno.usuario = user
                
            alumno.estado_alumno = 'ACT'
            alumno.save()
            messages.success(request, f"Aspirante {alumno.apellido}, {alumno.nombre} validado y dado de alta exitosamente. (Usuario: DNI, Clave: DNI)")
            return redirect('lista_preinscriptos')
    else:
        form = RevisarPreinscriptoForm(instance=alumno)
        
    return render(request, 'gestion/revisar_preinscripto.html', {'form': form, 'alumno': alumno})'''

new_validar = '''def validar_preinscripto(request, alumno_id):
    if es_solo_tutor(request.user): return redirect('lista_preinscriptos')
    from django.contrib.auth.models import User
    from .forms import RevisarPreinscriptoForm
    # Permitir ASP o ESP_CORREO para poder editarlo después
    alumno = get_object_or_404(Alumno, id=alumno_id, estado_alumno__in=['ASP', 'ESP_CORREO'])
    
    if request.method == 'POST':
        form = RevisarPreinscriptoForm(request.POST, instance=alumno)
        if form.is_valid():
            alumno = form.save(commit=False)
            
            if not alumno.correo_institucional:
                # Instancia 2: Aprobó papeles pero no tiene correo
                alumno.estado_alumno = 'ESP_CORREO'
                alumno.save()
                messages.warning(request, f"Aspirante {alumno.apellido}, {alumno.nombre} validado. Pasó a EN ESPERA DE CORREO INSTITUCIONAL.")
                return redirect('lista_preinscriptos')
            else:
                # Instancia 3: Tiene correo institucional, creamos usuario y activamos
                if not alumno.usuario:
                    username_correo = alumno.correo_institucional
                    if User.objects.filter(username=username_correo).exists():
                        messages.error(request, f"Ya existe un usuario con el correo {username_correo}.")
                        return redirect('lista_preinscriptos')
                        
                    user = User.objects.create_user(username=username_correo, password=alumno.dni)
                    user.first_name = alumno.nombre
                    user.last_name = alumno.apellido
                    user.email = alumno.correo_institucional
                    user.save()
                    alumno.usuario = user
                    
                alumno.estado_alumno = 'ACT'
                alumno.save()
                messages.success(request, f"Aspirante {alumno.apellido}, {alumno.nombre} validado y ACTIVO. (Usuario: {alumno.correo_institucional}, Clave: {alumno.dni})")
                return redirect('lista_preinscriptos')
    else:
        form = RevisarPreinscriptoForm(instance=alumno)
        
    return render(request, 'gestion/revisar_preinscripto.html', {'form': form, 'alumno': alumno})'''

content = content.replace(old_validar, new_validar)

with open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("validar_preinscripto updated successfully")
