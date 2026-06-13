import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from django.contrib.auth.models import User, Group
from gestion.models import PlanDeEstudio, Materia, Correlatividad, Docente, Alumno, Comision

def seed():
    # 1. CREAR GRUPOS
    grp_secretaria, _ = Group.objects.get_or_create(name='Secretaria')
    grp_docentes, _ = Group.objects.get_or_create(name='Docentes')
    grp_estudiantes, _ = Group.objects.get_or_create(name='Estudiantes')

    # 2. CREAR ADMIN (Secretaría)
    if not User.objects.filter(email='admin@admin.com').exists():
        admin_user = User.objects.create_superuser('admin@admin.com', 'admin@admin.com', 'admin')
        admin_user.groups.add(grp_secretaria)
        print("Admin creado (user/pass: admin@admin.com / admin)")

    # 3. CREAR PLAN Y MATERIAS
    plan, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Tecn. Sup. en Análisis de Sistemas',
        defaults={'resolucion_ministerial': 'Res. N° 521/SSPLINED/16'}
    )

    materias_dict = {}

    def crear_m(nombre, anio):
        m, _ = Materia.objects.get_or_create(nombre=nombre, plan=plan, año_dictado=anio)
        materias_dict[nombre] = m
        return m

    # 1er Año
    crear_m("Comunicación Visual", 1)
    crear_m("Programación Web I", 1)
    crear_m("Organización Empresarial", 1)
    crear_m("Elementos de la Matemática", 1)
    crear_m("Introducción a la Programación", 1)
    crear_m("Base de Datos I", 1)
    crear_m("Programación Web II", 1)
    crear_m("Experiencia de Usuario", 1)
    crear_m("Sistemas Empresariales", 1)
    crear_m("Programación Orientada a Objetos", 1)

    # 2do Año
    crear_m("Base de Datos II", 2)
    crear_m("Programación Avanzada", 2)
    crear_m("Ingeniería de Requerimientos", 2)
    crear_m("Arquitectura y Sistemas Operativos", 2)
    crear_m("Práctica Profesionalizante I: Producción Web", 2)
    crear_m("Aplicaciones Móviles", 2)
    crear_m("Comunicaciones y Redes", 2)
    crear_m("Plataforma de Desarrollo", 2)
    crear_m("Análisis y Metodología de Sistemas", 2)
    crear_m("Práctica Profesionalizante II: Base de Datos III", 2)

    # 3er Año
    crear_m("Estadística", 3)
    crear_m("Diseño de Sistemas", 3)
    crear_m("Administración de Proyectos", 3)
    crear_m("Planificación del Seminario Final", 3)
    crear_m("Práctica Profesionalizante III: Integración Tecnológica", 3)
    crear_m("Acreditación de Talleres, Jornadas o Seminarios de Actualización", 3) # Extra info del PDF
    crear_m("Calidad de Software", 3)
    crear_m("Seguridad e Integridad", 3)
    crear_m("Ética y Deontología Profesional", 3)
    crear_m("Modelos Estratégicos de Negocios", 3)
    crear_m("Práctica Profesionalizante VI: Seminario Final", 3)

    # 4. CORRELATIVIDADES
    def correlativa(m_nombre, req_nombre):
        m = materias_dict.get(m_nombre)
        r = materias_dict.get(req_nombre)
        if m and r:
            Correlatividad.objects.get_or_create(materia=m, requisito=r, tipo='CUR')

    # 1er Año
    correlativa("Programación Web II", "Programación Web I")
    correlativa("Programación Orientada a Objetos", "Introducción a la Programación")

    # 2do Año
    correlativa("Base de Datos II", "Base de Datos I")
    correlativa("Programación Avanzada", "Programación Orientada a Objetos")
    correlativa("Práctica Profesionalizante I: Producción Web", "Programación Web II")
    correlativa("Aplicaciones Móviles", "Elementos de la Matemática")
    correlativa("Plataforma de Desarrollo", "Programación Web II")
    correlativa("Análisis y Metodología de Sistemas", "Ingeniería de Requerimientos")
    correlativa("Práctica Profesionalizante II: Base de Datos III", "Base de Datos II")

    # 3er Año
    correlativa("Estadística", "Elementos de la Matemática")
    correlativa("Diseño de Sistemas", "Análisis y Metodología de Sistemas")
    correlativa("Administración de Proyectos", "Análisis y Metodología de Sistemas")
    correlativa("Planificación del Seminario Final", "Aplicaciones Móviles")
    correlativa("Planificación del Seminario Final", "Plataforma de Desarrollo")
    correlativa("Planificación del Seminario Final", "Análisis y Metodología de Sistemas")

    # Práctica Profesionalizante VI: Seminario Final (requiere muchas)
    m_seminario = materias_dict["Práctica Profesionalizante VI: Seminario Final"]
    reqs_seminario = [
        "Práctica Profesionalizante III: Integración Tecnológica",
        "Diseño de Sistemas",
        "Administración de Proyectos",
        "Planificación del Seminario Final",
        "Estadística"
    ]
    # Y todas las de 1er y 2do año
    for m in Materia.objects.filter(año_dictado__in=[1, 2]):
        Correlatividad.objects.get_or_create(materia=m_seminario, requisito=m, tipo='CUR')
    
    for r in reqs_seminario:
        correlativa("Práctica Profesionalizante VI: Seminario Final", r)

    print("Materias y Correlatividades creadas.")

    # 5. CREAR DOCENTE DE PRUEBA
    dni_docente = "20123456"
    email_docente = "docente@test.com"
    if not User.objects.filter(username=email_docente).exists():
        u_docente = User.objects.create_user(username=email_docente, email=email_docente, password=dni_docente)
        u_docente.groups.add(grp_docentes)
        Docente.objects.create(usuario=u_docente, dni=dni_docente, nombre="Juan", apellido="Perez", email=email_docente)
        print(f"Docente creado (user/pass: {email_docente} / {dni_docente})")

    # 6. CREAR ALUMNO DE PRUEBA
    dni_alumno = "40123456"
    email_alumno = "alumno@test.com"
    if not User.objects.filter(username=email_alumno).exists():
        u_alumno = User.objects.create_user(username=email_alumno, email=email_alumno, password=dni_alumno)
        u_alumno.groups.add(grp_estudiantes)
        Alumno.objects.create(usuario=u_alumno, dni=dni_alumno, nombre="Lucas", apellido="Gomez", email=email_alumno)
        print(f"Alumno creado (user/pass: {email_alumno} / {dni_alumno})")

    # 7. CREAR ALGUNAS COMISIONES DE EJEMPLO
    docente = Docente.objects.first()
    for mat_name in ["Introducción a la Programación", "Programación Web I"]:
        mat = materias_dict[mat_name]
        Comision.objects.get_or_create(
            materia=mat,
            docente=docente,
            ciclo_lectivo=2026,
            cuatrimestre='1C',
            dias_horarios="Martes 19:00 a 22:00",
            tipo_aprobacion='FIN'
        )
    print("Comisiones de ejemplo creadas.")

if __name__ == '__main__':
    seed()
