import codecs
import re

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the views to protect
views_to_protect = [
    'lista_alumnos', 'alta_alumno', 'editar_alumno',
    'lista_docentes', 'alta_docente', 'editar_docente',
    'lista_comisiones', 'apertura_masiva', 'alta_comision', 'eliminar_comision',
    'alta_evento_calendario',
    'lista_mesas', 'alta_mesa', 'eliminar_mesa',
    'alta_equivalencia', 'resetear_password_alumno'
]

for view in views_to_protect:
    pattern = rf"(@login_required\s*\n)(def {view}\()"
    replacement = r"\1@user_passes_test(lambda u: u.is_staff or u.is_superuser)\n\2"
    content = re.sub(pattern, replacement, content)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
