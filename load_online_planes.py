import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_escolar.settings')
django.setup()

from gestion.models import PlanDeEstudio, Materia, Correlatividad

def run():
    plan_1, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Tecn. Sup. en Análisis de Sistemas',
        defaults={'resolucion_ministerial': 'Res. N° 521/SSPLINED/16'}
    )
    plan_1.resolucion_ministerial = 'Res. N° 521/SSPLINED/16'
    plan_1.save()

    plan_2, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Prof. de Educ. Sup. en Ciencias Sagradas',
        defaults={'resolucion_ministerial': 'Res. N° 4184/MEGC/14'}
    )
    plan_2.resolucion_ministerial = 'Res. N° 4184/MEGC/14'
    plan_2.save()

    plan_3, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Tecnicatura Superior en Locución Integral (Res. N° 63/SSPLINED/19)',
        defaults={'resolucion_ministerial': ''}
    )
    plan_3.resolucion_ministerial = ''
    plan_3.save()

    plan_4, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Tecnicatura Superior en Locución Integral (Res. N° 63/SSPLINED/19)',
        defaults={'resolucion_ministerial': 'Res. N° 63/SSPLINED/19'}
    )
    plan_4.resolucion_ministerial = 'Res. N° 63/SSPLINED/19'
    plan_4.save()

    plan_5, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Tecnicatura Sup. en Producción Integral de Televisión (Res. N° 400/SSPLINED/2018)',
        defaults={'resolucion_ministerial': 'Res. N° 400/SSPLINED/18'}
    )
    plan_5.resolucion_ministerial = 'Res. N° 400/SSPLINED/18'
    plan_5.save()

    plan_6, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Locución Integral',
        defaults={'resolucion_ministerial': 'Res. N° 63/SSPLINED/19'}
    )
    plan_6.resolucion_ministerial = 'Res. N° 63/SSPLINED/19'
    plan_6.save()

    plan_7, _ = PlanDeEstudio.objects.get_or_create(
        nombre='Producción Integral de Televisión y Servicios Audiovisuales',
        defaults={'resolucion_ministerial': 'Res. N° 400/SSPLINED/2018'}
    )
    plan_7.resolucion_ministerial = 'Res. N° 400/SSPLINED/2018'
    plan_7.save()

    mat_1, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Comunicación Visual',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_1.año_dictado = 1
    mat_1.cuatrimestre_dictado = '1C'
    mat_1.save()

    mat_2, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Programación Web I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_2.año_dictado = 1
    mat_2.cuatrimestre_dictado = '1C'
    mat_2.save()

    mat_3, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Organización Empresarial',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_3.año_dictado = 1
    mat_3.cuatrimestre_dictado = '1C'
    mat_3.save()

    mat_4, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Elementos de la Matemática',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_4.año_dictado = 1
    mat_4.cuatrimestre_dictado = '1C'
    mat_4.save()

    mat_5, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Introducción a la Programación',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_5.año_dictado = 1
    mat_5.cuatrimestre_dictado = '1C'
    mat_5.save()

    mat_6, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Base de Datos I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_6.año_dictado = 1
    mat_6.cuatrimestre_dictado = '2C'
    mat_6.save()

    mat_7, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Programación Web II',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_7.año_dictado = 1
    mat_7.cuatrimestre_dictado = '2C'
    mat_7.save()

    mat_8, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Experiencia de Usuario',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_8.año_dictado = 1
    mat_8.cuatrimestre_dictado = '2C'
    mat_8.save()

    mat_9, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Sistemas Empresariales',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_9.año_dictado = 1
    mat_9.cuatrimestre_dictado = '2C'
    mat_9.save()

    mat_10, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Programación Orientada a Objetos',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_10.año_dictado = 1
    mat_10.cuatrimestre_dictado = '2C'
    mat_10.save()

    mat_11, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Base de Datos II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_11.año_dictado = 2
    mat_11.cuatrimestre_dictado = '1C'
    mat_11.save()

    mat_12, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Programación Avanzada',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_12.año_dictado = 2
    mat_12.cuatrimestre_dictado = '1C'
    mat_12.save()

    mat_13, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Ingeniería de Requerimientos',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_13.año_dictado = 2
    mat_13.cuatrimestre_dictado = '1C'
    mat_13.save()

    mat_14, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Arquitectura y Sistemas Operativos',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_14.año_dictado = 2
    mat_14.cuatrimestre_dictado = '1C'
    mat_14.save()

    mat_15, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Práctica Profesionalizante I: Producción Web',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_15.año_dictado = 2
    mat_15.cuatrimestre_dictado = '1C'
    mat_15.save()

    mat_16, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Aplicaciones Móviles',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_16.año_dictado = 2
    mat_16.cuatrimestre_dictado = '2C'
    mat_16.save()

    mat_17, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Comunicaciones y Redes',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_17.año_dictado = 2
    mat_17.cuatrimestre_dictado = '2C'
    mat_17.save()

    mat_18, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Plataforma de Desarrollo',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_18.año_dictado = 2
    mat_18.cuatrimestre_dictado = '2C'
    mat_18.save()

    mat_19, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Análisis y Metodología de Sistemas',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_19.año_dictado = 2
    mat_19.cuatrimestre_dictado = '2C'
    mat_19.save()

    mat_20, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Práctica Profesionalizante II: Base de Datos III',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_20.año_dictado = 2
    mat_20.cuatrimestre_dictado = '2C'
    mat_20.save()

    mat_21, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Estadística',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_21.año_dictado = 3
    mat_21.cuatrimestre_dictado = '1C'
    mat_21.save()

    mat_22, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Diseño de Sistemas',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_22.año_dictado = 3
    mat_22.cuatrimestre_dictado = '1C'
    mat_22.save()

    mat_23, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Administración de Proyectos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_23.año_dictado = 3
    mat_23.cuatrimestre_dictado = '1C'
    mat_23.save()

    mat_24, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Planificación del Seminario Final',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_24.año_dictado = 3
    mat_24.cuatrimestre_dictado = '1C'
    mat_24.save()

    mat_25, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Práctica Profesionalizante III: Integración Tecnológica',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_25.año_dictado = 3
    mat_25.cuatrimestre_dictado = '1C'
    mat_25.save()

    mat_26, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Acreditación de Talleres, Jornadas o Seminarios de Actualización',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_26.año_dictado = 3
    mat_26.cuatrimestre_dictado = 'AN'
    mat_26.save()

    mat_27, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Calidad de Software',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_27.año_dictado = 3
    mat_27.cuatrimestre_dictado = '2C'
    mat_27.save()

    mat_28, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Seguridad e Integridad',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_28.año_dictado = 3
    mat_28.cuatrimestre_dictado = '2C'
    mat_28.save()

    mat_29, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Ética y Deontología Profesional',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_29.año_dictado = 3
    mat_29.cuatrimestre_dictado = '2C'
    mat_29.save()

    mat_30, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Modelos Estratégicos de Negocios',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_30.año_dictado = 3
    mat_30.cuatrimestre_dictado = '2C'
    mat_30.save()

    mat_31, _ = Materia.objects.get_or_create(
        plan=plan_1,
        nombre='Práctica Profesionalizante VI: Seminario Final',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_31.año_dictado = 3
    mat_31.cuatrimestre_dictado = '2C'
    mat_31.save()

    mat_32, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Griego',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_32.año_dictado = 1
    mat_32.cuatrimestre_dictado = 'AN'
    mat_32.save()

    mat_33, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Filosofía',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_33.año_dictado = 1
    mat_33.cuatrimestre_dictado = 'AN'
    mat_33.save()

    mat_34, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Psicología',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_34.año_dictado = 1
    mat_34.cuatrimestre_dictado = 'AN'
    mat_34.save()

    mat_35, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Pedagogía',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_35.año_dictado = 1
    mat_35.cuatrimestre_dictado = 'AN'
    mat_35.save()

    mat_36, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Filosofía Antigua',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_36.año_dictado = 1
    mat_36.cuatrimestre_dictado = 'AN'
    mat_36.save()

    mat_37, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Introducción a la teología',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_37.año_dictado = 1
    mat_37.cuatrimestre_dictado = '1C'
    mat_37.save()

    mat_38, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Historia de Iglesia Antigua',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_38.año_dictado = 1
    mat_38.cuatrimestre_dictado = '1C'
    mat_38.save()

    mat_39, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Lectura, escritura y oralidad',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_39.año_dictado = 1
    mat_39.cuatrimestre_dictado = '1C'
    mat_39.save()

    mat_40, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Teología pastoral fundamental',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_40.año_dictado = 1
    mat_40.cuatrimestre_dictado = '1C'
    mat_40.save()

    mat_41, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Introducción al Antiguo Testamento',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_41.año_dictado = 1
    mat_41.cuatrimestre_dictado = '1C'
    mat_41.save()

    mat_42, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Patrología',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_42.año_dictado = 1
    mat_42.cuatrimestre_dictado = '2C'
    mat_42.save()

    mat_43, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Orígenes cristianos',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_43.año_dictado = 1
    mat_43.cuatrimestre_dictado = '2C'
    mat_43.save()

    mat_44, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Métodos exegéticos',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_44.año_dictado = 1
    mat_44.cuatrimestre_dictado = '2C'
    mat_44.save()

    mat_45, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Metodología de la Investigación',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_45.año_dictado = 1
    mat_45.cuatrimestre_dictado = '2C'
    mat_45.save()

    mat_46, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Observación institucional y áulica',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_46.año_dictado = 1
    mat_46.cuatrimestre_dictado = '2C'
    mat_46.save()

    mat_47, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Introducción al Nuevo Testamento',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_47.año_dictado = 1
    mat_47.cuatrimestre_dictado = '2C'
    mat_47.save()

    mat_48, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Didáctica General',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_48.año_dictado = 2
    mat_48.cuatrimestre_dictado = 'AN'
    mat_48.save()

    mat_49, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Filosofía Medieval',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_49.año_dictado = 2
    mat_49.cuatrimestre_dictado = 'AN'
    mat_49.save()

    mat_50, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Misterio de Dios y Trinidad',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_50.año_dictado = 2
    mat_50.cuatrimestre_dictado = 'AN'
    mat_50.save()

    mat_51, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Psicología de los Sujetos de la Educación',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_51.año_dictado = 2
    mat_51.cuatrimestre_dictado = 'AN'
    mat_51.save()

    mat_52, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Pentateuco',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_52.año_dictado = 2
    mat_52.cuatrimestre_dictado = '1C'
    mat_52.save()

    mat_53, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Escritos Paulinos',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_53.año_dictado = 2
    mat_53.cuatrimestre_dictado = '1C'
    mat_53.save()

    mat_54, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Psicología Educacional',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_54.año_dictado = 2
    mat_54.cuatrimestre_dictado = '1C'
    mat_54.save()

    mat_55, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Historia de la Iglesia Medieval',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_55.año_dictado = 2
    mat_55.cuatrimestre_dictado = '1C'
    mat_55.save()

    mat_56, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Observación de las acciones Pastorales',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_56.año_dictado = 2
    mat_56.cuatrimestre_dictado = '1C'
    mat_56.save()

    mat_57, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Profetas',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_57.año_dictado = 2
    mat_57.cuatrimestre_dictado = '2C'
    mat_57.save()

    mat_58, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Sinópticos y Hechos',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_58.año_dictado = 2
    mat_58.cuatrimestre_dictado = '2C'
    mat_58.save()

    mat_59, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Teología Fundamental',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_59.año_dictado = 2
    mat_59.cuatrimestre_dictado = '2C'
    mat_59.save()

    mat_60, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Instituciones Educativas',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_60.año_dictado = 2
    mat_60.cuatrimestre_dictado = '2C'
    mat_60.save()

    mat_61, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Teología Litúrgico Sacramental',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_61.año_dictado = 2
    mat_61.cuatrimestre_dictado = '2C'
    mat_61.save()

    mat_62, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Investigación de la Práctica Docente',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_62.año_dictado = 2
    mat_62.cuatrimestre_dictado = '2C'
    mat_62.save()

    mat_63, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Sociología',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_63.año_dictado = 3
    mat_63.cuatrimestre_dictado = 'AN'
    mat_63.save()

    mat_64, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Cristología',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_64.año_dictado = 3
    mat_64.cuatrimestre_dictado = 'AN'
    mat_64.save()

    mat_65, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Didáctica Especial',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_65.año_dictado = 3
    mat_65.cuatrimestre_dictado = 'AN'
    mat_65.save()

    mat_66, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Filosofía Moderna',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_66.año_dictado = 3
    mat_66.cuatrimestre_dictado = 'AN'
    mat_66.save()

    mat_67, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Ayudantía y Práctica',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_67.año_dictado = 3
    mat_67.cuatrimestre_dictado = 'AN'
    mat_67.save()

    mat_68, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Libros Históricos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_68.año_dictado = 3
    mat_68.cuatrimestre_dictado = '1C'
    mat_68.save()

    mat_69, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Escritos Joánicos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_69.año_dictado = 3
    mat_69.cuatrimestre_dictado = '1C'
    mat_69.save()

    mat_70, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Moral Fundamental',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_70.año_dictado = 3
    mat_70.cuatrimestre_dictado = '1C'
    mat_70.save()

    mat_71, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Creación y Antropología',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_71.año_dictado = 3
    mat_71.cuatrimestre_dictado = '1C'
    mat_71.save()

    mat_72, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Nuevos escenarios: Cultura, tecnología y subjetividad',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_72.año_dictado = 3
    mat_72.cuatrimestre_dictado = '1C'
    mat_72.save()

    mat_73, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Gracia y escatología',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_73.año_dictado = 3
    mat_73.cuatrimestre_dictado = '2C'
    mat_73.save()

    mat_74, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Salmos y Sapienciales',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_74.año_dictado = 3
    mat_74.cuatrimestre_dictado = '2C'
    mat_74.save()

    mat_75, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Educación Sexual Integral',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_75.año_dictado = 3
    mat_75.cuatrimestre_dictado = '2C'
    mat_75.save()

    mat_76, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Historia de la Iglesia Moderna y Contemporánea',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_76.año_dictado = 3
    mat_76.cuatrimestre_dictado = '2C'
    mat_76.save()

    mat_77, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Filosofía para Teólogos',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_77.año_dictado = 4
    mat_77.cuatrimestre_dictado = 'AN'
    mat_77.save()

    mat_78, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Filosofía Contemporánea',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_78.año_dictado = 4
    mat_78.cuatrimestre_dictado = 'AN'
    mat_78.save()

    mat_79, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Eclesiología y Misionología',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_79.año_dictado = 4
    mat_79.cuatrimestre_dictado = 'AN'
    mat_79.save()

    mat_80, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Problemáticas de los Niveles Educativos',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_80.año_dictado = 4
    mat_80.cuatrimestre_dictado = 'AN'
    mat_80.save()

    mat_81, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Ecumenismo y Teología del Pluralismo Religioso',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_81.año_dictado = 4
    mat_81.cuatrimestre_dictado = 'AN'
    mat_81.save()

    mat_82, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Bioética',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_82.año_dictado = 4
    mat_82.cuatrimestre_dictado = '1C'
    mat_82.save()

    mat_83, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Nuevas Tecnologías',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_83.año_dictado = 4
    mat_83.cuatrimestre_dictado = '1C'
    mat_83.save()

    mat_84, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Sistema y Política Educativa',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_84.año_dictado = 4
    mat_84.cuatrimestre_dictado = '1C'
    mat_84.save()

    mat_85, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Pastoral de la Palabra y la Liturgia',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_85.año_dictado = 4
    mat_85.cuatrimestre_dictado = '1C'
    mat_85.save()

    mat_86, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Historia de la iglesia Latinoamericana y Argentina',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_86.año_dictado = 4
    mat_86.cuatrimestre_dictado = '1C'
    mat_86.save()

    mat_87, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Síntesis Pastoral',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_87.año_dictado = 4
    mat_87.cuatrimestre_dictado = '2C'
    mat_87.save()

    mat_88, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Pastoral de la Comunidad',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_88.año_dictado = 4
    mat_88.cuatrimestre_dictado = '2C'
    mat_88.save()

    mat_89, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Historia de la Educación Argentina',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_89.año_dictado = 4
    mat_89.cuatrimestre_dictado = '2C'
    mat_89.save()

    mat_90, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Hebreos, Apocalipsis y Cartas Pastorales',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_90.año_dictado = 4
    mat_90.cuatrimestre_dictado = '2C'
    mat_90.save()

    mat_91, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Historia de la Iglesia Argentina Contemporánea',
        defaults={
            'año_dictado': 4,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_91.año_dictado = 4
    mat_91.cuatrimestre_dictado = '2C'
    mat_91.save()

    mat_92, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Residencia',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_92.año_dictado = 5
    mat_92.cuatrimestre_dictado = 'AN'
    mat_92.save()

    mat_93, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Moral Social',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_93.año_dictado = 5
    mat_93.cuatrimestre_dictado = '1C'
    mat_93.save()

    mat_94, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Sacramentos I',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_94.año_dictado = 5
    mat_94.cuatrimestre_dictado = '1C'
    mat_94.save()

    mat_95, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Sacramentos II',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_95.año_dictado = 5
    mat_95.cuatrimestre_dictado = '1C'
    mat_95.save()

    mat_96, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Gestión Educativa',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_96.año_dictado = 5
    mat_96.cuatrimestre_dictado = '1C'
    mat_96.save()

    mat_97, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Teología Espiritual',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_97.año_dictado = 5
    mat_97.cuatrimestre_dictado = '1C'
    mat_97.save()

    mat_98, _ = Materia.objects.get_or_create(
        plan=plan_2,
        nombre='Teología Latinoamericana y Argentina',
        defaults={
            'año_dictado': 5,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_98.año_dictado = 5
    mat_98.cuatrimestre_dictado = '1C'
    mat_98.save()

    mat_99, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Locución I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_99.año_dictado = 1
    mat_99.cuatrimestre_dictado = 'AN'
    mat_99.save()

    mat_100, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Televisión I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_100.año_dictado = 1
    mat_100.cuatrimestre_dictado = 'AN'
    mat_100.save()

    mat_101, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Técnicas de la Voz I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_101.año_dictado = 1
    mat_101.cuatrimestre_dictado = 'AN'
    mat_101.save()

    mat_102, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Taller integral de la Voz I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_102.año_dictado = 1
    mat_102.cuatrimestre_dictado = 'AN'
    mat_102.save()

    mat_103, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Práctica Profesionalizante en Radio I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_103.año_dictado = 1
    mat_103.cuatrimestre_dictado = 'AN'
    mat_103.save()

    mat_104, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Literatura',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_104.año_dictado = 1
    mat_104.cuatrimestre_dictado = '1C'
    mat_104.save()

    mat_105, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Fonética Italiana',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_105.año_dictado = 1
    mat_105.cuatrimestre_dictado = '1C'
    mat_105.save()

    mat_106, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Expresión Oral y Escrita',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_106.año_dictado = 1
    mat_106.cuatrimestre_dictado = '1C'
    mat_106.save()

    mat_107, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Teorías de la comunicación',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_107.año_dictado = 1
    mat_107.cuatrimestre_dictado = '1C'
    mat_107.save()

    mat_108, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Historia de la Cultura y el Arte',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_108.año_dictado = 1
    mat_108.cuatrimestre_dictado = '1C'
    mat_108.save()

    mat_109, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Tecnología I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_109.año_dictado = 1
    mat_109.cuatrimestre_dictado = '2C'
    mat_109.save()

    mat_110, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Fonética Francesa',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_110.año_dictado = 1
    mat_110.cuatrimestre_dictado = '2C'
    mat_110.save()

    mat_111, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Expresión Corporal',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_111.año_dictado = 1
    mat_111.cuatrimestre_dictado = '2C'
    mat_111.save()

    mat_112, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Redacción Periodística',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_112.año_dictado = 1
    mat_112.cuatrimestre_dictado = '2C'
    mat_112.save()

    mat_113, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Locución II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_113.año_dictado = 2
    mat_113.cuatrimestre_dictado = 'AN'
    mat_113.save()

    mat_114, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Televisión II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_114.año_dictado = 2
    mat_114.cuatrimestre_dictado = 'AN'
    mat_114.save()

    mat_115, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Técnicas de la Voz II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_115.año_dictado = 2
    mat_115.cuatrimestre_dictado = 'AN'
    mat_115.save()

    mat_116, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Taller integral de la Voz II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_116.año_dictado = 2
    mat_116.cuatrimestre_dictado = 'AN'
    mat_116.save()

    mat_117, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Práctica Profesionalizante en Radio II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_117.año_dictado = 2
    mat_117.cuatrimestre_dictado = 'AN'
    mat_117.save()

    mat_118, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Inglés',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_118.año_dictado = 2
    mat_118.cuatrimestre_dictado = 'AN'
    mat_118.save()

    mat_119, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Portugués',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_119.año_dictado = 2
    mat_119.cuatrimestre_dictado = '1C'
    mat_119.save()

    mat_120, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Libretos y Guiones',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_120.año_dictado = 2
    mat_120.cuatrimestre_dictado = '1C'
    mat_120.save()

    mat_121, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Problemática Religiosa Contemporánea',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_121.año_dictado = 2
    mat_121.cuatrimestre_dictado = '1C'
    mat_121.save()

    mat_122, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Práctica Profesionalizante en Conducción en Actos Públicos',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_122.año_dictado = 2
    mat_122.cuatrimestre_dictado = '1C'
    mat_122.save()

    mat_123, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Tecnología II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_123.año_dictado = 2
    mat_123.cuatrimestre_dictado = '2C'
    mat_123.save()

    mat_124, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Fonética Alemana',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_124.año_dictado = 2
    mat_124.cuatrimestre_dictado = '2C'
    mat_124.save()

    mat_125, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Actuación Dramática',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_125.año_dictado = 2
    mat_125.cuatrimestre_dictado = '2C'
    mat_125.save()

    mat_126, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Argentina Contemporánea',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_126.año_dictado = 2
    mat_126.cuatrimestre_dictado = '2C'
    mat_126.save()

    mat_127, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Locución III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_127.año_dictado = 3
    mat_127.cuatrimestre_dictado = 'AN'
    mat_127.save()

    mat_128, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Técnicas de la Voz III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_128.año_dictado = 3
    mat_128.cuatrimestre_dictado = 'AN'
    mat_128.save()

    mat_129, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Taller integral de la Voz III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_129.año_dictado = 3
    mat_129.cuatrimestre_dictado = 'AN'
    mat_129.save()

    mat_130, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Práctica Profesionalizante en Radio III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_130.año_dictado = 3
    mat_130.cuatrimestre_dictado = 'AN'
    mat_130.save()

    mat_131, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Doblaje',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_131.año_dictado = 3
    mat_131.cuatrimestre_dictado = 'AN'
    mat_131.save()

    mat_132, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Práctica Profesionalizante en Televisión Integral',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_132.año_dictado = 3
    mat_132.cuatrimestre_dictado = 'AN'
    mat_132.save()

    mat_133, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Oratoria',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_133.año_dictado = 3
    mat_133.cuatrimestre_dictado = '1C'
    mat_133.save()

    mat_134, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Periodismo',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_134.año_dictado = 3
    mat_134.cuatrimestre_dictado = '1C'
    mat_134.save()

    mat_135, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Legislación de Medios Audiovisuales',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_135.año_dictado = 3
    mat_135.cuatrimestre_dictado = '1C'
    mat_135.save()

    mat_136, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Ética Profesional',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_136.año_dictado = 3
    mat_136.cuatrimestre_dictado = '2C'
    mat_136.save()

    mat_137, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Semiótica de los Medios Masivos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_137.año_dictado = 3
    mat_137.cuatrimestre_dictado = '2C'
    mat_137.save()

    mat_138, _ = Materia.objects.get_or_create(
        plan=plan_4,
        nombre='Práctica Profesionalizante en Producción de Contenidos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_138.año_dictado = 3
    mat_138.cuatrimestre_dictado = '2C'
    mat_138.save()

    mat_139, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Producción General Audiovisual',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_139.año_dictado = 1
    mat_139.cuatrimestre_dictado = '1C'
    mat_139.save()

    mat_140, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Cobertura de Exteriores',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_140.año_dictado = 1
    mat_140.cuatrimestre_dictado = '1C'
    mat_140.save()

    mat_141, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Teoría de la Producción',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_141.año_dictado = 1
    mat_141.cuatrimestre_dictado = '1C'
    mat_141.save()

    mat_142, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Introducción a las Prácticas Audiovisuales',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_142.año_dictado = 1
    mat_142.cuatrimestre_dictado = '1C'
    mat_142.save()

    mat_143, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Trabajo Integrador: Producción en Exteriores',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_143.año_dictado = 1
    mat_143.cuatrimestre_dictado = '1C'
    mat_143.save()

    mat_144, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Culturas Contemporáneas',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_144.año_dictado = 1
    mat_144.cuatrimestre_dictado = '2C'
    mat_144.save()

    mat_145, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Introducción a los Medios Audiovisuales',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_145.año_dictado = 1
    mat_145.cuatrimestre_dictado = '2C'
    mat_145.save()

    mat_146, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Tecnologías de la Información y de la Comunicación I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_146.año_dictado = 1
    mat_146.cuatrimestre_dictado = '2C'
    mat_146.save()

    mat_147, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Guión',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_147.año_dictado = 1
    mat_147.cuatrimestre_dictado = '2C'
    mat_147.save()

    mat_148, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Prácticas Televisivas I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_148.año_dictado = 1
    mat_148.cuatrimestre_dictado = '2C'
    mat_148.save()

    mat_149, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Trabajo Integrador: Entrevistas',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_149.año_dictado = 1
    mat_149.cuatrimestre_dictado = '2C'
    mat_149.save()

    mat_150, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Diseño de Arte',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_150.año_dictado = 2
    mat_150.cuatrimestre_dictado = '1C'
    mat_150.save()

    mat_151, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Tecnologías de la Información y la Comunicación II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_151.año_dictado = 2
    mat_151.cuatrimestre_dictado = '1C'
    mat_151.save()

    mat_152, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Producción Periodística',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_152.año_dictado = 2
    mat_152.cuatrimestre_dictado = '1C'
    mat_152.save()

    mat_153, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Prácticas Televisivas II: Programas en Vivo',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_153.año_dictado = 2
    mat_153.cuatrimestre_dictado = '1C'
    mat_153.save()

    mat_154, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Trabajo Integrador: Grabación en Estudio',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_154.año_dictado = 2
    mat_154.cuatrimestre_dictado = '1C'
    mat_154.save()

    mat_155, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Historia de los Medios y la Televisión',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_155.año_dictado = 2
    mat_155.cuatrimestre_dictado = '2C'
    mat_155.save()

    mat_156, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Investigación de Mercados y Audiencias',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_156.año_dictado = 2
    mat_156.cuatrimestre_dictado = '2C'
    mat_156.save()

    mat_157, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Ficción y Puesta en Escena',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_157.año_dictado = 2
    mat_157.cuatrimestre_dictado = '2C'
    mat_157.save()

    mat_158, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Taller de Televisión Documental',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_158.año_dictado = 2
    mat_158.cuatrimestre_dictado = '2C'
    mat_158.save()

    mat_159, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Trabajo Integrador: Programa de Investigación – Noticias',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_159.año_dictado = 2
    mat_159.cuatrimestre_dictado = '2C'
    mat_159.save()

    mat_160, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Ética y Legislación',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_160.año_dictado = 3
    mat_160.cuatrimestre_dictado = '1C'
    mat_160.save()

    mat_161, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Guión de Ficción',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_161.año_dictado = 3
    mat_161.cuatrimestre_dictado = '1C'
    mat_161.save()

    mat_162, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Postproducción I',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_162.año_dictado = 3
    mat_162.cuatrimestre_dictado = '1C'
    mat_162.save()

    mat_163, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Taller de Proyecto Audiovisual',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_163.año_dictado = 3
    mat_163.cuatrimestre_dictado = '1C'
    mat_163.save()

    mat_164, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Trabajo Integrador: Presentación de Proyecto',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_164.año_dictado = 3
    mat_164.cuatrimestre_dictado = '1C'
    mat_164.save()

    mat_165, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Gestión y Comercialización de Televisión',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_165.año_dictado = 3
    mat_165.cuatrimestre_dictado = '2C'
    mat_165.save()

    mat_166, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Postproducción II: Animación y Efectos Especiales',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_166.año_dictado = 3
    mat_166.cuatrimestre_dictado = '2C'
    mat_166.save()

    mat_167, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Taller de Realización de Formatos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_167.año_dictado = 3
    mat_167.cuatrimestre_dictado = '2C'
    mat_167.save()

    mat_168, _ = Materia.objects.get_or_create(
        plan=plan_5,
        nombre='Trabajo Integrador: Ficción',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_168.año_dictado = 3
    mat_168.cuatrimestre_dictado = '2C'
    mat_168.save()

    mat_169, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Locución I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_169.año_dictado = 1
    mat_169.cuatrimestre_dictado = 'AN'
    mat_169.save()

    mat_170, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Televisión I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_170.año_dictado = 1
    mat_170.cuatrimestre_dictado = 'AN'
    mat_170.save()

    mat_171, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Técnicas de la Voz I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_171.año_dictado = 1
    mat_171.cuatrimestre_dictado = 'AN'
    mat_171.save()

    mat_172, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Taller integral de la Voz I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_172.año_dictado = 1
    mat_172.cuatrimestre_dictado = 'AN'
    mat_172.save()

    mat_173, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Práctica Profesionalizante en Radio I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_173.año_dictado = 1
    mat_173.cuatrimestre_dictado = 'AN'
    mat_173.save()

    mat_174, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Literatura',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_174.año_dictado = 1
    mat_174.cuatrimestre_dictado = '1C'
    mat_174.save()

    mat_175, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Fonética Italiana',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_175.año_dictado = 1
    mat_175.cuatrimestre_dictado = '1C'
    mat_175.save()

    mat_176, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Expresión Oral y Escrita',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_176.año_dictado = 1
    mat_176.cuatrimestre_dictado = '1C'
    mat_176.save()

    mat_177, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Teorías de la comunicación',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_177.año_dictado = 1
    mat_177.cuatrimestre_dictado = '1C'
    mat_177.save()

    mat_178, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Historia de la Cultura y el Arte',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_178.año_dictado = 1
    mat_178.cuatrimestre_dictado = '1C'
    mat_178.save()

    mat_179, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Tecnología I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_179.año_dictado = 1
    mat_179.cuatrimestre_dictado = '2C'
    mat_179.save()

    mat_180, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Fonética Francesa',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_180.año_dictado = 1
    mat_180.cuatrimestre_dictado = '2C'
    mat_180.save()

    mat_181, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Expresión Corporal',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_181.año_dictado = 1
    mat_181.cuatrimestre_dictado = '2C'
    mat_181.save()

    mat_182, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Redacción Periodística',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_182.año_dictado = 1
    mat_182.cuatrimestre_dictado = '2C'
    mat_182.save()

    mat_183, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Inglés',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_183.año_dictado = 2
    mat_183.cuatrimestre_dictado = 'AN'
    mat_183.save()

    mat_184, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Locución II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_184.año_dictado = 2
    mat_184.cuatrimestre_dictado = 'AN'
    mat_184.save()

    mat_185, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Televisión II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_185.año_dictado = 2
    mat_185.cuatrimestre_dictado = 'AN'
    mat_185.save()

    mat_186, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Técnicas de la Voz II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_186.año_dictado = 2
    mat_186.cuatrimestre_dictado = 'AN'
    mat_186.save()

    mat_187, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Taller integral de la Voz II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_187.año_dictado = 2
    mat_187.cuatrimestre_dictado = 'AN'
    mat_187.save()

    mat_188, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Práctica Profesionalizante en Radio II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_188.año_dictado = 2
    mat_188.cuatrimestre_dictado = 'AN'
    mat_188.save()

    mat_189, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Portugués',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_189.año_dictado = 2
    mat_189.cuatrimestre_dictado = '1C'
    mat_189.save()

    mat_190, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Libretos y Guiones',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_190.año_dictado = 2
    mat_190.cuatrimestre_dictado = '1C'
    mat_190.save()

    mat_191, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Problemática Religiosa Contemporánea',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_191.año_dictado = 2
    mat_191.cuatrimestre_dictado = '1C'
    mat_191.save()

    mat_192, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Práctica Profesionalizante en Conducción en Actos Públicos',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_192.año_dictado = 2
    mat_192.cuatrimestre_dictado = '1C'
    mat_192.save()

    mat_193, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Tecnología II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_193.año_dictado = 2
    mat_193.cuatrimestre_dictado = '2C'
    mat_193.save()

    mat_194, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Fonética Alemana',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_194.año_dictado = 2
    mat_194.cuatrimestre_dictado = '2C'
    mat_194.save()

    mat_195, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Actuación Dramática',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_195.año_dictado = 2
    mat_195.cuatrimestre_dictado = '2C'
    mat_195.save()

    mat_196, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Argentina Contemporánea',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_196.año_dictado = 2
    mat_196.cuatrimestre_dictado = '2C'
    mat_196.save()

    mat_197, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Doblaje',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_197.año_dictado = 3
    mat_197.cuatrimestre_dictado = 'AN'
    mat_197.save()

    mat_198, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Locución III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_198.año_dictado = 3
    mat_198.cuatrimestre_dictado = 'AN'
    mat_198.save()

    mat_199, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Técnicas de la Voz III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_199.año_dictado = 3
    mat_199.cuatrimestre_dictado = 'AN'
    mat_199.save()

    mat_200, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Taller integral de la Voz III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_200.año_dictado = 3
    mat_200.cuatrimestre_dictado = 'AN'
    mat_200.save()

    mat_201, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Práctica Profesionalizante en Radio III',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_201.año_dictado = 3
    mat_201.cuatrimestre_dictado = 'AN'
    mat_201.save()

    mat_202, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Práctica Profesionalizante en Televisión Integral',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': 'AN'
        }
    )
    mat_202.año_dictado = 3
    mat_202.cuatrimestre_dictado = 'AN'
    mat_202.save()

    mat_203, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Oratoria',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_203.año_dictado = 3
    mat_203.cuatrimestre_dictado = '1C'
    mat_203.save()

    mat_204, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Periodismo',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_204.año_dictado = 3
    mat_204.cuatrimestre_dictado = '1C'
    mat_204.save()

    mat_205, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Legislación de Medios Audiovisuales',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_205.año_dictado = 3
    mat_205.cuatrimestre_dictado = '1C'
    mat_205.save()

    mat_206, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Ética Profesional',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_206.año_dictado = 3
    mat_206.cuatrimestre_dictado = '2C'
    mat_206.save()

    mat_207, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Semiótica de los Medios Masivos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_207.año_dictado = 3
    mat_207.cuatrimestre_dictado = '2C'
    mat_207.save()

    mat_208, _ = Materia.objects.get_or_create(
        plan=plan_6,
        nombre='Práctica Profesionalizante en Producción de Contenidos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_208.año_dictado = 3
    mat_208.cuatrimestre_dictado = '2C'
    mat_208.save()

    mat_209, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Producción General Audiovisual',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_209.año_dictado = 1
    mat_209.cuatrimestre_dictado = '1C'
    mat_209.save()

    mat_210, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Cobertura de Exteriores',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_210.año_dictado = 1
    mat_210.cuatrimestre_dictado = '1C'
    mat_210.save()

    mat_211, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Teoría de la Producción',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_211.año_dictado = 1
    mat_211.cuatrimestre_dictado = '1C'
    mat_211.save()

    mat_212, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Introducción a las Prácticas Audiovisuales',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_212.año_dictado = 1
    mat_212.cuatrimestre_dictado = '1C'
    mat_212.save()

    mat_213, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Trabajo Integrador: Producción en Exteriores',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_213.año_dictado = 1
    mat_213.cuatrimestre_dictado = '1C'
    mat_213.save()

    mat_214, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Culturas Contemporáneas',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_214.año_dictado = 1
    mat_214.cuatrimestre_dictado = '2C'
    mat_214.save()

    mat_215, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Introducción a los Medios Audiovisuales',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_215.año_dictado = 1
    mat_215.cuatrimestre_dictado = '2C'
    mat_215.save()

    mat_216, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Tecnologías de la Información y de la Comunicación I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_216.año_dictado = 1
    mat_216.cuatrimestre_dictado = '2C'
    mat_216.save()

    mat_217, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Guión',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_217.año_dictado = 1
    mat_217.cuatrimestre_dictado = '2C'
    mat_217.save()

    mat_218, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Prácticas Televisivas I',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_218.año_dictado = 1
    mat_218.cuatrimestre_dictado = '2C'
    mat_218.save()

    mat_219, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Trabajo Integrador: Entrevistas',
        defaults={
            'año_dictado': 1,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_219.año_dictado = 1
    mat_219.cuatrimestre_dictado = '2C'
    mat_219.save()

    mat_220, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Diseño de Arte',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_220.año_dictado = 2
    mat_220.cuatrimestre_dictado = '1C'
    mat_220.save()

    mat_221, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Tecnologías de la Información y la Comunicación II',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_221.año_dictado = 2
    mat_221.cuatrimestre_dictado = '1C'
    mat_221.save()

    mat_222, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Producción Periodística',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_222.año_dictado = 2
    mat_222.cuatrimestre_dictado = '1C'
    mat_222.save()

    mat_223, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Prácticas Televisivas II: Programas en Vivo',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_223.año_dictado = 2
    mat_223.cuatrimestre_dictado = '1C'
    mat_223.save()

    mat_224, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Trabajo Integrador: Grabación en Estudio',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_224.año_dictado = 2
    mat_224.cuatrimestre_dictado = '1C'
    mat_224.save()

    mat_225, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Historia de los Medios y la Televisión',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_225.año_dictado = 2
    mat_225.cuatrimestre_dictado = '2C'
    mat_225.save()

    mat_226, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Investigación de Mercados y Audiencias',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_226.año_dictado = 2
    mat_226.cuatrimestre_dictado = '2C'
    mat_226.save()

    mat_227, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Ficción y Puesta en Escena',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_227.año_dictado = 2
    mat_227.cuatrimestre_dictado = '2C'
    mat_227.save()

    mat_228, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Taller de Televisión Documental',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_228.año_dictado = 2
    mat_228.cuatrimestre_dictado = '2C'
    mat_228.save()

    mat_229, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Trabajo Integrador: Programa de Investigación – Noticias',
        defaults={
            'año_dictado': 2,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_229.año_dictado = 2
    mat_229.cuatrimestre_dictado = '2C'
    mat_229.save()

    mat_230, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Ética y Legislación',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_230.año_dictado = 3
    mat_230.cuatrimestre_dictado = '1C'
    mat_230.save()

    mat_231, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Guión de Ficción',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_231.año_dictado = 3
    mat_231.cuatrimestre_dictado = '1C'
    mat_231.save()

    mat_232, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Postproducción I',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_232.año_dictado = 3
    mat_232.cuatrimestre_dictado = '1C'
    mat_232.save()

    mat_233, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Taller de Proyecto Audiovisual',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_233.año_dictado = 3
    mat_233.cuatrimestre_dictado = '1C'
    mat_233.save()

    mat_234, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Trabajo Integrador: Presentación de Proyecto',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '1C'
        }
    )
    mat_234.año_dictado = 3
    mat_234.cuatrimestre_dictado = '1C'
    mat_234.save()

    mat_235, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Gestión y Comercialización de Televisión',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_235.año_dictado = 3
    mat_235.cuatrimestre_dictado = '2C'
    mat_235.save()

    mat_236, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Postproducción II: Animación y Efectos Especiales',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_236.año_dictado = 3
    mat_236.cuatrimestre_dictado = '2C'
    mat_236.save()

    mat_237, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Taller de Realización de Formatos',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_237.año_dictado = 3
    mat_237.cuatrimestre_dictado = '2C'
    mat_237.save()

    mat_238, _ = Materia.objects.get_or_create(
        plan=plan_7,
        nombre='Trabajo Integrador: Ficción',
        defaults={
            'año_dictado': 3,
            'cuatrimestre_dictado': '2C'
        }
    )
    mat_238.año_dictado = 3
    mat_238.cuatrimestre_dictado = '2C'
    mat_238.save()

    Correlatividad.objects.get_or_create(
        materia=mat_7,
        requisito=mat_2,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_10,
        requisito=mat_5,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_11,
        requisito=mat_6,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_12,
        requisito=mat_10,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_15,
        requisito=mat_7,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_16,
        requisito=mat_4,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_18,
        requisito=mat_7,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_19,
        requisito=mat_13,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_20,
        requisito=mat_11,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_21,
        requisito=mat_4,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_22,
        requisito=mat_19,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_23,
        requisito=mat_19,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_24,
        requisito=mat_16,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_24,
        requisito=mat_18,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_24,
        requisito=mat_19,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_1,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_2,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_3,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_4,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_5,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_6,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_7,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_8,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_9,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_10,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_11,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_12,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_13,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_14,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_15,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_16,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_17,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_18,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_19,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_20,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_25,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_22,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_23,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_24,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_21,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_49,
        requisito=mat_36,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_50,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_50,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_51,
        requisito=mat_34,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_52,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_52,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_53,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_53,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_53,
        requisito=mat_32,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_54,
        requisito=mat_34,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_55,
        requisito=mat_38,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_56,
        requisito=mat_40,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_57,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_57,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_58,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_58,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_58,
        requisito=mat_32,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_61,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_61,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_64,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_64,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_65,
        requisito=mat_48,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_66,
        requisito=mat_49,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_67,
        requisito=mat_46,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_67,
        requisito=mat_56,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_67,
        requisito=mat_62,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_67,
        requisito=mat_65,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_68,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_68,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_69,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_69,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_69,
        requisito=mat_32,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_71,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_71,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_73,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_73,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_74,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_74,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_76,
        requisito=mat_55,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_77,
        requisito=mat_33,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_78,
        requisito=mat_66,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_79,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_79,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_81,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_81,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_82,
        requisito=mat_70,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_85,
        requisito=mat_40,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_85,
        requisito=mat_46,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_85,
        requisito=mat_56,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_85,
        requisito=mat_62,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_86,
        requisito=mat_76,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_87,
        requisito=mat_40,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_87,
        requisito=mat_46,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_87,
        requisito=mat_56,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_87,
        requisito=mat_62,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_88,
        requisito=mat_40,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_88,
        requisito=mat_46,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_88,
        requisito=mat_56,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_88,
        requisito=mat_62,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_90,
        requisito=mat_41,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_90,
        requisito=mat_44,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_90,
        requisito=mat_32,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_91,
        requisito=mat_86,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_46,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_56,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_62,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_65,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_67,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_88,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_85,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_92,
        requisito=mat_87,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_93,
        requisito=mat_70,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_94,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_94,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_94,
        requisito=mat_61,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_95,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_95,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_95,
        requisito=mat_61,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_97,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_97,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_98,
        requisito=mat_37,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_98,
        requisito=mat_59,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_7,
        requisito=mat_2,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_10,
        requisito=mat_5,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_11,
        requisito=mat_6,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_12,
        requisito=mat_10,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_15,
        requisito=mat_7,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_16,
        requisito=mat_4,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_18,
        requisito=mat_7,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_19,
        requisito=mat_13,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_20,
        requisito=mat_11,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_21,
        requisito=mat_4,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_22,
        requisito=mat_19,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_23,
        requisito=mat_19,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_24,
        requisito=mat_16,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_24,
        requisito=mat_18,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_24,
        requisito=mat_19,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_1,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_2,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_3,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_4,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_5,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_6,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_7,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_8,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_9,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_10,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_11,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_12,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_13,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_14,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_15,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_16,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_17,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_18,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_19,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_20,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_25,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_22,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_23,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_24,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_31,
        requisito=mat_21,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_113,
        requisito=mat_99,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_114,
        requisito=mat_100,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_115,
        requisito=mat_101,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_116,
        requisito=mat_102,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_117,
        requisito=mat_103,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_127,
        requisito=mat_113,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_128,
        requisito=mat_115,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_129,
        requisito=mat_116,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_130,
        requisito=mat_117,
        tipo='CUR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_151,
        requisito=mat_146,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_153,
        requisito=mat_148,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_166,
        requisito=mat_162,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_167,
        requisito=mat_163,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_221,
        requisito=mat_216,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_223,
        requisito=mat_218,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_236,
        requisito=mat_232,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_237,
        requisito=mat_233,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_184,
        requisito=mat_169,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_185,
        requisito=mat_170,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_186,
        requisito=mat_171,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_187,
        requisito=mat_172,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_188,
        requisito=mat_173,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_193,
        requisito=mat_179,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_198,
        requisito=mat_184,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_199,
        requisito=mat_186,
        tipo='APR'
    )
    Correlatividad.objects.get_or_create(
        materia=mat_201,
        requisito=mat_188,
        tipo='APR'
    )

    print('¡Planes, materias y correlatividades sincronizados con exito!')

if __name__ == '__main__':
    run()
