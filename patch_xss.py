import codecs

with codecs.open('gestion/templates/gestion/apertura_masiva.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_js = '''<script>
    const planesData = {{ planes_json|safe }};'''

new_js = '''{{ planes_json|json_script:"planes-data" }}
<script>
    const planesData = JSON.parse(document.getElementById('planes-data').textContent);'''

content = content.replace(old_js, new_js)

with codecs.open('gestion/templates/gestion/apertura_masiva.html', 'w', encoding='utf-8') as f:
    f.write(content)
