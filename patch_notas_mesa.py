import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_try = '''                try:
                    nota = float(nota_str)
                    insc.nota_final = nota'''

new_try = '''                try:
                    nota = float(nota_str)
                    if not (1 <= nota <= 10):
                        messages.error(request, f"La nota de {insc.alumno.apellido} debe estar entre 1 y 10.")
                        continue
                    insc.nota_final = nota'''

content = content.replace(old_try, new_try)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
