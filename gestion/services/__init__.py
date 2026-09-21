
from datetime import date
from ..models import PlanillaDiaria, RegistroAsistencia, Inscripcion, Materia, Feriado

def generar_planilla_del_dia(comision, fecha=None):
    if fecha is None:
        fecha = date.today()
        
    # 1. Chequeamos si es finde (En Python: 0=Lunes, 4=Viernes, 5=SÃ¡bado, 6=Domingo)
    if fecha.weekday() >= 5:
        return False, "Es fin de semana. No hay clases."

    # 2. Chequeamos si es Feriado
    feriado = Feriado.objects.filter(fecha=fecha).first()
    if feriado:
        return False, f"DÃ­a no laborable: {feriado.motivo}"

    # 3. Buscamos a los inscriptos
    inscripciones = Inscripcion.objects.filter(comision=comision)
    if not inscripciones.exists():
        return False, "No hay alumnos inscriptos en esta comisiÃ³n todavÃ­a."

    # 4. Magia de Django: Trae la planilla o la crea
    planilla, creada = PlanillaDiaria.objects.get_or_create(comision=comision, fecha=fecha)
    
    for insc in inscripciones:
        RegistroAsistencia.objects.get_or_create(
            planilla=planilla,
            alumno=insc.alumno
        )
        
    return True, "Planilla lista."

def enviar_comunicado(comunicado):
    from django.contrib.auth.models import User
    from ..models import Notificacion, Alumno, Docente, Inscripcion, Comision
    
    usuarios_destino = set()
    
    if comunicado.tipo_destinatario == 'TODOS':
        usuarios_destino = set(User.objects.all())
        
    elif comunicado.tipo_destinatario == 'DOCENTES':
        usuarios_destino = set(User.objects.filter(perfil_docente__isnull=False))
        
    elif comunicado.tipo_destinatario == 'DOCENTES_CARRERA' and comunicado.plan_estudio:
        # Docentes de materias de ese plan
        docentes = Docente.objects.filter(comisiones_asignadas__materia__plan=comunicado.plan_estudio)
        for d in docentes:
            if d.usuario:
                usuarios_destino.add(d.usuario)
                
    elif comunicado.tipo_destinatario == 'ALUMNOS':
        usuarios_destino = set(User.objects.filter(perfil_alumno__isnull=False))
        
    elif comunicado.tipo_destinatario == 'ALUMNOS_CARRERA' and comunicado.plan_estudio:
        alumnos = Alumno.objects.filter(plan=comunicado.plan_estudio)
        for a in alumnos:
            if a.usuario:
                usuarios_destino.add(a.usuario)
                
    elif comunicado.tipo_destinatario == 'COMISION' and comunicado.comision:
        # Solo alumnos REGulares ("MIENTRAS ESTEN CURSANDO")
        inscripciones = Inscripcion.objects.filter(comision=comunicado.comision, estado='REG')
        for i in inscripciones:
            if i.alumno.usuario:
                usuarios_destino.add(i.alumno.usuario)
        
        # TambiÃ©n incluir al docente si es un admin quien manda
        if comunicado.comision.docente and comunicado.comision.docente.usuario:
            usuarios_destino.add(comunicado.comision.docente.usuario)

    # Crear las notificaciones en el sistema
    notificaciones_a_crear = []
    emails_destino = []
    
    for u in usuarios_destino:
        notificaciones_a_crear.append(Notificacion(usuario=u, comunicado=comunicado))
        if u.email:
            emails_destino.append(u.email)
            
    Notificacion.objects.bulk_create(notificaciones_a_crear, ignore_conflicts=True)
    
    # Enviar correo electrÃ³nico
    if emails_destino:
        from django.core.mail import send_mail
        from django.conf import settings
        import logging
        
        logger = logging.getLogger(__name__)
        
        cuerpo_mensaje = f"{comunicado.mensaje}\n\n---\nEste es un mensaje automÃ¡tico de SiGeEt. Por favor, no respondas a este correo."
        
        try:
            send_mail(
                subject=f"[SiGeEt] {comunicado.titulo}",
                message=cuerpo_mensaje,
                from_email=settings.EMAIL_HOST_USER or 'sigeet@pioix.edu.ar',
                recipient_list=[], # Vacio para que no se vean entre si en "Para"
                fail_silently=True,
                bcc=emails_destino
            )
        except Exception as e:
            # Capturamos cualquier error (timeout, credenciales invÃ¡lidas, etc)
            # para que no impida la creaciÃ³n de la notificaciÃ³n interna.
            logger.error(f"Error al enviar correo del comunicado {comunicado.id}: {e}")
