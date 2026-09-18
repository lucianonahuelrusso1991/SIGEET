import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_try = '''                try:
                    nota_valor_int = int(nota_valor)
                except ValueError:'''

new_try = '''                try:
                    nota_valor_int = int(nota_valor)
                    if not (1 <= nota_valor_int <= 10):
                        messages.error(request, f"La nota de {insc.alumno.apellido} debe estar entre 1 y 10.")
                        continue
                except ValueError:'''

content = content.replace(old_try, new_try)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
