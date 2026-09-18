import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "if nota_valor:" in line and "Nota.objects.create(" in lines[i+1]:
        lines[i] = "                    if nota_valor:\n                        nota_entera = int(nota_valor)\n                        if 1 <= nota_entera <= 10:\n"
        lines[i+4] = lines[i+4].replace("calificacion=int(nota_valor)", "calificacion=nota_entera")
        
    if "if nota_valor:" in line and "insc.estado = 'APR' if int(nota_valor) >= 4 else 'DES'" in lines[i+1]:
        lines[i] = "                if nota_valor:\n                    nota_entera = int(nota_valor)\n                    if 1 <= nota_entera <= 10:\n"
        lines[i+1] = "                        insc.estado = 'APR' if nota_entera >= 4 else 'DES'\n"
        lines[i+2] = "                        insc.nota = nota_entera\n"

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
