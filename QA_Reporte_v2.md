# Reporte de QA v2 - Sistema SiGeEt (Actualización de Calificaciones y Estados)

## Resumen Ejecutivo
Se ha realizado una nueva auditoría del código tras los cambios en la lógica de calificaciones, reglas de recuperatorio y bloqueos de UI. Se encontraron vulnerabilidades de validación en el backend, errores matemáticos críticos en el cálculo de promedios, y problemas graves de rendimiento (N+1 Queries) introducidos en las recientes modificaciones de `views.py`.

---

### 1. Falla Crítica en Lógica de Negocio: Cálculo de Promedios Roto
* **Vista:** `cargar_notas`
* **Descripción:** El cálculo del promedio final suma **todas** las notas y las divide por la cantidad total de notas `sum(...) / todas_las_notas.count()`. Esto incluye los exámenes desaprobados originales y las notas de "Concepto" o "Trabajos Prácticos". 
* **Caso Límite Fallido (Falso Libre):** Si un alumno saca 2 en el 1er Parcial, 4 en el 2do Parcial y 4 en el Recuperatorio, la suma es 10 y se divide por 3 notas. El promedio es `3.33`. Como es menor a 4, el sistema lo marca como Libre (`LIB`), a pesar de haber aprobado su recuperatorio.
* **Caso Límite Fallido (Falsa Promoción):** Si un alumno no asiste a los parciales pero recibe una nota de "Concepto" de 8, su promedio será 8/1 = 8, logrando la Promoción Directa (`PROM`) sin rendir parciales. Asimismo, una nota de concepto de 6 puede quitarle la promoción a un alumno con todo aprobado con 8.
* **Solución Sugerida:** El cálculo del promedio debe excluir o reemplazar las notas desaprobadas si hay un recuperatorio aprobado, y debe ponderar únicamente las instancias de tipo "Parcial" y "Recuperatorio".

### 2. Bypass de Seguridad (Falta de Validación Backend)
* **Vista:** `cargar_notas`
* **Descripción:** Las reglas que bloquean la carga de "Recuperatorios" si el alumno tiene > 1 aplazo o no tiene aplazos se aplican **únicamente en el frontend** a través de JavaScript y el atributo `disabled`.
* **Vulnerabilidad:** Un atacante (o un docente con conocimientos técnicos) puede inspeccionar el DOM, remover el atributo `disabled`, y enviar un `POST` con una nota de Recuperatorio para cualquier alumno. El backend ciegamente ejecuta `Nota.objects.create(...)` sin validar si el alumno cumplía las condiciones.

### 3. Errores de Estado de QuerySets (N+1 Queries Massivos)
* **Vista:** `cargar_notas` y `Inscripcion.faltas_acumuladas()`
* **Problema A:** En la línea 1009 se ignora el caché introduciendo `todas_las_notas = Nota.objects.filter(inscripcion=insc)` dentro de un bucle `for`, lo que dispara una consulta a la base de datos por cada alumno al cerrar la cursada (N consultas).
* **Problema B:** La función `faltas_acumuladas()` en `models.py` utiliza `self.alumno.asistencias.filter(...)`. Los métodos `.filter()` sobre relaciones ignoran el `prefetch_related`. Al llamar a esta función dentro de los bucles en `cargar_notas` para calcular el estado UI y el estado de cierre, se disparan **decenas o cientos de queries redundantes**.
* **Solución Sugerida:** Mapear en memoria las asistencias prefetcheadas usando `[r for r in self.alumno.asistencias.all() if r.planilla.comision_id == self.comision_id]` y evitar `.filter()` en bucles.

### 4. Error 500 por Tipado Estricto de Enteros (Integer Constraint)
* **Vista:** `cargar_notas`
* **Descripción:** El campo `valor_nota` en el modelo `Nota` fue migrado a `IntegerField`. Sin embargo, en `views.py` no hay validación ni casteo (solo se valida `if nota_valor:`). 
* **Impacto:** Si por error o manipulación se envía un valor decimal en la petición POST (ej. `nota_123=7.5`), el intento de crear la instancia `Nota.objects.create(valor_nota="7.5")` arrojará un `ValueError` no capturado, rompiendo la aplicación con un Error 500 y perdiendo todo el progreso de carga de notas del docente.

### 5. Falla Lógica con Excepciones de Cero (ZeroDivisionError)
* **Vista:** `cargar_notas`
* **Descripción:** Si el docente marca la opción "Cerrar Cursada" con la "Nota Final", pero no le ha cargado ninguna nota en toda la cursada a un alumno ausente, el bloque `else` calculará `promedio = sum(...) / todas_las_notas.count()`. Como `count()` es 0, la aplicación arrojará un `ZeroDivisionError` y devolverá un Error 500 general. El chequeo `if todas_las_notas.exists():` en la línea 1010 previene esto *solo* si el alumno no tiene notas, pero el código es muy frágil ante cambios.

---
**Conclusión:** Se recomienda suspender el pase a producción de este módulo hasta reparar la lógica de promedio ponderado, mover las validaciones del Recuperatorio al backend e implementar manejo de excepciones (try/except) sobre la coerción de tipos.
