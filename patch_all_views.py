import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. preinscripcion_publica
old_pre = '''def preinscripcion_publica(request):
    if request.method == 'POST':
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.estado_alumno = 'ASP'
            alumno.save()
            from .models import InscripcionCarrera
            InscripcionCarrera.objects.create(alumno=alumno, plan=form.cleaned_data['plan'], estado='PREINSCRIPTO')
            return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})
        else:
            if 'dni' in form.errors and any('ya existe' in str(e).lower() or 'already exists' in str(e).lower() for e in form.errors['dni']):
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
                        return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})
    else:
        form = PreinscripcionForm()
    
    return render(request, 'gestion/preinscripcion.html', {'form': form})'''

new_pre = '''def preinscripcion_publica(request):
    if request.method == 'POST':
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            dni_ingresado = form.cleaned_data.get('dni')
            from .models import Alumno, InscripcionCarrera
            alumno_existente = Alumno.objects.filter(dni=dni_ingresado).first()
            
            if alumno_existente:
                InscripcionCarrera.objects.get_or_create(alumno=alumno_existente, plan=form.cleaned_data['plan'], defaults={'estado': 'PREINSCRIPTO'})
            else:
                alumno = form.save(commit=False)
                alumno.estado_alumno = 'ASP'
                alumno.save()
                InscripcionCarrera.objects.create(alumno=alumno, plan=form.cleaned_data['plan'], estado='PREINSCRIPTO')
            
            return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})
        else:
            if 'dni' in form.errors and any('ya existe' in str(e).lower() or 'already exists' in str(e).lower() for e in form.errors['dni']):
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
                        return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})
    else:
        form = PreinscripcionForm()
    
    return render(request, 'gestion/preinscripcion.html', {'form': form})'''

old_pre2 = '''def preinscripcion_publica(request):
    if request.method == 'POST':
        form = PreinscripcionForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.estado_alumno = 'ASP'
            alumno.save()
            from .models import InscripcionCarrera
            InscripcionCarrera.objects.create(alumno=alumno, plan=form.cleaned_data['plan'], estado='PREINSCRIPTO')
            return render(request, 'gestion/preinscripcion.html', {'form': form, 'exito': True})
    else:
        form = PreinscripcionForm()
    
    return render(request, 'gestion/preinscripcion.html', {'form': form})'''

if old_pre in content:
    content = content.replace(old_pre, new_pre)
elif old_pre2 in content:
    content = content.replace(old_pre2, new_pre)

# 2. notas bounds
# we do this by simply re-running the strict regex

import re
# Pattern for cargar_notas (cursada)
pattern1 = r"(if nota_valor:\s*\n\s*)try:\s*\n\s*nota_valor_int = int\(nota_valor\)\s*\n\s*except ValueError:"
repl1 = r"\1try:\n                      nota_valor_int = int(nota_valor)\n                      if not (1 <= nota_valor_int <= 10):\n                          messages.error(request, f'La nota de {insc.alumno.apellido} debe estar entre 1 y 10.')\n                          continue\n                  except ValueError:"
content = re.sub(pattern1, repl1, content)

# Pattern for cargar_notas_mesa
pattern2 = r"try:\s*\n\s*nota = float\(nota_str\)\s*\n\s*insc\.nota_final = nota"
repl2 = r"try:\n                    nota = float(nota_str)\n                    if not (1 <= nota <= 10):\n                        messages.error(request, f'La nota de {insc.alumno.apellido} debe estar entre 1 y 10.')\n                        continue\n                    insc.nota_final = nota"
content = re.sub(pattern2, repl2, content)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
