import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import PlanDeEstudio, Materia, Correlatividad

def main():
    print("--- 1. ACTUALIZANDO CUATRIMESTRES DE SISTEMAS ---")
    
    # Text definition
    sistemas_1c = [
        "Comunicación Visual", "Programación Web I", "Organización Empresarial", 
        "Elementos de la Matemática", "Introducción a la Programación",
        "Base de Datos II", "Programación Avanzada", "Ingeniería de Requerimientos", 
        "Arquitectura y Sistemas Operativos", "Práctica Profesionalizante I: Producción Web",
        "Estadística", "Diseño de Sistemas", "Administración de Proyectos", 
        "Planificación del Seminario Final", "Práctica Profesionalizante III: Integración Tecnológica"
    ]
    
    sistemas_2c = [
        "Base de Datos I", "Programación Web II", "Experiencia de Usuario", "Sistemas Empresariales", 
        "Programación Orientada a Objetos", "Aplicaciones Móviles", "Comunicaciones y Redes", 
        "Plataforma de Desarrollo", "Análisis y Metodología de Sistemas", "Práctica Profesionalizante II: Base de Datos III",
        "Calidad de Software", "Seguridad e Integridad", "Ética y Deontología Profesional", 
        "Modelos Estratégicos de Negocios", "Práctica Profesionalizante VI: Seminario Final"
    ]
    
    sistemas_an = [
        "Acreditación de Talleres, Jornadas o Seminarios de Actualización"
    ]

    for m_name in sistemas_1c:
        Materia.objects.filter(nombre__iexact=m_name, plan__nombre__icontains='Sistemas').update(cuatrimestre_dictado='1C')
    for m_name in sistemas_2c:
        Materia.objects.filter(nombre__iexact=m_name, plan__nombre__icontains='Sistemas').update(cuatrimestre_dictado='2C')
    for m_name in sistemas_an:
        Materia.objects.filter(nombre__iexact=m_name, plan__nombre__icontains='Sistemas').update(cuatrimestre_dictado='AN')
        
    print("Materias de Sistemas actualizadas con sus cuatrimestres respectivos.")

    print("\n--- 2. CREANDO PLAN DE CIENCIAS SAGRADAS ---")
    plan_cs, created = PlanDeEstudio.objects.get_or_create(
        nombre="Prof. de Educ. Sup. en Ciencias Sagradas",
        defaults={'resolucion_ministerial': 'Res. N° 4184/MEGC/14'}
    )
    
    materias_cs = {
        1: {
            'AN': ["Griego", "Filosofía", "Psicología", "Pedagogía", "Filosofía Antigua"],
            '1C': ["Introducción a la teología", "Historia de Iglesia Antigua", "Lectura, escritura y oralidad", "Teología pastoral fundamental", "Introducción al Antiguo Testamento"],
            '2C': ["Patrología", "Orígenes cristianos", "Métodos exegéticos", "Metodología de la Investigación", "Observación institucional y áulica", "Introducción al Nuevo Testamento"]
        },
        2: {
            'AN': ["Didáctica General", "Filosofía Medieval", "Misterio de Dios y Trinidad", "Psicología de los Sujetos de la Educación"],
            '1C': ["Pentateuco", "Escritos Paulinos", "Psicología Educacional", "Historia de la Iglesia Medieval", "Observación de las acciones Pastorales"],
            '2C': ["Profetas", "Sinópticos y Hechos", "Teología Fundamental", "Instituciones Educativas", "Teología Litúrgico Sacramental", "Investigación de la Práctica Docente"]
        },
        3: {
            'AN': ["Sociología", "Cristología", "Didáctica Especial", "Filosofía Moderna", "Ayudantía y Práctica"],
            '1C': ["Libros Históricos", "Escritos Joánicos", "Moral Fundamental", "Creación y Antropología", "Nuevos escenarios: Cultura, tecnología y subjetividad"],
            '2C': ["Gracia y escatología", "Salmos y Sapienciales", "Educación Sexual Integral", "Historia de la Iglesia Moderna y Contemporánea"]
        },
        4: {
            'AN': ["Filosofía para Teólogos", "Filosofía Contemporánea", "Eclesiología y Misionología", "Problemáticas de los Niveles Educativos", "Ecumenismo y Teología del Pluralismo Religioso"],
            '1C': ["Bioética", "Nuevas Tecnologías", "Sistema y Política Educativa", "Pastoral de la Palabra y la Liturgia", "Historia de la iglesia Latinoamericana y Argentina"],
            '2C': ["Síntesis Pastoral", "Pastoral de la Comunidad", "Historia de la Educación Argentina", "Hebreos, Apocalipsis y Cartas Pastorales", "Historia de la Iglesia Argentina Contemporánea"]
        },
        5: {
            'AN': ["Residencia"],
            '1C': ["Moral Social", "Sacramentos I", "Sacramentos II", "Gestión Educativa", "Teología Espiritual", "Teología Latinoamericana y Argentina"],
            '2C': []
        }
    }
    
    materias_dict = {}
    for year, periodos in materias_cs.items():
        for periodo, m_names in periodos.items():
            for m_name in m_names:
                m, _ = Materia.objects.get_or_create(
                    nombre=m_name,
                    plan=plan_cs,
                    defaults={'año_dictado': year, 'cuatrimestre_dictado': periodo}
                )
                if m.cuatrimestre_dictado != periodo:
                    m.cuatrimestre_dictado = periodo
                    m.save()
                materias_dict[m_name] = m
                
    print(f"Creadas/Actualizadas {len(materias_dict)} materias de Ciencias Sagradas.")
    
    print("\n--- 3. CREANDO CORRELATIVIDADES CIENCIAS SAGRADAS ---")
    
    def correlativa(m_nombre, req_nombre):
        m = materias_dict.get(m_nombre)
        r = materias_dict.get(req_nombre)
        if m and r:
            Correlatividad.objects.get_or_create(materia=m, requisito=r, tipo='APR')
            
    # Asignaciones del PDF 2 (Correlativas)
    # 2do año
    correlativa("Filosofía Medieval", "Filosofía Antigua")
    correlativa("Misterio de Dios y Trinidad", "Introducción a la teología")
    correlativa("Misterio de Dios y Trinidad", "Teología Fundamental")
    correlativa("Psicología de los Sujetos de la Educación", "Psicología")
    correlativa("Pentateuco", "Introducción al Antiguo Testamento")
    correlativa("Pentateuco", "Métodos exegéticos")
    correlativa("Escritos Paulinos", "Introducción al Antiguo Testamento")
    correlativa("Escritos Paulinos", "Métodos exegéticos")
    correlativa("Escritos Paulinos", "Griego")
    correlativa("Psicología Educacional", "Psicología")
    correlativa("Historia de la Iglesia Medieval", "Historia de Iglesia Antigua")
    correlativa("Observación de las acciones Pastorales", "Teología pastoral fundamental")
    correlativa("Profetas", "Introducción al Antiguo Testamento")
    correlativa("Profetas", "Métodos exegéticos")
    correlativa("Sinópticos y Hechos", "Introducción al Antiguo Testamento")
    correlativa("Sinópticos y Hechos", "Métodos exegéticos")
    correlativa("Sinópticos y Hechos", "Griego")
    correlativa("Teología Litúrgico Sacramental", "Introducción a la teología")
    correlativa("Teología Litúrgico Sacramental", "Teología Fundamental")
    
    # 3er año
    correlativa("Cristología", "Introducción a la teología")
    correlativa("Cristología", "Teología Fundamental")
    correlativa("Didáctica Especial", "Didáctica General")
    correlativa("Filosofía Moderna", "Filosofía Medieval")
    correlativa("Ayudantía y Práctica", "Observación institucional y áulica")
    correlativa("Ayudantía y Práctica", "Observación de las acciones Pastorales")
    correlativa("Ayudantía y Práctica", "Investigación de la Práctica Docente")
    correlativa("Ayudantía y Práctica", "Didáctica Especial")
    correlativa("Libros Históricos", "Introducción al Antiguo Testamento")
    correlativa("Libros Históricos", "Métodos exegéticos")
    correlativa("Escritos Joánicos", "Introducción al Antiguo Testamento")
    correlativa("Escritos Joánicos", "Métodos exegéticos")
    correlativa("Escritos Joánicos", "Griego")
    correlativa("Creación y Antropología", "Introducción a la teología")
    correlativa("Creación y Antropología", "Teología Fundamental")
    correlativa("Gracia y escatología", "Introducción a la teología")
    correlativa("Gracia y escatología", "Teología Fundamental")
    correlativa("Salmos y Sapienciales", "Introducción al Antiguo Testamento")
    correlativa("Salmos y Sapienciales", "Métodos exegéticos")
    correlativa("Historia de la Iglesia Moderna y Contemporánea", "Historia de la Iglesia Medieval")
    
    # 4to año
    correlativa("Filosofía para Teólogos", "Filosofía")
    correlativa("Filosofía Contemporánea", "Filosofía Moderna")
    correlativa("Eclesiología y Misionología", "Introducción a la teología")
    correlativa("Eclesiología y Misionología", "Teología Fundamental")
    correlativa("Ecumenismo y Teología del Pluralismo Religioso", "Introducción a la teología")
    correlativa("Ecumenismo y Teología del Pluralismo Religioso", "Teología Fundamental")
    correlativa("Bioética", "Moral Fundamental")
    correlativa("Pastoral de la Palabra y la Liturgia", "Teología pastoral fundamental")
    correlativa("Pastoral de la Palabra y la Liturgia", "Observación institucional y áulica")
    correlativa("Pastoral de la Palabra y la Liturgia", "Observación de las acciones Pastorales")
    correlativa("Pastoral de la Palabra y la Liturgia", "Investigación de la Práctica Docente")
    correlativa("Historia de la iglesia Latinoamericana y Argentina", "Historia de la Iglesia Moderna y Contemporánea")
    correlativa("Síntesis Pastoral", "Teología pastoral fundamental")
    correlativa("Síntesis Pastoral", "Observación institucional y áulica")
    correlativa("Síntesis Pastoral", "Observación de las acciones Pastorales")
    correlativa("Síntesis Pastoral", "Investigación de la Práctica Docente")
    correlativa("Pastoral de la Comunidad", "Teología pastoral fundamental")
    correlativa("Pastoral de la Comunidad", "Observación institucional y áulica")
    correlativa("Pastoral de la Comunidad", "Observación de las acciones Pastorales")
    correlativa("Pastoral de la Comunidad", "Investigación de la Práctica Docente")
    correlativa("Hebreos, Apocalipsis y Cartas Pastorales", "Introducción al Antiguo Testamento")
    correlativa("Hebreos, Apocalipsis y Cartas Pastorales", "Métodos exegéticos")
    correlativa("Hebreos, Apocalipsis y Cartas Pastorales", "Griego")
    correlativa("Historia de la Iglesia Argentina Contemporánea", "Historia de la iglesia Latinoamericana y Argentina")
    
    # 5to año
    correlativa("Residencia", "Observación institucional y áulica")
    correlativa("Residencia", "Observación de las acciones Pastorales")
    correlativa("Residencia", "Investigación de la Práctica Docente")
    correlativa("Residencia", "Didáctica Especial")
    correlativa("Residencia", "Ayudantía y Práctica")
    correlativa("Residencia", "Pastoral de la Comunidad")
    correlativa("Residencia", "Pastoral de la Palabra y la Liturgia")
    correlativa("Residencia", "Síntesis Pastoral")
    
    correlativa("Moral Social", "Moral Fundamental")
    correlativa("Sacramentos I", "Introducción a la teología")
    correlativa("Sacramentos I", "Teología Fundamental")
    correlativa("Sacramentos I", "Teología Litúrgico Sacramental")
    correlativa("Sacramentos II", "Introducción a la teología")
    correlativa("Sacramentos II", "Teología Fundamental")
    correlativa("Sacramentos II", "Teología Litúrgico Sacramental")
    correlativa("Teología Espiritual", "Introducción a la teología")
    correlativa("Teología Espiritual", "Teología Fundamental")
    correlativa("Teología Latinoamericana y Argentina", "Introducción a la teología")
    correlativa("Teología Latinoamericana y Argentina", "Teología Fundamental")
    
    print("Correlatividades de Ciencias Sagradas cargadas.")

if __name__ == '__main__':
    main()
