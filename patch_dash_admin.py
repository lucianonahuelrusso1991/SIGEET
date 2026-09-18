import codecs

with codecs.open('gestion/templates/gestion/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_link = '''<a href="{% url 'lista_preinscriptos' %}" class="btn btn-outline-secondary w-100 fw-bold rounded-pill btn-sm">Revisar Preinscriptos</a>'''
new_link = '''<a href="{% url 'lista_preinscriptos' %}" class="btn btn-outline-secondary w-100 fw-bold rounded-pill btn-sm">Revisar Preinscriptos</a>
                    <a href="{% url 'lista_tramites' %}" class="btn btn-outline-info w-100 fw-bold rounded-pill btn-sm mt-2 text-dark">Trámites y Certificados</a>'''

content = content.replace(old_link, new_link)

with codecs.open('gestion/templates/gestion/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
