import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# For cargar_notas
old_cargar_notas = '''                    if nota_valor:
                        Nota.objects.create(
                            inscripcion=insc,
                            instancia=instancia_nombre,
                            calificacion=int(nota_valor)
                        )'''

new_cargar_notas = '''                    if nota_valor:
                        nota_entera = int(nota_valor)
                        if 1 <= nota_entera <= 10:
                            Nota.objects.create(
                                inscripcion=insc,
                                instancia=instancia_nombre,
                                calificacion=nota_entera
                            )'''

content = content.replace(old_cargar_notas, new_cargar_notas)

# For cargar_notas_mesa
old_cargar_notas_mesa = '''                if nota_valor:
                    insc.estado = 'APR' if int(nota_valor) >= 4 else 'DES'
                    insc.nota = int(nota_valor)
                    insc.save()'''

new_cargar_notas_mesa = '''                if nota_valor:
                    nota_entera = int(nota_valor)
                    if 1 <= nota_entera <= 10:
                        insc.estado = 'APR' if nota_entera >= 4 else 'DES'
                        insc.nota = nota_entera
                        insc.save()'''

content = content.replace(old_cargar_notas_mesa, new_cargar_notas_mesa)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
