import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_pre = '''def preinscripcion_publica(request):
    if request.method == 'POST':
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.estado_alumno = 'ASP'
            alumno.save()
            from .models import InscripcionCarrera
            InscripcionCarrera.objects.create(alumno=alumno, plan=form.cleaned_data['plan'], estado='PREINSCRIPTO')
            return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})'''

new_pre = '''def preinscripcion_publica(request):
    if request.method == 'POST':
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            dni_ingresado = form.cleaned_data.get('dni')
            from .models import Alumno, InscripcionCarrera
            alumno_existente = Alumno.objects.filter(dni=dni_ingresado).first()
            
            if alumno_existente:
                # El alumno ya existe, le agregamos la carrera nueva
                InscripcionCarrera.objects.get_or_create(alumno=alumno_existente, plan=form.cleaned_data['plan'], defaults={'estado': 'PREINSCRIPTO'})
            else:
                alumno = form.save(commit=False)
                alumno.estado_alumno = 'ASP'
                alumno.save()
                InscripcionCarrera.objects.create(alumno=alumno, plan=form.cleaned_data['plan'], estado='PREINSCRIPTO')
            
            return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})
        else:
            # Si el form es inválido solo porque el DNI ya existe, forzamos el procesamiento
            if 'dni' in form.errors and any('ya existe' in str(e).lower() or 'already exists' in str(e).lower() for e in form.errors['dni']):
                # Recuperar los datos crudos y hacer el proceso manual para este DNI
                dni_ingresado = request.POST.get('dni')
                import re
                dni_limpio = re.sub(r'\D', '', str(dni_ingresado))
                from .models import Alumno, InscripcionCarrera, PlanDeEstudio
                alumno_existente = Alumno.objects.filter(dni=dni_limpio).first()
                if alumno_existente:
                    plan_id = request.POST.get('plan')
                    plan_obj = PlanDeEstudio.objects.filter(id=plan_id).first()
                    if plan_obj:
                        InscripcionCarrera.objects.get_or_create(alumno=alumno_existente, plan=plan_obj, defaults={'estado': 'PREINSCRIPTO'})
                        return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})'''

content = content.replace(old_pre, new_pre)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
