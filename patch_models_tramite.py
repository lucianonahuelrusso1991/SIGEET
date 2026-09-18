import codecs

with codecs.open('gestion/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_model = '''
class SolicitudTramite(models.Model):
    TIPO_TRAMITE = [
        ('REGULAR', 'Constancia de Alumno Regular'),
        ('EXAMEN', 'Certificado de Examen'),
    ]
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de Autorización'),
        ('APROBADO', 'Autorizado / Disponible para descarga'),
        ('RECHAZADO', 'Rechazado'),
    ]

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='tramites_solicitados')
    tipo = models.CharField('Tipo de Trámite', max_length=15, choices=TIPO_TRAMITE)
    materia = models.ForeignKey('Materia', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_examen = models.DateField('Fecha del Examen', null=True, blank=True)
    estado = models.CharField('Estado', max_length=15, choices=ESTADOS, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    @property
    def esta_vigente(self):
        if self.estado != 'APROBADO' or not self.fecha_aprobacion:
            return False
        import datetime
        from django.utils import timezone
        
        dias_habiles = 0
        fecha_eval = self.fecha_aprobacion.date()
        while dias_habiles < 7:
            fecha_eval += datetime.timedelta(days=1)
            if fecha_eval.weekday() < 5:
                dias_habiles += 1
        
        return timezone.localtime(timezone.now()).date() <= fecha_eval

    def __str__(self):
        return f"Trámite {self.get_tipo_display()} - {self.alumno}"
'''

content += new_model

with codecs.open('gestion/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added SolicitudTramite to models.py")
