import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from gestion.models import Materia, Docente, Alumno

CREDENTIALS_FILE = '/app/google_credentials.json' if os.path.exists('/app/google_credentials.json') else 'google_credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.profile.emails'
]

def get_classroom_service():
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    try:
        creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        return build('classroom', 'v1', credentials=creds)
    except Exception as e:
        print(f"Error autenticando con Google Classroom: {e}")
        return None

def obtener_o_crear_aula_materia(materia):
    if materia.google_classroom_id:
        return materia.google_classroom_id

    service = get_classroom_service()
    if not service:
        return None

    course = {
        'name': materia.nombre,
        'section': f"{materia.plan.nombre} ({materia.get_cuatrimestre_dictado_display()})",
        'descriptionHeading': 'Aula generada automaticamente por SIGES',
        'ownerId': 'me',
        'courseState': 'ACTIVE'
    }

    try:
        course_created = service.courses().create(body=course).execute()
        materia.google_classroom_id = course_created.get('id')
        materia.google_classroom_url = course_created.get('alternateLink')
        materia.save()
        return materia.google_classroom_id
    except Exception as e:
        print(f"Error creando aula para {materia.nombre}: {e}")
        return None

def invitar_usuario_a_aula(course_id, email, role='STUDENT'):
    if not email:
        return False
        
    # Restricción: Solo cuentas institucionales
    if not email.strip().lower().endswith('@pioix.edu.ar'):
        print(f"Invitacion rechazada: El correo {email} no es institucional (@pioix.edu.ar)")
        return False
        
    service = get_classroom_service()
    if not service:
        return False

    invitation = {
        'courseId': course_id,
        'userId': email,
        'role': role
    }

    try:
        service.invitations().create(body=invitation).execute()
        return True
    except Exception as e:
        print(f"Error invitando a {email} como {role}: {e}")
        return False

def invitar_equipo_docente(materia, docente_principal):
    if not materia.google_classroom_id:
        return

    # 1. Supervisor Global (Cuenta Maestra)
    invitar_usuario_a_aula(materia.google_classroom_id, 'secretaria.alumnos@pioix.edu.ar', role='TEACHER')

    # 2. Docente titular usando su correo institucional
    if docente_principal and hasattr(docente_principal, 'correo_institucional') and docente_principal.correo_institucional:
        invitar_usuario_a_aula(materia.google_classroom_id, docente_principal.correo_institucional, role='TEACHER')
        
    # 3. Tutores / Coordinadores
    tutores = Docente.objects.filter(carreras_coordinadas=materia.plan)
    for tutor in tutores:
        if hasattr(tutor, 'correo_institucional') and tutor.correo_institucional and tutor != docente_principal:
            invitar_usuario_a_aula(materia.google_classroom_id, tutor.correo_institucional, role='TEACHER')

def invitar_alumno_a_aula(materia, alumno):
    if not materia.google_classroom_id:
        return
    
    if hasattr(alumno, 'correo_institucional') and alumno.correo_institucional:
        invitar_usuario_a_aula(materia.google_classroom_id, alumno.correo_institucional, role='STUDENT')

def remover_todos_los_alumnos(course_id):
    service = get_classroom_service()
    if not service:
        return 0
        
    removed_count = 0
    try:
        # Obtener lista de alumnos
        results = service.courses().students().list(courseId=course_id).execute()
        students = results.get('students', [])
        
        # Eliminar uno por uno
        for student in students:
            user_id = student.get('userId')
            try:
                service.courses().students().delete(courseId=course_id, userId=user_id).execute()
                removed_count += 1
            except Exception as inner_e:
                print(f"Error eliminando alumno {user_id}: {inner_e}")
                
        return removed_count
    except Exception as e:
        print(f"Error listando alumnos para borrar: {e}")
        return 0
