import codecs

with codecs.open('gestion/templates/gestion/alumnos/certificado_examen.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_date = '''<strong>{{ fecha_actual.day }} de {{ fecha_actual|date:"F" }} de {{ fecha_actual.year }}</strong> con el fin de rendir'''
new_date = '''<strong>{% if fecha_cert %}{{ fecha_cert }}{% else %}{{ fecha_actual.day }} de {{ fecha_actual|date:"F" }} de {{ fecha_actual.year }}{% endif %}</strong> con el fin de rendir'''

content = content.replace(old_date, new_date)

with codecs.open('gestion/templates/gestion/alumnos/certificado_examen.html', 'w', encoding='utf-8') as f:
    f.write(content)
