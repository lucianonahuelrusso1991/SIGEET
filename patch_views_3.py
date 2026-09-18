import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Cargar notas cursada
for i, line in enumerate(lines):
    if "Nota.objects.create(" in line and "calificacion=int(nota_valor)" in lines[i+3]:
        lines[i-1] = "                    if nota_valor:\n                        nota_entera = int(nota_valor)\n                        if 1 <= nota_entera <= 10:\n"
        lines[i+3] = lines[i+3].replace("calificacion=int(nota_valor)", "calificacion=nota_entera")
        break

# 2. Cargar notas mesa
for i, line in enumerate(lines):
    if "insc.estado = 'APR' if int(nota_valor) >= 4 else 'DES'" in line:
        lines[i] = "                    nota_entera = int(nota_valor)\n                    if 1 <= nota_entera <= 10:\n                        insc.estado = 'APR' if nota_entera >= 4 else 'DES'\n"
        lines[i+1] = "                        insc.nota = nota_entera\n"
        lines[i+2] = "                        insc.save()\n"

# 3. preinscripcion_publica
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "def preinscripcion_publica(request):" in line:
        start_idx = i
        break
for i in range(start_idx, len(lines)):
    if "return render(request, 'gestion/preinscripcion.html', {'form': form})" in line:
        end_idx = i
        break

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
    
    return render(request, 'gestion/preinscripcion.html', {'form': form})
'''

lines[start_idx:end_idx+1] = [new_pre]

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
