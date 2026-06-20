from datetime import date
from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. USUARIOS Y PERFILES
# ==========================================

class Docente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_docente', null=True, blank=True)
    dni = models.CharField('DNI', max_length=15, unique=True)
    nombre = models.CharField('Nombre/s', max_length=100)
    apellido = models.CharField('Apellido/s', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    
    # Contacto y Demográficos
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono Fijo")
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular")
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección")
    email = models.EmailField(blank=True, null=True)
    
    nacionalidad = models.CharField(max_length=100, default='Argentina')
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    comuna_zona = models.CharField(max_length=100, blank=True, null=True)
    
    PROVINCIAS = [
        ('Buenos Aires', 'Buenos Aires'), ('CABA', 'Ciudad Autónoma de Buenos Aires'), 
        ('Catamarca', 'Catamarca'), ('Chaco', 'Chaco'), ('Chubut', 'Chubut'), 
        ('Córdoba', 'Córdoba'), ('Corrientes', 'Corrientes'), ('Entre Ríos', 'Entre Ríos'), 
        ('Formosa', 'Formosa'), ('Jujuy', 'Jujuy'), ('La Pampa', 'La Pampa'), 
        ('La Rioja', 'La Rioja'), ('Mendoza', 'Mendoza'), ('Misiones', 'Misiones'), 
        ('Neuquén', 'Neuquén'), ('Río Negro', 'Río Negro'), ('Salta', 'Salta'), 
        ('San Juan', 'San Juan'), ('San Luis', 'San Luis'), ('Santa Cruz', 'Santa Cruz'), 
        ('Santa Fe', 'Santa Fe'), ('Santiago del Estero', 'Santiago del Estero'), 
        ('Tierra del Fuego', 'Tierra del Fuego'), ('Tucumán', 'Tucumán')
    ]
    provincia = models.CharField(max_length=100, choices=PROVINCIAS, blank=True, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)
    
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Alumno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_alumno', null=True, blank=True)
    dni = models.CharField('DNI', max_length=15, unique=True) 
    nombre = models.CharField('Nombre/s', max_length=100)
    apellido = models.CharField('Apellido/s', max_length=100)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    
    # Contacto y Demográficos
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono Fijo")
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular")
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección")
    email = models.EmailField(blank=True, null=True)
    
    nacionalidad = models.CharField(max_length=100, default='Argentina')
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    comuna_zona = models.CharField(max_length=100, blank=True, null=True)
    
    PROVINCIAS = [
        ('Buenos Aires', 'Buenos Aires'), ('CABA', 'Ciudad Autónoma de Buenos Aires'), 
        ('Catamarca', 'Catamarca'), ('Chaco', 'Chaco'), ('Chubut', 'Chubut'), 
        ('Córdoba', 'Córdoba'), ('Corrientes', 'Corrientes'), ('Entre Ríos', 'Entre Ríos'), 
        ('Formosa', 'Formosa'), ('Jujuy', 'Jujuy'), ('La Pampa', 'La Pampa'), 
        ('La Rioja', 'La Rioja'), ('Mendoza', 'Mendoza'), ('Misiones', 'Misiones'), 
        ('Neuquén', 'Neuquén'), ('Río Negro', 'Río Negro'), ('Salta', 'Salta'), 
        ('San Juan', 'San Juan'), ('San Luis', 'San Luis'), ('Santa Cruz', 'Santa Cruz'), 
        ('Santa Fe', 'Santa Fe'), ('Santiago del Estero', 'Santiago del Estero'), 
        ('Tierra del Fuego', 'Tierra del Fuego'), ('Tucumán', 'Tucumán')
    ]
    provincia = models.CharField(max_length=100, choices=PROVINCIAS, blank=True, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)
    
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=100, blank=True, null=True)
    
    # Documentación
    doc_dni = models.BooleanField(default=False, verbose_name="Fotocopia DNI")
    doc_vacunas = models.BooleanField(default=False, verbose_name="Certificado de Vacunas")
    doc_partida = models.BooleanField(default=False, verbose_name="Partida de Nacimiento")
    doc_primaria = models.BooleanField(default=False, verbose_name="Título Secundario") # Adaptado a terciario
    doc_pase = models.BooleanField(default=False, verbose_name="Pase de Escuela Anterior")

    # Plan de Estudio Asignado
    plan = models.ForeignKey('PlanDeEstudio', on_delete=models.SET_NULL, null=True, blank=True, related_name='alumnos', verbose_name="Plan de Estudios")

    ESTADOS_ALUMNO = [
        ('ACT', 'Activo'),
        ('INA', 'Inactivo / Abandonó'),
        ('EGR', 'Egresado'),
        ('COND_DOC', 'Condicionado (Documentación)'),
        ('COND_PAG', 'Condicionado (Falta de Pago)'),
    ]
    estado_alumno = models.CharField('Estado', max_length=10, choices=ESTADOS_ALUMNO, default='ACT')

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - DNI: {self.dni}"


# ==========================================
# 2. ESTRUCTURA ACADÉMICA (PLANES Y MATERIAS)
# ==========================================

class PlanDeEstudio(models.Model):
    nombre = models.CharField('Nombre del Plan', max_length=150)
    resolucion_ministerial = models.CharField('Resolución', max_length=50)

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    CUATRIMESTRES = [
        ('1C', '1er Cuatrimestre'),
        ('2C', '2do Cuatrimestre'),
        ('AN', 'Anual'),
    ]
    nombre = models.CharField(max_length=150)
    plan = models.ForeignKey(PlanDeEstudio, on_delete=models.CASCADE, related_name='materias')
    año_dictado = models.IntegerField(verbose_name="Año en que se dicta (1, 2, 3...)")
    cuatrimestre_dictado = models.CharField(max_length=2, choices=CUATRIMESTRES, default='1C')

    def __str__(self):
        return f"{self.nombre} ({self.año_dictado}º Año - {self.get_cuatrimestre_dictado_display()})"

class Correlatividad(models.Model):
    TIPO_REQUISITO = [
        ('CUR', 'Cursada Regular'),
        ('APR', 'Final Aprobado'),
    ]
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='correlativas_requeridas')
    requisito = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='es_requisito_de')
    tipo = models.CharField('Tipo de Requisito', max_length=3, choices=TIPO_REQUISITO)

    def __str__(self):
        return f"Para {self.materia.nombre} se requiere {self.get_tipo_display()} de {self.requisito.nombre}"


# ==========================================
# 3. COMISIONES E INSCRIPCIONES (NUEVO NÚCLEO)
# ==========================================

class Comision(models.Model):
    CUATRIMESTRES = [
        ('1C', '1er Cuatrimestre'),
        ('2C', '2do Cuatrimestre'),
        ('AN', 'Anual'),
    ]
    TIPO_APROBACION = [
        ('PROM', 'Promocionable'),
        ('FIN', 'Final Obligatorio'),
    ]
    MODALIDAD = [
        ('P', 'Presencial'),
        ('V', 'Virtual'),
        ('B', 'Bimodal (1 sem presencial / 1 sem virtual)'),
    ]
    INICIO_BIMODAL = [
        ('P', 'Arranca Presencial'),
        ('V', 'Arranca Virtual'),
    ]
    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='comisiones')
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name='comisiones_asignadas')
    docente_auxiliar = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name='comisiones_auxiliares', verbose_name="Pareja Pedagógica")
    ciclo_lectivo = models.IntegerField('Ciclo Lectivo (Año)', default=2026)
    cuatrimestre = models.CharField('Cuatrimestre', max_length=2, choices=CUATRIMESTRES)
    fecha_inicio = models.DateField('Fecha de Inicio', null=True, blank=True)
    fecha_fin = models.DateField('Fecha de Finalización', null=True, blank=True)
    tipo_aprobacion = models.CharField('Tipo de Aprobación', max_length=4, choices=TIPO_APROBACION, default='FIN')
    modalidad = models.CharField('Modalidad', max_length=1, choices=MODALIDAD, default='P')
    semana_inicio_bimodal = models.CharField('Semana de Inicio (Bimodal)', max_length=1, choices=INICIO_BIMODAL, null=True, blank=True)
    inscripciones_abiertas = models.BooleanField('Inscripciones Abiertas', default=True)
    cerrada = models.BooleanField('Comisión Cerrada', default=False)

    def __str__(self):
        return f"{self.materia.nombre} - {self.get_cuatrimestre_display()} {self.ciclo_lectivo} (Prof. {self.docente.apellido if self.docente else 'A designar'})"

class HorarioComision(models.Model):
    DIAS_SEMANA = [
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado')
    ]
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=1, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.get_dia_display()} de {self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')}"

class EventoInstitucional(models.Model):
    TIPOS_EVENTO = [
        ('FERIADO', 'Feriado Nacional / Provincial'),
        ('EVENTO', 'Evento Institucional'),
        ('EXAMEN', 'Semana de Exámenes'),
    ]
    titulo = models.CharField('Título', max_length=200)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    fecha_inicio = models.DateTimeField('Fecha de Inicio')
    fecha_fin = models.DateTimeField('Fecha de Fin', blank=True, null=True)
    tipo = models.CharField('Tipo de Evento', max_length=10, choices=TIPOS_EVENTO, default='EVENTO')
    todo_el_dia = models.BooleanField('Todo el día', default=True)

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo} - {self.fecha_inicio.strftime('%d/%m/%Y')}"

class Inscripcion(models.Model):
    ESTADOS_POSIBLES = [
        ('REG', 'Cursando (Regular)'),
        ('LIB', 'Quedó Libre'),
        ('APR', 'Cursada Aprobada'),
        ('PROM', 'Materia Promocionada'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='alumnos_inscriptos')
    estado = models.CharField('Estado', max_length=4, choices=ESTADOS_POSIBLES, default='REG')
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def faltas_acumuladas(self):
        from decimal import Decimal
        registros = self.alumno.asistencias.filter(planilla__comision=self.comision)
        total = Decimal('0.0')
        for r in registros:
            if r.estado == 'A':
                total += Decimal('1.0')
            elif r.estado == 'T':
                total += Decimal('0.5')
        return float(total)

    def faltas_permitidas(self):
        if self.comision.get_cuatrimestre_display() == 'Anual':
            return 8
        return 4

    def porcentaje_asistencia_restante(self):
        permitidas = self.faltas_permitidas()
        acumuladas = self.faltas_acumuladas()
        if acumuladas >= permitidas:
            return 0
        return int(((permitidas - acumuladas) / permitidas) * 100)
        
    class Meta:
        unique_together = ['alumno', 'comision']

    def __str__(self):
        return f"{self.alumno} en {self.comision}"

class Nota(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='notas')
    valor_nota = models.DecimalField('Nota', max_digits=4, decimal_places=2)
    instancia = models.CharField('Instancia (Ej: 1er Parcial, TP1)', max_length=50)
    fecha = models.DateField('Fecha de Carga', default=date.today)

    def __str__(self):
        return f"{self.valor_nota} - {self.instancia}"


# ==========================================
# 4. ASISTENCIAS Y JUSTIFICATIVOS
# ==========================================

class PlanillaDiaria(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='planillas_asistencia')
    fecha = models.DateField('Fecha', default=date.today)
    tema_dictado = models.TextField('Tema de la Clase (Libro de Temas)', blank=True, null=True)
    
    class Meta:
        unique_together = ['comision', 'fecha']

    def __str__(self):
        return f"Asistencia: {self.comision} - {self.fecha.strftime('%d/%m/%Y')}"

class ProgramaComision(models.Model):
    comision = models.OneToOneField(Comision, on_delete=models.CASCADE, related_name='programa')
    archivo = models.FileField('Archivo del Programa', upload_to='programas/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Programa - {self.comision}"

class RegistroAsistencia(models.Model):
    ESTADOS_ASISTENCIA = [
        ('P', 'Presente'),
        ('A', 'Ausente'),
        ('T', 'Llegada Tarde (Media Falta)'),
        ('J', 'Falta Justificada'),
    ]
    planilla = models.ForeignKey(PlanillaDiaria, on_delete=models.CASCADE, related_name='registros')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    estado = models.CharField('Estado', max_length=1, choices=ESTADOS_ASISTENCIA, default='P')

    def __str__(self):
        return f"{self.alumno.apellido} - {self.get_estado_display()}"
        
class JustificativoAsistencia(models.Model):
    ESTADOS = [
        ('PEND', 'Pendiente de Revisión'),
        ('APR', 'Aprobado'),
        ('RECH', 'Rechazado'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='justificativos')
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name='justificativos')
    fecha_ausencia = models.DateField('Fecha de Inasistencia')
    archivo = models.FileField('Certificado Médico/Laboral', upload_to='justificativos/')
    fecha_carga = models.DateTimeField(auto_now_add=True)
    estado = models.CharField('Estado', max_length=4, choices=ESTADOS, default='PEND')
    observaciones = models.TextField('Observaciones (Bedelía)', blank=True, null=True)

    def __str__(self):
        return f"Justificativo {self.alumno} - {self.fecha_ausencia}"

class Feriado(models.Model):
    fecha = models.DateField(unique=True, verbose_name="Fecha del Feriado")
    motivo = models.CharField(max_length=200, verbose_name="Motivo (ej: Día del Trabajador)")

    def __str__(self):
        return f"{self.fecha.strftime('%d/%m/%Y')} - {self.motivo}"


# ==========================================
# 5. MESAS DE EXAMEN FINALES
# ==========================================

class MesaExamen(models.Model):
    TURNOS = [
        ('FEB_MAR', 'Febrero / Marzo'),
        ('JUL_AGO', 'Julio / Agosto'),
        ('NOV_DIC', 'Noviembre / Diciembre'),
        ('ESPECIAL', 'Mesa Especial / Única'),
    ]
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='mesas_examen')
    turno = models.CharField('Turno', max_length=20, choices=TURNOS, default='NOV_DIC')
    fecha_hora = models.DateTimeField('Fecha y Hora')
    presidente_mesa = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, related_name='mesas_presidente')
    vocal_1 = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name='mesas_vocal1')
    vocal_2 = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, related_name='mesas_vocal2')
    ciclo_lectivo = models.IntegerField('Ciclo Lectivo', default=2026)
    inscripciones_abiertas = models.BooleanField('Inscripciones Abiertas', default=True)
    cerrada = models.BooleanField('Mesa Cerrada', default=False)
    libro = models.CharField('Libro', max_length=50, null=True, blank=True)
    folio = models.CharField('Folio', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Mesa de {self.materia.nombre} ({self.get_turno_display()}) - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"

class InscripcionMesa(models.Model):
    ESTADOS_MESA = [
        ('PEND', 'Pendiente'),
        ('APR', 'Aprobado'),
        ('REP', 'Reprobado'),
        ('AUS', 'Ausente'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='mesas_inscriptas')
    mesa = models.ForeignKey(MesaExamen, on_delete=models.CASCADE, related_name='inscriptos')
    nota_final = models.DecimalField('Nota Final', max_digits=4, decimal_places=2, null=True, blank=True)
    estado = models.CharField('Estado', max_length=4, choices=ESTADOS_MESA, default='PEND')

    class Meta:
        unique_together = ['alumno', 'mesa']

    def __str__(self):
        return f"{self.alumno.apellido} en {self.mesa}"


# ==========================================
# 6. MÓDULO IA / CHATBOT
# ==========================================

class TicketReclamo(models.Model):
    ESTADOS_TICKET = [
        ('ABIERTO', 'Abierto'),
        ('PROCESO', 'En Proceso'),
        ('RESUELTO', 'Resuelto'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='tickets')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asunto = models.CharField('Asunto', max_length=200)
    descripcion = models.TextField('Descripción del Reclamo/Consulta')
    estado = models.CharField('Estado', max_length=10, choices=ESTADOS_TICKET, default='ABIERTO')

    def __str__(self):
        return f"Ticket #{self.id} - {self.alumno.apellido} - {self.get_estado_display()}"


# ==========================================
# 7. HISTORIAL ACADÉMICO (EQUIVALENCIAS)
# ==========================================

class Equivalencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='equivalencias')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='equivalencias_otorgadas')
    resolucion = models.CharField('Número de Resolución', max_length=100)
    institucion_origen = models.CharField('Institución de Origen', max_length=200, blank=True, null=True)
    fecha_otorgamiento = models.DateField('Fecha de Otorgamiento', default=date.today)
    nota = models.DecimalField('Nota Reconocida', max_digits=4, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ['alumno', 'materia']

    def __str__(self):
        return f"{self.alumno} - {self.materia} (Res: {self.resolucion})"

# ==========================================
# 8. COMUNICACIONES Y NOTIFICACIONES
# ==========================================

class Comunicado(models.Model):
    DESTINATARIOS_CHOICES = [
        ('TODOS', 'Toda la Institución'),
        ('DOCENTES', 'Todos los Docentes'),
        ('DOCENTES_CARRERA', 'Docentes por Carrera'),
        ('ALUMNOS', 'Todos los Alumnos'),
        ('ALUMNOS_CARRERA', 'Alumnos por Carrera'),
        ('COMISION', 'Alumnos de una Comisión Específica'),
    ]
    titulo = models.CharField('Título', max_length=200)
    mensaje = models.TextField('Mensaje')
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comunicados_enviados')
    
    # Segmentación
    tipo_destinatario = models.CharField('Destinatarios', max_length=20, choices=DESTINATARIOS_CHOICES)
    plan_estudio = models.ForeignKey(PlanDeEstudio, on_delete=models.CASCADE, null=True, blank=True, help_text="Requerido si se envía por carrera")
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, null=True, blank=True, help_text="Requerido si se envía a una comisión")

    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_destinatario_display()}"

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    comunicado = models.ForeignKey(Comunicado, on_delete=models.CASCADE, related_name='notificaciones_individuales')
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['usuario', 'comunicado']

    def __str__(self):
        estado = "Leída" if self.leida else "No leída"
        return f"Notificación para {self.usuario.username} - {estado}"