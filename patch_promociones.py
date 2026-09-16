import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import Materia

def patch():
    # Produccion (ID 5)
    print("Seteando plan Produccion como PROMOCIONABLE...")
    Materia.objects.filter(plan__nombre__icontains="Producc").update(tipo_aprobacion='PROM')
    
    # Sistemas (ID 1)
    print("Seteando plan Sistemas como FINAL OBLIGATORIO...")
    Materia.objects.filter(plan__nombre__icontains="Sistemas").update(tipo_aprobacion='FIN')
    
    # Locución (2025) - ID 8 (or whichever it is now)
    print("Seteando plan Locución según PDF...")
    promo_directa_locucion = [
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
    
    Materia.objects.filter(plan__nombre__icontains="Locución", nombre__in=promo_directa_locucion).update(tipo_aprobacion='PROM')
    Materia.objects.filter(plan__nombre__icontains="Locución").exclude(nombre__in=promo_directa_locucion).update(tipo_aprobacion='FIN')

    print("¡Listo!")

if __name__ == '__main__':
    patch()
