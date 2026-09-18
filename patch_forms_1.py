import codecs

with codecs.open('gestion/forms.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''def normalize_alumno_data(cleaned_data):
    # Only numbers for DNI
    if 'dni' in cleaned_data and cleaned_data['dni']:
        cleaned_data['dni'] = re.sub(r'\D', '', str(cleaned_data['dni']))'''

new_func = '''def normalize_alumno_data(cleaned_data):
    from django.core.exceptions import ValidationError
    # Only numbers for DNI
    if 'dni' in cleaned_data and cleaned_data['dni']:
        cleaned_dni = re.sub(r'\D', '', str(cleaned_data['dni']))
        if not cleaned_dni:
            raise ValidationError({'dni': 'El DNI debe contener números.'})
        cleaned_data['dni'] = cleaned_dni'''

content = content.replace(old_func, new_func)

with codecs.open('gestion/forms.py', 'w', encoding='utf-8') as f:
    f.write(content)
