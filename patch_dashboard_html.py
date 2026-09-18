import codecs
import re

with codecs.open('gestion/templates/gestion/alumnos/dashboard_alumno.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<!-- Autogestin y Trǭmites -->.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>'

new_tramites = '''<!-- Autogestión y Trámites -->
        <div class="col-md-12 fade-in-up" style="animation-delay: 0.5s;">
            <div class="card shadow-sm border-0 rounded-4">
                <div class="card-header bg-body-tertiary border-bottom p-4">
                    <h5 class="mb-0 fw-bold"><i class="bi bi-person-badge me-2"></i>Trámites y Autogestión</h5>
                </div>
                <div class="card-body p-4">
                    <div class="row g-3">
                        <div class="col-md-6 col-lg-3">
                            <div class="d-flex flex-column align-items-center p-4 bg-light rounded-3 text-center h-100 hover-lift">
                                <i class="bi bi-file-earmark-pdf-fill text-danger fs-1 mb-2"></i>
                                <h6 class="fw-bold mb-1">Certificado Regular</h6>
                                <p class="text-muted small mb-3">Solicitá tu constancia oficial.</p>
                                <form method="post" action="{% url 'solicitar_tramite_alumno' %}">
                                    {% csrf_token %}
                                    <input type="hidden" name="tipo_tramite" value="REGULAR">
                                    <button type="submit" class="btn btn-sm btn-dark fw-bold rounded-pill px-4 mt-auto">Solicitar</button>
                                </form>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-3">
                            <div class="d-flex flex-column align-items-center p-4 bg-light rounded-3 text-center h-100 hover-lift">
                                <i class="bi bi-file-earmark-check-fill text-primary fs-1 mb-2"></i>
                                <h6 class="fw-bold mb-1">Certificado Examen</h6>
                                <p class="text-muted small mb-3">Solicitá constancia de asistencia a examen.</p>
                                <button type="button" class="btn btn-sm btn-primary fw-bold rounded-pill px-4 mt-auto" data-bs-toggle="modal" data-bs-target="#modalExamen">
                                    Solicitar
                                </button>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-3">
                            <div class="d-flex flex-column align-items-center p-4 bg-light rounded-3 text-center h-100 hover-lift">
                                <i class="bi bi-file-medical-fill text-success fs-1 mb-2"></i>
                                <h6 class="fw-bold mb-1">Justificar Inasistencia</h6>
                                <p class="text-muted small mb-3">Subí tu certificado médico.</p>
                                <a href="{% url 'subir_justificativo' %}" class="btn btn-sm btn-success text-white fw-bold rounded-pill px-4 mt-auto">Subir Archivo</a>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-3">
                            <div class="d-flex flex-column align-items-center p-4 bg-light rounded-3 text-center h-100 hover-lift">
                                <i class="bi bi-mortarboard-fill text-warning fs-1 mb-2"></i>
                                <h6 class="fw-bold mb-1">Nueva Carrera</h6>
                                <p class="text-muted small mb-3">Postulate a una carrera diferente.</p>
                                <a href="{% url 'solicitar_nueva_carrera' %}" class="btn btn-sm btn-warning fw-bold rounded-pill px-4 mt-auto">Inscribirse</a>
                            </div>
                        </div>
                    </div>
                    
                    <hr class="my-4">
                    <h6 class="fw-bold text-dark mb-3"><i class="bi bi-clock-history me-1"></i>Mis Solicitudes de Trámites</h6>
                    <div class="table-responsive">
                        <table class="table table-sm table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Fecha</th>
                                    <th>Trámite</th>
                                    <th>Detalle</th>
                                    <th>Estado</th>
                                    <th>Acción</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for tram in tramites %}
                                <tr>
                                    <td>{{ tram.fecha_solicitud|date:"d/m/Y H:i" }}</td>
                                    <td>{{ tram.get_tipo_display }}</td>
                                    <td>
                                        {% if tram.tipo == 'EXAMEN' %}
                                            {{ tram.materia.nombre }} (Examen: {{ tram.fecha_examen|date:"d/m/Y" }})
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if tram.estado == 'PENDIENTE' %}
                                            <span class="badge bg-secondary">Pendiente</span>
                                        {% elif tram.estado == 'RECHAZADO' %}
                                            <span class="badge bg-danger">Rechazado</span>
                                        {% elif tram.estado == 'APROBADO' %}
                                            {% if tram.esta_vigente %}
                                                <span class="badge bg-success">Aprobado / Vigente</span>
                                            {% else %}
                                                <span class="badge bg-warning text-dark">Vencido (Pasaron >7 días)</span>
                                            {% endif %}
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if tram.estado == 'APROBADO' and tram.esta_vigente %}
                                            {% if tram.tipo == 'REGULAR' %}
                                                <a href="{% url 'constancia_alumno' alumno.id %}" target="_blank" class="btn btn-sm btn-dark"><i class="bi bi-download"></i> PDF</a>
                                            {% elif tram.tipo == 'EXAMEN' %}
                                                <a href="{% url 'certificado_examen_alumno' alumno.id %}?materia_id={{ tram.materia.id }}&fecha={{ tram.fecha_examen|date:'Y-m-d' }}" target="_blank" class="btn btn-sm btn-primary"><i class="bi bi-download"></i> PDF</a>
                                            {% endif %}
                                        {% else %}
                                            <span class="text-muted small">-</span>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="5" class="text-center text-muted">No has solicitado trámites recientemente.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>

</div>

<!-- Modal Solicitud Certificado Examen -->
<div class="modal fade" id="modalExamen" tabindex="-1" aria-labelledby="modalExamenLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <form method="post" action="{% url 'solicitar_tramite_alumno' %}">
          {% csrf_token %}
          <input type="hidden" name="tipo_tramite" value="EXAMEN">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="modalExamenLabel"><i class="bi bi-file-earmark-check-fill me-2"></i>Solicitar Certificado de Examen</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
                <label class="form-label fw-bold">Materia rendida</label>
                <select name="materia_id" class="form-select" required>
                    <option value="">-- Seleccionar Materia --</option>
                    {% for m in materias_plan %}
                        <option value="{{ m.id }}">{{ m.nombre }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Fecha del Examen</label>
                <input type="date" name="fecha_examen" class="form-control" required>
            </div>
            <p class="small text-muted mb-0">La solicitud será enviada a Bedelía para su autorización. Una vez aprobada, tendrás 7 días hábiles para descargar el certificado PDF.</p>
          </div>
          <div class="modal-footer border-top-0">
            <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancelar</button>
            <button type="submit" class="btn btn-primary fw-bold">Enviar Solicitud</button>
          </div>
      </form>
    </div>
  </div>
</div>
'''

content = re.sub(pattern, new_tramites, content, flags=re.DOTALL)

with codecs.open('gestion/templates/gestion/alumnos/dashboard_alumno.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("dashboard html updated")
