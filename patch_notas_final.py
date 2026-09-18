import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. cargar_notas
old_try_1 = '''                try:
                    nota_valor_int = int(nota_valor)
                except ValueError:
                    messages.error(request, f"La nota de {insc.alumno.apellido} debe ser un número entero.")
                    continue'''

new_try_1 = '''                try:
                    nota_valor_int = int(nota_valor)
                    if not (1 <= nota_valor_int <= 10):
                        messages.error(request, f"La nota de {insc.alumno.apellido} debe estar entre 1 y 10.")
                        continue
                except ValueError:
                    messages.error(request, f"La nota de {insc.alumno.apellido} debe ser un número entero.")
                    continue'''

content = content.replace(old_try_1.replace('número', 'nǧmero'), new_try_1.replace('número', 'nǧmero'))
content = content.replace(old_try_1, new_try_1)

# 2. cargar_notas_mesa
old_try_2 = '''                try:
                    nota = float(nota_str)
                    insc.nota_final = nota'''

new_try_2 = '''                try:
                    nota = float(nota_str)
                    if not (1 <= nota <= 10):
                        messages.error(request, f"La nota de {insc.alumno.apellido} debe estar entre 1 y 10.")
                        continue
                    insc.nota_final = nota'''

content = content.replace(old_try_2, new_try_2)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
