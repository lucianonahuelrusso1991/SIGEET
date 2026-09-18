import re

with open('sistema_escolar/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
import_pattern = r'from gestion.views import \('
import_replacement = r'from gestion.views import (\n    solicitar_tramite_alumno, lista_tramites, autorizar_tramite,'
content = re.sub(import_pattern, import_replacement, content)

# Add paths
url_pattern = r"path\('eliminar-alumno/<int:alumno_id>/', eliminar_alumno, name='eliminar_alumno'\),"
url_replacement = r"path('eliminar-alumno/<int:alumno_id>/', eliminar_alumno, name='eliminar_alumno'),\n    path('tramites/', lista_tramites, name='lista_tramites'),\n    path('tramites/solicitar/', solicitar_tramite_alumno, name='solicitar_tramite_alumno'),\n    path('tramites/autorizar/<int:tramite_id>/', autorizar_tramite, name='autorizar_tramite'),"
content = re.sub(url_pattern, url_replacement, content)

with open('sistema_escolar/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("urls.py patched successfully")
