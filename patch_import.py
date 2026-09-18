import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('from django.contrib.auth.decorators import login_required', 'from django.contrib.auth.decorators import login_required, user_passes_test')

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
