import codecs

with codecs.open('gestion/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_model = '''    def __str__(self):
        return f"{self.alumno.apellido} - {self.get_estado_display()}"
        
class JustificativoAsistencia(models.Model):'''

new_model = '''    def __str__(self):
        return f"{self.alumno.apellido} - {self.get_estado_display()}"

    class Meta:
        unique_together = ['planilla', 'alumno']
        
class JustificativoAsistencia(models.Model):'''

content = content.replace(old_model, new_model)

with codecs.open('gestion/models.py', 'w', encoding='utf-8') as f:
    f.write(content)
