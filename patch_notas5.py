import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "valor_nota=nota_valor_int" in line and "Nota.objects.create(" in lines[i-3]:
        lines[i-4] = "                  if nota_valor:\n                      try:\n                          nota_valor_int = int(nota_valor)\n                          if not (1 <= nota_valor_int <= 10):\n                              messages.error(request, f'La nota de {insc.alumno.apellido} debe estar entre 1 y 10.')\n                              continue\n                      except ValueError:\n"
        
    if "insc.estado = 'APR' if int(nota_valor) >= 4 else 'DES'" in line:
        lines[i] = "                  nota_entera = int(nota_valor)\n                  if 1 <= nota_entera <= 10:\n                      insc.estado = 'APR' if nota_entera >= 4 else 'DES'\n                      insc.nota = nota_entera\n                      insc.save()\n"
        lines[i+1] = ""
        lines[i+2] = ""

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
