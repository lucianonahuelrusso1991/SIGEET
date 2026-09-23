import os
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Importa cursadas y finales segmentado por carrera legacy y año'

    def add_arguments(self, parser):
        parser.add_argument('--carrera_legacy', type=int, required=True, help='ID de la carrera en la DB vieja (ej: 13 para Sistemas)')
        parser.add_argument('--plan_nuevo', type=int, required=True, help='ID del plan en el sistema nuevo (ej: 1 para Sistemas)')
        parser.add_argument('--anio', type=int, required=True, help='Año a importar (ej: 2026)')
        parser.add_argument('--dry-run', action='store_true')

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
        carrera_legacy = options['carrera_legacy']
        plan_nuevo = options['plan_nuevo']
        anio = options['anio']
        dry_run = options['dry_run']

        file_path = r'/tmp/redarg_pdb.sql'
        if not os.path.exists(file_path): file_path = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("No se encontro redarg_pdb.sql"))
            return

        from gestion.models import Alumno, Materia, Comision, Inscripcion, MesaExamen, InscripcionMesa
        
        def normalize(n): return n.lower().strip().replace('ǭ','a').replace('Ǹ','e').replace('','i').replace('','o').replace('ǧ','u').replace('','n').replace(' ', '')

        self.stdout.write(f">> Mapeando datos para Legacy Carrera {carrera_legacy} -> Nuevo Plan {plan_nuevo} | AÑO: {anio}")
        
        # 1. users -> DNI
        legacy_u = {}
        for row in self.parse_sql_lines(file_path, 'users'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                legacy_u[int(parts[0])] = parts[4].strip()
            except: pass
            
        # 2. materias -> nombres
        legacy_m_names = {}
        for row in self.parse_sql_lines(file_path, 'materias'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\', skipinitialspace=True))
                legacy_m_names[int(parts[0])] = parts[1].strip()
            except: pass

        # 3. cursos -> (materia_id, anio) solo para esta carrera y año
        target_cursos = {}
        for row in self.parse_sql_lines(file_path, 'cursos'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                c_id = int(parts[0])
                c_anio = int(parts[2])
                m_id = int(parts[6])
                c_car = int(parts[7])
                if c_car == carrera_legacy and c_anio == anio:
                    target_cursos[c_id] = m_id
            except: pass

        # 4. examens -> (materia_id, fecha)
        target_examens = {}
        for row in self.parse_sql_lines(file_path, 'examens'):
            try:
                parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                e_id = int(parts[0])
                e_car = int(parts[1])
                m_id = int(parts[2])
                fecha = parts[5].strip()
                if e_car == carrera_legacy and fecha.startswith(str(anio)):
                    target_examens[e_id] = {'m_id': m_id, 'fecha': fecha}
            except: pass

        alumnos_db = {a.dni: a for a in Alumno.objects.all()}
        
        # Materias del plan nuevo indexadas por nombre normalizado
        materias_plan = {normalize(m.nombre): m for m in Materia.objects.filter(plan_id=plan_nuevo)}

        # Procesar Cursadas
        estado_map = {'cursando': 'REG', 'libre': 'LIB', 'regular': 'APR', 'promocionado': 'PROM'}
        insc_creadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_cursos'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                    u_id = int(parts[1])
                    c_id = int(parts[2])
                    l_estado = parts[4].strip().lower()
                    
                    if c_id not in target_cursos: continue
                    
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    legacy_m_id = target_cursos[c_id]
                    legacy_name = legacy_m_names.get(legacy_m_id, "")
                    mat_real = materias_plan.get(normalize(legacy_name))
                    
                    if not mat_real:
                        self.stdout.write(self.style.WARNING(f"Materia legacy no encontrada en nuevo plan: {legacy_name}"))
                        continue
                        
                    estado_nuevo = estado_map.get(l_estado, 'REG')
                    
                    comision_obj, _ = Comision.objects.get_or_create(
                        materia=mat_real, ciclo_lectivo=anio,
                        defaults={'cuatrimestre': 'AN', 'cerrada': (anio < 2025)}
                    )
                    
                    # Chequear si ya esta inscripto
                    existe = Inscripcion.objects.filter(alumno=al, comision=comision_obj).exists()
                    if not existe:
                        if not dry_run:
                            Inscripcion.objects.create(alumno=al, comision=comision_obj, estado=estado_nuevo)
                        insc_creadas += 1
                except Exception as e:
                    pass

        self.stdout.write(f"Inscripciones a Cursada ({anio}): {insc_creadas} cargadas.")

        # Procesar Finales
        estado_mesa_map = {'aprobado': 'APR', 'desaprobado': 'REP', 'ausente': 'AUS'}
        mesas_creadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_examens'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                    u_id = int(parts[1])
                    e_id = int(parts[2])
                    nota = parts[3].strip() if parts[3].strip() != 'None' else ''
                    l_estado = parts[4].strip().lower()
                    folio = parts[6].strip() if parts[6].strip() != 'None' else ''
                    libro = parts[7].strip() if parts[7].strip() != 'None' else ''
                    
                    if e_id not in target_examens: continue
                    
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    examen_info = target_examens[e_id]
                    legacy_m_id = examen_info['m_id']
                    legacy_name = legacy_m_names.get(legacy_m_id, "")
                    mat_real = materias_plan.get(normalize(legacy_name))
                    
                    if not mat_real: continue
                    
                    estado_nuevo = estado_mesa_map.get(l_estado, 'AUS')
                    fecha_str = examen_info['fecha']
                    
                    mesa_obj = MesaExamen.objects.filter(materia=mat_real, fecha_hora__startswith=fecha_str).first()
                    if not mesa_obj:
                        if not dry_run:
                            mesa_obj = MesaExamen.objects.create(materia=mat_real, fecha_hora=f"{fecha_str} 18:00:00", cerrada=True)
                            
                    if mesa_obj:
                        existe = InscripcionMesa.objects.filter(alumno=al, mesa=mesa_obj).exists()
                        if not existe:
                            if not dry_run:
                                InscripcionMesa.objects.create(
                                    alumno=al, mesa=mesa_obj, 
                                    estado=estado_nuevo, nota=nota, 
                                    libro_matriz=libro, folio_matriz=folio
                                )
                            mesas_creadas += 1
                except Exception as e:
                    pass

        self.stdout.write(f"Inscripciones a Finales ({anio}): {mesas_creadas} cargadas.")
        self.stdout.write(self.style.SUCCESS(">>> IMPORTACION SEGMENTADA COMPLETADA <<<"))
