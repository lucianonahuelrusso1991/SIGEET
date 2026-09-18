import re

with open('gestion/templates/gestion/revisar_preinscripto.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Documentation section
old_docs = '''                        <!-- Checklists de Documentacin -->
                        <h5 class="fw-bold text-primary mb-3 border-bottom pb-2">4. Documentacin Fsicamente Entregada</h5>
                        <div class="card border-0 shadow-sm rounded-3 mb-4">
                            <div class="card-body">
                                <div class="row g-3">
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_dni }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_dni.id_for_label }}">Fotocopia DNI</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_vacunas }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_vacunas.id_for_label }}">Certificado de Vacunas</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_partida }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_partida.id_for_label }}">Partida de Nacimiento</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_primaria }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_primaria.id_for_label }}">Certificado Primaria</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_pase }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_pase.id_for_label }}">Pase / Ttulo Secundario</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Submit -->
                        <div class="d-flex justify-content-end gap-3 mt-5 border-top pt-4">
                            <a href="{% url 'lista_preinscriptos' %}" class="btn btn-outline-light px-4 fw-bold rounded-pill">Cancelar</a>
                            <button type="submit" class="btn btn-success px-5 fw-bold rounded-pill shadow-sm hover-lift">
                                o. Confirmar Alta de Alumno
                            </button>
                        </div>'''

new_docs = '''                        <!-- Checklists de Documentacin -->
                        <h5 class="fw-bold text-primary mb-3 border-bottom pb-2">4. Documentacin Fsicamente Entregada</h5>
                        <div class="card border-0 shadow-sm rounded-3 mb-4">
                            <div class="card-body">
                                <div class="row g-3">
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_dni }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_dni.id_for_label }}">Fotocopia DNI</label>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-check form-switch fs-5 mb-2">
                                            {{ form.doc_primaria }}
                                            <label class="form-check-label text-dark" for="{{ form.doc_primaria.id_for_label }}">Ttulo Secundario</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Datos Institucionales -->
                        <h5 class="fw-bold text-primary mb-3 border-bottom pb-2">5. Datos Institucionales</h5>
                        <div class="alert alert-info shadow-sm rounded-3">
                            <strong><i class="bi bi-info-circle-fill me-2"></i>Instrucciones de alta:</strong><br>
                            Si an no tiene correo institucional creado por Soporte Tcnico, dej el campo en blanco y guard los datos. El alumno quedarǭ en estado <b>En Espera de Correo</b>.<br>
                            Si ya tenǸs el correo, completalo para formalizar la inscripcin y crearle el usuario.
                        </div>
                        <div class="row g-3 mb-4">
                            <div class="col-md-12">
                                <label class="form-label fw-bold text-dark fs-5">Correo Institucional (Genera el usuario final)</label>
                                {{ form.correo_institucional }}
                            </div>
                        </div>

                        <!-- Submit -->
                        <div class="d-flex justify-content-end gap-3 mt-5 border-top pt-4">
                            <a href="{% url 'lista_preinscriptos' %}" class="btn btn-outline-light px-4 fw-bold rounded-pill">Cancelar</a>
                            <button type="submit" class="btn btn-success px-5 fw-bold rounded-pill shadow-sm hover-lift">
                                <i class="bi bi-check-circle-fill me-2"></i> Confirmar y Guardar
                            </button>
                        </div>'''

# Need to decode old_docs if character encoding issues, but exact string match should work if we read the file normally
with open('gestion/templates/gestion/revisar_preinscripto.html', 'r', encoding='latin-1') as f:
    content = f.read()

# I will use a regex to be safer due to encoding artifacts
pattern = r'<!-- Checklists de Documentaci.*<!-- Submit -->.*?</div>'

content_new = re.sub(pattern, new_docs, content, flags=re.DOTALL)

with open('gestion/templates/gestion/revisar_preinscripto.html', 'w', encoding='utf-8') as f:
    f.write(content_new)

print("Template updated")
