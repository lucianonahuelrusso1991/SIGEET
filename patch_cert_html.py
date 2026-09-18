import codecs

with codecs.open('gestion/templates/gestion/alumnos/certificado_examen.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Patch Materia / Asignatura
old_mat = '''            {% if ultima_mesa %}
                {{ ultima_mesa.mesa.materia.nombre }}
            {% else %}'''

new_mat = '''            {% if materia_cert %}
                {{ materia_cert.nombre }}
            {% elif ultima_mesa %}
                {{ ultima_mesa.mesa.materia.nombre }}
            {% else %}'''

content = content.replace(old_mat, new_mat)

# The date might be hardcoded as "se presentó a rendir examen el día ________"
# Let's try to find it.

print("Check the file manually for date replacement.")

with codecs.open('gestion/templates/gestion/alumnos/certificado_examen.html', 'w', encoding='utf-8') as f:
    f.write(content)
