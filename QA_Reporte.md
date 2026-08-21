# Reporte de QA - Sistema SiGeEt

## Resumen Ejecutivo
Se ha realizado un análisis exhaustivo enfocado en los módulos de inscripción, estados de alumnos y manejo de permisos del sistema escolar "SiGeEt". Se han detectado fallas críticas de seguridad (Escalada de Privilegios/IDOR), errores en la lógica de negocio y problemas de experiencia/roles. A continuación, se detallan los hallazgos para su pronta corrección.

---

### 1. Vulnerabilidad Crítica: Falta de Validación de Roles (IDOR)
Las vistas orientadas a bedeles y administrativos para la inscripción manual no validan que el usuario solicitante posea privilegios administrativos (`request.user.is_staff`). 
* **Rutas afectadas:** `inscribir_alumno_comision` e `inscribir_alumno_mesa`
* **Impacto:** Cualquier usuario autenticado en el sistema (incluyendo un alumno estándar) que conozca o adivine la URL (ej. `/comisiones/inscribir/<id>`) puede enviar una petición POST y realizar inscripciones masivas a cualquier comisión o mesa de final, salteándose todas las restricciones académicas.

### 2. Evasión de Correlatividades de Cursada
* **Vista afectada:** `alumno_inscripcion_cursada`
* **Descripción:** El algoritmo evalúa si un alumno cumple con las correlatividades (`cumple_correlativas`) únicamente con el propósito de mostrar u ocultar el botón en el Frontend (HTML). En el bloque de código que procesa la inscripción real (petición `POST`), **no se vuelve a realizar esta validación**. 
* **Impacto:** Un alumno con conocimientos mínimos técnicos puede modificar el DOM del navegador (habilitar el botón deshabilitado) o enviar el `POST` mediante herramientas externas e inscribirse a materias de años superiores sin haber rendido las anteriores.

### 3. Filtros Inexistentes para "Estados de Alumno"
* **Vistas afectadas:** `alumno_inscripcion_cursada` y `alumno_inscripcion_finales`
* **Descripción:** Se constató que no existe ninguna validación respecto al campo `estado_alumno` al momento de la autogestión de inscripciones.
* **Impacto:** Un alumno con estado `INA` (Inactivo/Abandonó) o `COND_PAG` (Deudor) puede acceder al sistema (ya que su usuario sigue activo) y continuar inscribiéndose en comisiones y finales como si fuera un alumno regular, volviendo inútil el control de morosidad.

### 4. Bloqueo de Perfil por Bifurcación en Dashboard
* **Vista afectada:** `dashboard`
* **Descripción:** La lógica de la pantalla de inicio bifurca la navegación utilizando verificaciones `hasattr` estrictas: si existe `perfil_alumno` va a su panel, si existe `perfil_docente` va a su panel, y como última opción muestra el panel de administración.
* **Impacto:** Si un perfil de Dirección/Administrador (`is_superuser`) es también cargado como Docente en el sistema (escenario muy habitual), el algoritmo lo atrapará indefinidamente en `dashboard_docente.html`, y el administrador **perderá por completo el acceso a los gráficos y atajos administrativos** de la pantalla de inicio principal.

### 5. Errores Graves de Base de Datos (Error 500)
* **Vista afectada:** `inscribir_alumno_comision`
* **Descripción:** Al asignar los alumnos, se itera sobre una lista enviando directamente `Inscripcion.objects.create(...)`. El modelo `Inscripcion` cuenta con una restricción a nivel base de datos (`unique_together = ['alumno', 'comision']`).
* **Impacto:** Si por concurrencia, doble click, o recarga de página el usuario intenta inscribir a un alumno ya asignado, el ORM lanzará un `IntegrityError` y la página devolverá un **Error 500 (Server Error)** a los administrativos en lugar de un mensaje amigable. Debe reemplazarse por `get_or_create`.

### 6. Omisión de Decorador en Panel Contable
* **Vista afectada:** `panel_contable`
* **Descripción:** Si bien internamente se validan los permisos de los grupos (`Contable`, `Secretaría`, etc.), se omitió incluir el decorador `@login_required` arriba de la vista.
* **Impacto:** Usuarios anónimos o no logueados que intenten acceder al panel serán rebotados incorrectamente, en lugar de ser redirigidos de forma fluida a la pantalla de inicio de sesión (`/accounts/login/`).

---

### Tareas Preventivas Realizadas
Se generó el archivo `gestion/tests.py` incorporando un bloque de tests automatizados (`InscripcionCursadaTest`) para evidenciar y reproducir estos fallos (Prueba de evasión de correlativas y prueba de inscripción de alumno Inactivo). Al ejecutar los tests, los mismos **fallarán**, comprobando así la existencia de los bugs para que los desarrolladores puedan repararlos.
