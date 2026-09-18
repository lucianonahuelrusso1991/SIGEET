import codecs
import re

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for cargar_notas (cursada)
pattern1 = r"(if nota_valor:\s*\n\s*)Nota\.objects\.create\(\s*\n\s*inscripcion=insc,\s*\n\s*instancia=instancia_nombre,\s*\n\s*calificacion=int\(nota_valor\)\s*\n\s*\)"
repl1 = r"\1nota_entera = int(nota_valor)\n                        if 1 <= nota_entera <= 10:\n                            Nota.objects.create(\n                                inscripcion=insc,\n                                instancia=instancia_nombre,\n                                calificacion=nota_entera\n                            )"

content = re.sub(pattern1, repl1, content)

# Pattern for cargar_notas_mesa
pattern2 = r"(if nota_valor:\s*\n\s*)insc\.estado = 'APR' if int\(nota_valor\) >= 4 else 'DES'\s*\n\s*insc\.nota = int\(nota_valor\)\s*\n\s*insc\.save\(\)"
repl2 = r"\1nota_entera = int(nota_valor)\n                    if 1 <= nota_entera <= 10:\n                        insc.estado = 'APR' if nota_entera >= 4 else 'DES'\n                        insc.nota = nota_entera\n                        insc.save()"

content = re.sub(pattern2, repl2, content)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
