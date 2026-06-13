import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import PlanDeEstudio, Materia, Curso, Correlatividad

def seed():
    # Crear el Plan
    plan = PlanDeEstudio.objects.create(
        nombre='Tecnicatura Superior en Análisis de Sistemas',
        resolucion_ministerial='Res. N° 521/SSPLINED/16'
    )
    print(f"Plan creado: {plan.nombre}")

    # Diccionarios para guardar las materias y poder usarlas en las correlatividades
    materias_dict = {}

    def crear_materia(nombre, anio):
        m = Materia.objects.create(nombre=nombre, plan=plan, año_dictado=anio)
        materias_dict[nombre] = m
        return m

    # 1er Año
    crear_materia("Comunicación Visual", 1)
    crear_materia("Base de Datos I", 1)
    crear_materia("Programación Web I", 1)
    crear_materia("Programación Web II", 1)
    crear_materia("Organización Empresarial", 1)
    crear_materia("Experiencia de Usuario", 1)
    crear_materia("Elementos de la Matemática", 1)
    crear_materia("Sistemas Empresariales", 1)
    crear_materia("Introducción a la Programación", 1)
    crear_materia("Programación Orientada a Objetos", 1)

    # 2do Año
    crear_materia("Base de Datos II", 2)
    crear_materia("Aplicaciones Móviles", 2)
    crear_materia("Programación Avanzada", 2)
    crear_materia("Comunicaciones y Redes", 2)
    crear_materia("Ingeniería de Requerimientos", 2)
    crear_materia("Plataforma de Desarrollo", 2)
    crear_materia("Arquitectura y Sistemas Operativos", 2)
    crear_materia("Análisis y Metodología de Sistemas", 2)
    crear_materia("Práctica Profesionalizante I: Producción Web", 2)
    crear_materia("Práctica Profesionalizante II: Base de Datos III", 2)

    # 3er Año
    crear_materia("Estadística", 3)
    crear_materia("Calidad de Software", 3)
    crear_materia("Diseño de Sistemas", 3)
    crear_materia("Seguridad e Integridad", 3)
    crear_materia("Administración de Proyectos", 3)
    crear_materia("Ética y Deontología Profesional", 3)
    crear_materia("Planificación del Seminario Final", 3)
    crear_materia("Modelos Estratégicos de Negocios", 3)
    crear_materia("Práctica Profesionalizante III: Integración Tecnológica", 3)
    crear_materia("Práctica Profesionalizante VI: Seminario Final", 3)

    # Creando correlatividades lógicas
    def correlativa(materia_nombre, requisito_nombre, tipo='CUR'):
        materia = materias_dict.get(materia_nombre)
        requisito = materias_dict.get(requisito_nombre)
        if materia and requisito:
            Correlatividad.objects.create(materia=materia, requisito=requisito, tipo=tipo)

    # Correlatividades de 1er año (asumiendo 2do cuatri requiere 1er cuatri)
    correlativa("Programación Web II", "Programación Web I", "CUR")
    correlativa("Programación Orientada a Objetos", "Introducción a la Programación", "CUR")

    # Correlatividades de 2do año
    correlativa("Base de Datos II", "Base de Datos I", "CUR")
    correlativa("Programación Avanzada", "Programación Orientada a Objetos", "CUR")
    correlativa("Arquitectura y Sistemas Operativos", "Sistemas Empresariales", "CUR")
    correlativa("Análisis y Metodología de Sistemas", "Ingeniería de Requerimientos", "CUR")
    correlativa("Práctica Profesionalizante I: Producción Web", "Programación Web II", "CUR")
    correlativa("Práctica Profesionalizante II: Base de Datos III", "Base de Datos II", "CUR")

    # Correlatividades de 3er año
    correlativa("Estadística", "Elementos de la Matemática", "CUR")
    correlativa("Diseño de Sistemas", "Análisis y Metodología de Sistemas", "CUR")
    correlativa("Práctica Profesionalizante III: Integración Tecnológica", "Práctica Profesionalizante I: Producción Web", "APR")
    correlativa("Práctica Profesionalizante VI: Seminario Final", "Planificación del Seminario Final", "CUR")

    # Crear algunos cursos iniciales
    Curso.objects.create(plan=plan, año_de_cursada=1, division='A', turno='N')
    Curso.objects.create(plan=plan, año_de_cursada=2, division='A', turno='N')
    Curso.objects.create(plan=plan, año_de_cursada=3, division='A', turno='N')

    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        print("Superusuario 'admin' (pass: 'admin') creado.")

    print("Carga completa. Materias, correlatividades y cursos iniciales creados.")

if __name__ == '__main__':
    seed()
