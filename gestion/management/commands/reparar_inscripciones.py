import os
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Repara inscripciones y mesas usando los ids reales de cursos y examens del legacy'
    def add_arguments(self, parser): parser.add_argument('--dry-run', action='store_true')
    
    def parse_sql_lines(self, file_path, table_name):
        in_table = False
        rows = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith(f"INSERT INTO `{table_name}`"): in_table = True; continue
                if in_table:
                    line = line.strip()
                    is_end = line.endswith(';')
                    if line.endswith(';') or line.endswith(','): line = line[:-1]
                    if line.startswith('('): rows.append(line[1:-1])
                    if is_end: in_table = False
        return rows

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        file_path = r'/tmp/redarg_pdb.sql'
        if not os.path.exists(file_path): file_path = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'

        self.stdout.write(">> Parseando legacy data...")
        
        # 1. users -> DNI
        legacy_u = {}
        for row in self.parse_sql_lines(file_path, 'users'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                u_id, dni = int(parts[0]), parts[4].strip()
                if dni: legacy_u[u_id] = dni
            except: pass
            
        # 2. cursos -> materia_id, anio
        legacy_cursos = {}
        for row in self.parse_sql_lines(file_path, 'cursos'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                c_id = int(parts[0])
                anio = int(parts[2])
                m_id = int(parts[6])
                legacy_cursos[c_id] = {'m_id': m_id, 'anio': anio}
            except: pass
            
        # 3. examens -> materia_id, fecha
        legacy_examens = {}
        for row in self.parse_sql_lines(file_path, 'examens'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                e_id = int(parts[0])
                m_id = int(parts[2])
                fecha = parts[5].strip()
                legacy_examens[e_id] = {'m_id': m_id, 'fecha': fecha}
            except: pass

        from gestion.models import Alumno, Materia, Comision, Inscripcion, MesaExamen, InscripcionMesa, Nota
        from django.db.models.signals import post_save
        from gestion.signals import sync_inscripcion_classroom
        if not dry_run: post_save.disconnect(sync_inscripcion_classroom, sender=Inscripcion)

        alumnos_db = {a.dni: a for a in Alumno.objects.all()}
        materias_db = {m.id: m for m in Materia.objects.all()}
        
        def normalize(n): return n.lower().strip().replace('ǭ','a').replace('Ǹ','e').replace('','i').replace('','o').replace('ǧ','u').replace('','n').replace(' ', '')
        
        self.stdout.write(">> Procesando alumnos_cursos (Inscripciones de Cursada)...")
        # 4. alumnos_cursos
        estado_map = {'cursando': 'REG', 'libre': 'LIB', 'regular': 'APR', 'promocionado': 'PROM'}
        
        insc_creadas = 0
        insc_movidas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_cursos'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                    u_id = int(parts[1])
                    c_id = int(parts[2])
                    l_estado = parts[4].strip().lower()
                    dni = legacy_u.get(u_id)
                    curso = legacy_cursos.get(c_id)
                    if not dni or not curso: continue
                    
                    al = alumnos_db.get(dni)
                    mat = materias_db.get(curso['m_id'])
                    if not al or not mat: continue
                    
                    estado_nuevo = estado_map.get(l_estado, 'REG')
                    anio = curso['anio']
                    
                    # Buscar la comision real (con el ID correcto)
                    comision_real, _ = Comision.objects.get_or_create(
                        materia=mat, ciclo_lectivo=anio,
                        defaults={'cuatrimestre': 'AN', 'cerrada': (anio < 2025)}
                    )
                    
                    # Buscar si el alumno ya tiene una inscripcion a esta materia (incluso en otra comision erronea)
                    # Para evitar duplicados en el legajo
                    norm_mat_name = normalize(mat.nombre)
                    # Find existing inscripcion for this year and normalized name
                    existing = Inscripcion.objects.filter(
                        alumno=al, 
                        comision__ciclo_lectivo=anio
                    ).select_related('comision__materia')
                    
                    match_found = False
                    for ex in existing:
                        if normalize(ex.comision.materia.nombre) == norm_mat_name:
                            # This is the old inscripcion in the WRONG (or right) comision
                            if ex.comision_id != comision_real.id:
                                if not dry_run:
                                    ex.comision = comision_real
                                    ex.estado = estado_nuevo
                                    ex.save(update_fields=['comision', 'estado'])
                                insc_movidas += 1
                            else:
                                # Already right
                                pass
                            match_found = True
                            break
                            
                    if not match_found:
                        if not dry_run:
                            Inscripcion.objects.get_or_create(
                                alumno=al, comision=comision_real,
                                defaults={'estado': estado_nuevo}
                            )
                        insc_creadas += 1
                        
                except Exception as e:
                    pass
        
        self.stdout.write(f"Inscripciones a Comisiones: Creadas {insc_creadas}, Movidas/Corregidas {insc_movidas}")
        
        self.stdout.write(">> Procesando alumnos_examens (Mesas de Final)...")
        # 5. alumnos_examens
        estado_mesa_map = {'aprobado': 'APR', 'desaprobado': 'REP', 'ausente': 'AUS'}
        mesas_creadas = 0
        mesas_movidas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_examens'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                    u_id = int(parts[1])
                    e_id = int(parts[2])
                    nota = parts[3].strip() if parts[3].strip() != 'None' else ''
                    l_estado = parts[4].strip().lower()
                    motivo = int(parts[5]) if parts[5].strip() != 'None' else 0
                    folio = parts[6].strip() if parts[6].strip() != 'None' else ''
                    libro = parts[7].strip() if parts[7].strip() != 'None' else ''
                    
                    dni = legacy_u.get(u_id)
                    examen = legacy_examens.get(e_id)
                    if not dni or not examen: continue
                    
                    al = alumnos_db.get(dni)
                    mat = materias_db.get(examen['m_id'])
                    if not al or not mat: continue
                    
                    # Equivalencias (motivo_id = 90 o 40) we skip? 
                    # The user said Equivalencias were transformed to notes.
                    # We will map everything.
                    
                    estado_nuevo = estado_mesa_map.get(l_estado, 'AUS')
                    fecha_str = examen['fecha']
                    
                    mesa_real, _ = MesaExamen.objects.get_or_create(
                        materia=mat, fecha_hora__startswith=fecha_str,
                        defaults={'fecha_hora': f"{fecha_str} 18:00:00", 'cerrada': True}
                    )
                    
                    # Find existing
                    norm_mat_name = normalize(mat.nombre)
                    existing_mesas = InscripcionMesa.objects.filter(
                        alumno=al, 
                        mesa__fecha_hora__startswith=fecha_str
                    ).select_related('mesa__materia')
                    
                    match_found = False
                    for ex in existing_mesas:
                        if normalize(ex.mesa.materia.nombre) == norm_mat_name:
                            if ex.mesa_id != mesa_real.id:
                                if not dry_run:
                                    ex.mesa = mesa_real
                                    ex.estado = estado_nuevo
                                    ex.nota = nota
                                    ex.libro_matriz = libro
                                    ex.folio_matriz = folio
                                    ex.save()
                                mesas_movidas += 1
                            else:
                                pass
                            match_found = True
                            break
                            
                    if not match_found:
                        if not dry_run:
                            InscripcionMesa.objects.get_or_create(
                                alumno=al, mesa=mesa_real,
                                defaults={'estado': estado_nuevo, 'nota': nota, 'libro_matriz': libro, 'folio_matriz': folio}
                            )
                        mesas_creadas += 1
                        
                except Exception as e:
                    pass

        self.stdout.write(f"Inscripciones a Mesas: Creadas {mesas_creadas}, Movidas/Corregidas {mesas_movidas}")
        self.stdout.write(self.style.SUCCESS(">>> REPARACION PROFUNDA COMPLETADA <<<"))
