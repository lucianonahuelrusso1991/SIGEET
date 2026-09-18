import codecs

with codecs.open('gestion/templates/gestion/revisar_preinscripto.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

content = content.replace('Acadǟmico', 'Académico')
content = content.replace('Documentacin', 'Documentación')
content = content.replace('Fsicamente', 'Físicamente')
content = content.replace('Ttulo', 'Título')
content = content.replace('an no tiene', 'aún no tiene')
content = content.replace('Tcnico', 'Técnico')
content = content.replace('dej el', 'dejá el')
content = content.replace('guard los', 'guardá los')
content = content.replace('quedar', 'quedará')
content = content.replace('tens', 'tenés')
content = content.replace('inscripcin', 'inscripción')

with codecs.open('gestion/templates/gestion/revisar_preinscripto.html', 'w', encoding='utf-8') as f:
    f.write(content)
