import os
import ast
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Importa cursadas y finales segmentado por carrera legacy y año'

    def add_arguments(self, parser):
        parser.add_argument('--carrera_legacy', type=int, required=True)
        parser.add_argument('--plan_nuevo', type=int, required=True)
        parser.add_argument('--anio', type=int, required=True)
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
                    if line.startswith('('): rows.append(line)
                    if is_end: in_table = False
        return rows

    def handle(self, *args, **options):
        carrera_legacy = options['carrera_legacy']
        plan_nuevo = options['plan_nuevo']
        anio = options['anio']
        dry_run = options['dry_run']

        file_path = r'/tmp/redarg_pdb.sql'
        if not os.path.exists(file_path): file_path = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'

        from gestion.models import Alumno, Materia, Comision, Inscripcion, MesaExamen, InscripcionMesa
        def normalize(n): return n.lower().strip().replace('ǭ','a').replace('Ǹ','e').replace('','i').replace('','o').replace('ǧ','u').replace('','n').replace(' ', '')

        self.stdout.write(f">> Mapeando datos para Legacy Carrera {carrera_legacy} -> Nuevo Plan {plan_nuevo} | AÑO: {anio}")
        
        legacy_u = {}
        for row in self.parse_sql_lines(file_path, 'users'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_u[int(parts[0])] = str(parts[4]).strip()
            except: pass
            
        legacy_m_names = {}
        for row in self.parse_sql_lines(file_path, 'materias'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_m_names[int(parts[0])] = str(parts[1]).strip()
            except: pass

        target_cursos = {}
        for row in self.parse_sql_lines(file_path, 'cursos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                c_id = int(parts[0])
                c_anio = int(parts[2])
                m_id = int(parts[6])
                c_car = int(parts[7])
                if c_car == carrera_legacy and c_anio == anio:
                    target_cursos[c_id] = m_id
            except: pass

        target_examens = {}
        for row in self.parse_sql_lines(file_path, 'examens'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                e_id = int(parts[0])
                e_car = int(parts[1])
                m_id = int(parts[2])
                fecha = str(parts[5]).strip()
                if e_car == carrera_legacy and fecha.startswith(str(anio)):
                    target_examens[e_id] = {'m_id': m_id, 'fecha': fecha}
            except: pass

        alumnos_db = {a.dni: a for a in Alumno.objects.all()}
        materias_plan = {normalize(m.nombre): m for m in Materia.objects.filter(plan_id=plan_nuevo)}

        estado_map = {'cursando': 'REG', 'libre': 'LIB', 'regular': 'APR', 'promocionado': 'PROM'}
        insc_creadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_cursos'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    u_id = int(parts[1])
                    c_id = int(parts[2])
                    l_estado = str(parts[4]).strip().lower()
                    
                    if c_id not in target_cursos: continue
                    
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    legacy_name = legacy_m_names.get(target_cursos[c_id], "")
                    mat_real = materias_plan.get(normalize(legacy_name))
                    if not mat_real: continue
                        
                    estado_nuevo = estado_map.get(l_estado, 'REG')
                    comision_obj, _ = Comision.objects.get_or_create(
                        materia=mat_real, ciclo_lectivo=anio,
                        defaults={'cuatrimestre': 'AN', 'cerrada': (anio < 2025)}
                    )
                    
                    if not Inscripcion.objects.filter(alumno=al, comision=comision_obj).exists():
                        if not dry_run: Inscripcion.objects.create(alumno=al, comision=comision_obj, estado=estado_nuevo)
                        insc_creadas += 1
                except: pass

        self.stdout.write(f"Inscripciones a Cursada ({anio}): {insc_creadas} cargadas.")

        estado_mesa_map = {'aprobado': 'APR', 'desaprobado': 'REP', 'ausente': 'AUS'}
        mesas_creadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_examens'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    u_id = int(parts[1])
                    e_id = int(parts[2])
                    nota = str(parts[3]).strip() if parts[3] is not None else ''
                    l_estado = str(parts[4]).strip().lower()
                    folio = str(parts[6]).strip() if parts[6] is not None else ''
                    libro = str(parts[7]).strip() if parts[7] is not None else ''
                    
                    if e_id not in target_examens: continue
                    
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    examen_info = target_examens[e_id]
                    legacy_name = legacy_m_names.get(examen_info['m_id'], "")
                    mat_real = materias_plan.get(normalize(legacy_name))
                    if not mat_real: continue
                    
                    estado_nuevo = estado_mesa_map.get(l_estado, 'AUS')
                    fecha_str = examen_info['fecha']
                    
                    mesa_obj = MesaExamen.objects.filter(materia=mat_real, fecha_hora__startswith=fecha_str).first()
                    if not mesa_obj:
                        if not dry_run: mesa_obj = MesaExamen.objects.create(materia=mat_real, fecha_hora=f"{fecha_str} 18:00:00", cerrada=True)
                            
                    if mesa_obj and not InscripcionMesa.objects.filter(alumno=al, mesa=mesa_obj).exists():
                        if not dry_run:
                            InscripcionMesa.objects.create(alumno=al, mesa=mesa_obj, estado=estado_nuevo, nota=nota, libro_matriz=libro, folio_matriz=folio)
                        mesas_creadas += 1
                except: pass

        self.stdout.write(f"Inscripciones a Finales ({anio}): {mesas_creadas} cargadas.")
        self.stdout.write(self.style.SUCCESS(">>> IMPORTACION SEGMENTADA COMPLETADA <<<"))
