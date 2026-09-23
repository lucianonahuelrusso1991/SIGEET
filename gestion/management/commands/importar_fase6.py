import os
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reasignacion de Inscripciones a las Comisiones reales (Fase 6)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Simulacro sin guardar cambios')

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
        if dry_run: self.stdout.write(self.style.WARNING("--- EJECUTANDO EN MODO DRY-RUN (SIMULACRO) ---"))

        sql_file = '/tmp/redarg_pdb.sql'
        if not os.path.exists(sql_file):
            sql_file = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'
            if not os.path.exists(sql_file): return
            
        def normalize(n): return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')

        from gestion.models import Materia, Comision, Inscripcion, Alumno, MesaExamen, InscripcionMesa
        
        try:
            self.stdout.write(">> Mapeando Materias y Cursos...")
            legacy_m = {}
            for row in self.parse_sql_lines(sql_file, 'materias'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                    legacy_m[parts[0].strip()] = normalize(parts[1].strip())
                except: pass

            materias_db = {normalize(m.nombre): m for m in Materia.objects.all()}
            
            # curso_id -> (materia_id_db, anio)
            legacy_cursos = {}
            for row in self.parse_sql_lines(sql_file, 'cursos'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                    c_id = parts[0].strip()
                    anio = int(parts[2].strip())
                    m_id_leg = parts[6].strip()
                    
                    norm_mat = legacy_m.get(m_id_leg)
                    if norm_mat and norm_mat in materias_db:
                        legacy_cursos[c_id] = (materias_db[norm_mat].id, anio)
                except: pass

            self.stdout.write(">> Indexando Comisiones locales...")
            # (materia_id, anio) -> Comision
            comisiones_map = {}
            for c in Comision.objects.exclude(ciclo_lectivo=1900):
                comisiones_map[(c.materia_id, c.ciclo_lectivo)] = c
                
            self.stdout.write(">> Mapeando Usuarios...")
            legacy_u = {}
            for row in self.parse_sql_lines(sql_file, 'users'):
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                    u_id = parts[0].strip()
                    l_dni = parts[4].strip()
                    if l_dni and l_dni != 'NULL':
                        l_dni_limpio = ''.join(filter(str.isdigit, l_dni.split('.')[0].split(',')[0]))
                        if l_dni_limpio: legacy_u[u_id] = l_dni_limpio
                except: pass
                
            alumnos_db = {a.dni: a for a in Alumno.objects.all()}

            self.stdout.write(">> Parseando Libretas para mover alumnos de 1900 a las Reales...")
            lib_rows = self.parse_sql_lines(sql_file, 'libretas')
            
            movidas_insc = 0
            
            for row in lib_rows:
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                except: continue
                
                if len(parts) > 12:
                    l_user_id = parts[3].strip()
                    l_curso_id = parts[12].strip()
                    
                    if l_curso_id == 'NULL' or not l_curso_id: continue
                    
                    u_dni = legacy_u.get(l_user_id)
                    curso_info = legacy_cursos.get(l_curso_id)
                    
                    if u_dni and curso_info:
                        al = alumnos_db.get(u_dni)
                        m_db_id, anio = curso_info
                        comision_real = comisiones_map.get((m_db_id, anio))
                        
                        if al and comision_real:
                            # Buscar inscripcion del alumno en esta materia pero en comision 1900
                            # y moverla a comision_real
                            inscs = Inscripcion.objects.filter(alumno=al, comision__materia_id=m_db_id)
                            for insc in inscs:
                                if insc.comision.ciclo_lectivo == 1900:
                                    if not dry_run:
                                        insc.comision = comision_real
                                        insc.save()
                                    movidas_insc += 1

            self.stdout.write(self.style.SUCCESS(f">> Migracion Fase 6 completa. {movidas_insc} inscripciones movidas a sus comisiones reales con docentes asignados."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
