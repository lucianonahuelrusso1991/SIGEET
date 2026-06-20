from django.contrib import admin
from django.urls import path, include
from gestion.views import (
    dashboard, lista_alumnos, legajo_alumno, alta_alumno, editar_alumno, constancia_alumno, boletin_alumno,
    lista_docentes, alta_docente, legajo_docente, editar_docente,
    lista_comisiones, alta_comision, detalle_comision, apertura_masiva,
    inscribir_alumno_comision, toggle_inscripcion_comision, cerrar_comision, eliminar_comision, editar_comision,
    lista_comisiones_asistencia, cargar_asistencia,
    cargar_notas, eliminar_nota,
    detalle_plan, api_chatbot, calendario_general, calendario_alumno, calendario_docente,
    alta_evento_calendario,
    imprimir_lista_asistencia, acta_volante,
    lista_mesas, alta_mesa, detalle_mesa, eliminar_mesa,
    inscribir_alumno_mesa, cargar_notas_mesa, cerrar_mesa,
    acta_examen,
    alta_equivalencia, analitico_alumno,
    redactar_comunicado, mis_notificaciones, leer_notificacion,
    resetear_password_alumno, perfil_alumno, libro_matriz_alumno, alumno_inscripcion_cursada,
    alumno_inscripcion_finales, subir_justificativo, revisar_justificativos
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('', dashboard, name='dashboard'),
    
    # Docentes (Deprecated block, kept to avoid routing errors but the real one is below)
    path('docentes/', lista_docentes, name='lista_docentes'),
    path('docentes/nuevo/', alta_docente, name='alta_docente'),
    
    # Alumnos
    path('alumnos/', lista_alumnos, name='lista_alumnos'),
    path('alumnos/nuevo/', alta_alumno, name='alta_alumno'),
    path('alumnos/<int:alumno_id>/', legajo_alumno, name='legajo_alumno'),
    path('alumnos/<int:alumno_id>/equivalencias/nueva/', alta_equivalencia, name='alta_equivalencia'),
    path('alumnos/<int:alumno_id>/analitico/', analitico_alumno, name='analitico_alumno'),

    path('alumnos/<int:alumno_id>/editar/', editar_alumno, name='editar_alumno'), 
    path('alumnos/<int:alumno_id>/reset-password/', resetear_password_alumno, name='resetear_password_alumno'),
    path('alumnos/<int:alumno_id>/constancia/', constancia_alumno, name='constancia_alumno'),
    path('alumnos/<int:alumno_id>/boletin/<int:ciclo_lectivo>/', boletin_alumno, name='boletin_alumno'),
    path('alumnos/<int:alumno_id>/calendario/', calendario_alumno, name='calendario_alumno'),
    path('mi-perfil/', perfil_alumno, name='perfil_alumno'),
    path('mi-libro-matriz/', libro_matriz_alumno, name='libro_matriz_alumno'),
    path('mi-inscripcion-cursadas/', alumno_inscripcion_cursada, name='alumno_inscripcion_cursada'),
    path('mi-inscripcion-finales/', alumno_inscripcion_finales, name='alumno_inscripcion_finales'),

    # DOCENTES
    path('docentes/', lista_docentes, name='lista_docentes'),
    path('docentes/nuevo/', alta_docente, name='alta_docente'),
    path('docentes/<int:docente_id>/', legajo_docente, name='legajo_docente'),
    path('docentes/<int:docente_id>/editar/', editar_docente, name='editar_docente'),
    path('docentes/<int:docente_id>/calendario/', calendario_docente, name='calendario_docente'),

    # ACADÉMICA / COMISIONES
    path('comisiones/', lista_comisiones, name='lista_comisiones'),
    path('comisiones/nueva/', alta_comision, name='alta_comision'),
    path('comisiones/apertura-masiva/', apertura_masiva, name='apertura_masiva'),
    path('comisiones/<int:comision_id>/', detalle_comision, name='detalle_comision'),
    path('comisiones/<int:comision_id>/editar/', editar_comision, name='editar_comision'),
    path('comisiones/<int:comision_id>/toggle-inscripcion/', toggle_inscripcion_comision, name='toggle_inscripcion_comision'),
    path('comisiones/<int:comision_id>/cerrar/', cerrar_comision, name='cerrar_comision'),
    path('comisiones/<int:comision_id>/eliminar/', eliminar_comision, name='eliminar_comision'),
    path('comisiones/<int:comision_id>/acta-volante/', acta_volante, name='acta_volante'),
    path('comisiones/<int:comision_id>/inscribir/', inscribir_alumno_comision, name='inscribir_alumno_comision'),
    
    # GESTIÓN DIARIA (ASISTENCIA Y NOTAS)
    path('asistencia/', lista_comisiones_asistencia, name='lista_comisiones_asistencia'),
    path('asistencia/<int:comision_id>/', cargar_asistencia, name='cargar_asistencia'),
    path('comisiones/<int:comision_id>/notas/', cargar_notas, name='cargar_notas'),
    path('notas/<int:nota_id>/eliminar/', eliminar_nota, name='eliminar_nota'),
    
    # CALENDARIO GLOBAL
    path('calendario/', calendario_general, name='calendario_general'),
    path('calendario/nuevo-evento/', alta_evento_calendario, name='alta_evento_calendario'),
    path('comisiones/<int:comision_id>/lista-asistencia/', imprimir_lista_asistencia, name='imprimir_lista_asistencia'),

    # PLANES DE ESTUDIO
    path('academica/planes/<int:plan_id>/', detalle_plan, name='detalle_plan'),

    # CALENDARIO GENERAL
    # (Ya incluido en bloque anterior)

    # MÓDULO DE IA
    path('api/chatbot/', api_chatbot, name='api_chatbot'),

    # MESAS DE EXAMEN (FINALES)
    path('mesas/', lista_mesas, name='lista_mesas'),
    path('mesas/nueva/', alta_mesa, name='alta_mesa'),
    path('mesas/<int:mesa_id>/', detalle_mesa, name='detalle_mesa'),
    path('mesas/<int:mesa_id>/eliminar/', eliminar_mesa, name='eliminar_mesa'),
    path('mesas/<int:mesa_id>/inscribir/', inscribir_alumno_mesa, name='inscribir_alumno_mesa'),
    path('mesas/<int:mesa_id>/notas/', cargar_notas_mesa, name='cargar_notas_mesa'),
    path('mesas/<int:mesa_id>/cerrar/', cerrar_mesa, name='cerrar_mesa'),
    path('mesas/<int:mesa_id>/acta/', acta_examen, name='acta_examen'),

    # COMUNICACIONES Y NOTIFICACIONES
    path('comunicaciones/redactar/', redactar_comunicado, name='redactar_comunicado'),
    path('comunicaciones/inbox/', mis_notificaciones, name='mis_notificaciones'),
    path('comunicaciones/leer/<int:notificacion_id>/', leer_notificacion, name='leer_notificacion'),
    
    # JUSTIFICATIVOS DE ASISTENCIA
    path('mi-asistencia/subir-justificativo/', subir_justificativo, name='subir_justificativo'),
    path('bedelia/revisar-justificativos/', revisar_justificativos, name='revisar_justificativos'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)