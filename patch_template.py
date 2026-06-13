import re

with open(r'd:\Escritorio\GESTION ESCOLAR\gestion\templates\gestion\editar_comision.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Title
content = content.replace("Nueva Comisión", "Editar Comisión")

# Materia select
content = content.replace('name="materia" class="form-select" required', 'name="materia" class="form-select" required disabled')
content = content.replace('value="{{ materia.id }}"', 'value="{{ materia.id }}" {% if materia.id == comision.materia.id %}selected{% endif %}')

# Docente select
content = content.replace('value="{{ docente.id }}"', 'value="{{ docente.id }}" {% if comision.docente and docente.id == comision.docente.id %}selected{% endif %}')

# Ciclo lectivo
content = content.replace('value="{{ proximo_año }}"', 'value="{{ comision.ciclo_lectivo }}"')

# Cuatrimestre
content = content.replace('value="1C"', 'value="1C" {% if comision.cuatrimestre == "1C" %}selected{% endif %}')
content = content.replace('value="2C"', 'value="2C" {% if comision.cuatrimestre == "2C" %}selected{% endif %}')
content = content.replace('value="AN"', 'value="AN" {% if comision.cuatrimestre == "AN" %}selected{% endif %}')

# Fechas
content = content.replace('name="fecha_inicio" class="form-control"', 'name="fecha_inicio" class="form-control" value="{{ comision.fecha_inicio|date:\'Y-m-d\' }}"')
content = content.replace('name="fecha_fin" class="form-control"', 'name="fecha_fin" class="form-control" value="{{ comision.fecha_fin|date:\'Y-m-d\' }}"')

# Tipo aprob
content = content.replace('value="PROM"', 'value="PROM" {% if comision.tipo_aprobacion == "PROM" %}selected{% endif %}')
content = content.replace('value="FIN" selected', 'value="FIN" {% if comision.tipo_aprobacion == "FIN" %}selected{% endif %}')

# Modalidad
content = content.replace('value="P" selected', 'value="P" {% if comision.modalidad == "P" %}selected{% endif %}')
content = content.replace('value="V"', 'value="V" {% if comision.modalidad == "V" %}selected{% endif %}')
content = content.replace('value="B"', 'value="B" {% if comision.modalidad == "B" %}selected{% endif %}')

# Inicio Bimodal (only value="P" left because previous replaced selected)
content = content.replace('value="P">', 'value="P" {% if comision.semana_inicio_bimodal == "P" %}selected{% endif %}>')

# Checkboxes
def cb_repl(match):
    val = match.group(1) # e.g. value="1_17:20_18:00"
    val_str = val.split('"')[1] # e.g. 1_17:20_18:00
    return f'{val} {{% if "{val_str}" in horarios_actuales %}}checked{{% endif %}}'

content = re.sub(r'(value="\d_\d\d:\d\d_\d\d:\d\d")', cb_repl, content)

# Back button
content = content.replace("{% url 'lista_comisiones' %}", "{% url 'detalle_comision' comision.id %}")
content = content.replace("⬅ Volver al Listado", "⬅ Volver a la Comisión")

# Add a hidden input for materia since it's disabled
content = content.replace('</form>', '<input type="hidden" name="materia" value="{{ comision.materia.id }}"></form>')

with open(r'd:\Escritorio\GESTION ESCOLAR\gestion\templates\gestion\editar_comision.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template patched.")
