import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import PlanDeEstudio, Materia, Correlatividad

def run():
    print("Creando nuevo Plan de Locución 2025...")
    
    plan, _ = PlanDeEstudio.objects.get_or_create(
        nombre="Tecnicatura Superior en Locución Integral (2025)",
        defaults={'resolucion_ministerial': 'IF-2025-13731090-GCABA-DGEGP'}
    )
    
    materias_data = {
        # PRIMER AÑO - 1C
        "Introducción a la Locución": (1, "1C"),
        "Introducción al Entrenamiento Vocal": (1, "1C"),
        "Práctica Profesionalizante en Locución para Televisión": (1, "1C"),
        "Expresión Corporal": (1, "1C"),
        "Herramientas de Producción y Edición Digital": (1, "1C"),
        "EDI 1": (1, "1C"),
        
        # PRIMER AÑO - 2C
        "Locución, Interpretación y Lectura": (1, "2C"),
        "Entrenamiento Vocal": (1, "2C"),
        "Práctica Profesionalizante en Locución para Radio": (1, "2C"),
        "Redacción y Edición de Contenidos": (1, "2C"),
        "Pronunciación de Italiano y Francés": (1, "2C"),
        "EDI 2": (1, "2C"),
        
        # SEGUNDO AÑO - 1C
        "Locución Artística y Publicitaria": (2, "1C"),
        "Educación Vocal": (2, "1C"),
        "Práctica Profesionalizante en Conducción para Radio": (2, "1C"),
        "Práctica Profesionalizante en Conducción para Televisión": (2, "1C"),
        "Técnicas Periodísticas": (2, "1C"),
        "Libretos y Guiones": (2, "1C"),
        
        # SEGUNDO AÑO - 2C
        "Locución Aplicada e Improvisación": (2, "2C"),
        "Técnica Vocal": (2, "2C"),
        "Práctica Profesionalizante en Podcast y Producción de Contenidos Digitales": (2, "2C"),
        "Locución de Contenidos para Medios Audiovisuales": (2, "2C"),
        "Pronunciación de Inglés": (2, "2C"),
        "Comunicación Convergente": (2, "2C"),
        
        # TERCER AÑO - 1C
        "Locución para Medios Digitales": (3, "1C"),
        "Técnica Vocal Avanzada": (3, "1C"),
        "Práctica Profesionalizante en Radio y Streaming": (3, "1C"),
        "Plataformas Digitales y Nuevas Tendencias Audiovisuales": (3, "1C"),
        "Pronunciación de Alemán y Portugués": (3, "1C"),
        "Técnicas de Doblaje": (3, "1C"),
        
        # TERCER AÑO - 2C
        "Taller Integrador de Locución": (3, "2C"),
        "Taller Integrador de la Voz": (3, "2C"),
        "Taller Integrador de Contenidos Sonoros": (3, "2C"),
        "Proyecto Integrador en Locución para Plataformas Audiovisuales": (3, "2C"),
        "Doblaje y Locución de Personajes": (3, "2C"),
        "EDI 3": (3, "2C"),
    }
    
    materias_creadas = {}
    for nombre, (anio, cuatri) in materias_data.items():
        m, created = Materia.objects.get_or_create(
            plan=plan,
            nombre=nombre,
            defaults={
                'año_dictado': anio,
                'cuatrimestre_dictado': cuatri
            }
        )
        materias_creadas[nombre] = m

    # Correlatividades (Para Cursar -> Requiere Cursada REG)
    correlatividades_data = [
        ("Locución, Interpretación y Lectura", "Introducción a la Locución"),
        ("Entrenamiento Vocal", "Introducción al Entrenamiento Vocal"),
        ("Locución Artística y Publicitaria", "Locución, Interpretación y Lectura"),
        ("Educación Vocal", "Entrenamiento Vocal"),
        ("Práctica Profesionalizante en Conducción para Televisión", "Práctica Profesionalizante en Locución para Televisión"),
        ("Práctica Profesionalizante en Conducción para Radio", "Práctica Profesionalizante en Locución para Radio"),
        ("Locución Aplicada e Improvisación", "Locución Artística y Publicitaria"),
        ("Técnica Vocal", "Educación Vocal"),
        ("Locución para Medios Digitales", "Locución Aplicada e Improvisación"),
        ("Técnica Vocal Avanzada", "Técnica Vocal"),
        ("Taller Integrador de Locución", "Locución para Medios Digitales"),
        ("Taller Integrador de la Voz", "Técnica Vocal Avanzada"),
        ("Taller Integrador de Contenidos Sonoros", "Práctica Profesionalizante en Podcast y Producción de Contenidos Digitales"),
        ("Taller Integrador de Contenidos Sonoros", "Práctica Profesionalizante en Radio y Streaming"),
        ("Proyecto Integrador en Locución para Plataformas Audiovisuales", "Locución de Contenidos para Medios Audiovisuales"),
        ("Proyecto Integrador en Locución para Plataformas Audiovisuales", "Plataformas Digitales y Nuevas Tendencias Audiovisuales"),
        ("Doblaje y Locución de Personajes", "Técnicas de Doblaje"),
    ]
    
    for materia, requisito in correlatividades_data:
        Correlatividad.objects.get_or_create(
            materia=materias_creadas[materia],
            requisito=materias_creadas[requisito],
            tipo='REG' # Para cursar se necesita cursada (REGULAR)
        )
        
    # Agregando las promociones directas
    promo_directa = [
        "Doblaje y Locución de Personajes", "Entrenamiento Vocal", "Técnica Vocal", "Expresión Corporal",
        "Herramientas de Producción y Edición Digital", "Introducción a la Locución", "Introducción al Entrenamiento Vocal",
        "Locución Aplicada e Improvisación", "Locución Artística y Publicitaria", "Locución de Contenidos para Medios Audiovisuales",
        "Locución, Interpretación y Lectura", "Locución para Medios Digitales", "Plataformas Digitales y Nuevas Tendencias Audiovisuales",
        "Práctica Profesionalizante en Radio y Streaming", "Práctica Profesionalizante en Conducción para Radio",
        "Práctica Profesionalizante en Conducción para Televisión", "Práctica Profesionalizante en Locución para Radio",
        "Práctica Profesionalizante en Locución para Televisión", "Práctica Profesionalizante en Podcast y Producción de Contenidos Digitales",
        "Proyecto Integrador en Locución para Plataformas Audiovisuales", "Taller Integrador de Contenidos Sonoros",
        "Taller Integrador de la Voz", "Taller Integrador de Locución", "Técnica Vocal Avanzada", "Educación Vocal"
    ]
    
    print(f"Total de materias agregadas al plan Locucion 2025: {len(materias_creadas)}")
    print("Correlatividades agregadas exitosamente.")

if __name__ == '__main__':
    run()
