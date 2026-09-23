import os
import ast
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Reasignacion de Inscripciones masivas desde alumnos_cursos (Fase 6b)'
    def add_arguments(self, parser): parser.add_argument('--dry-run', action='store_true', help='Simulacro')
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
        dry_run = options['dry_run']
        if dry_run: self.stdout.write(self.style.WARNING("--- EJECUTANDO EN MODO DRY-RUN (SIMULACRO) ---"))

        sql_file = '/tmp/redarg_pdb.sql'
        if not os.path.exists(sql_file): sql_file = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'
            
        def normalize(n): return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')

        from gestion.models import Materia, Comision, Inscripcion, Alumno, Nota
        from django.db.models.signals import post_save
        from gestion.signals import sync_inscripcion_classroom
        if not dry_run: post_save.disconnect(sync_inscripcion_classroom, sender=Inscripcion)
        
        try:
            self.stdout.write(">> Mapeando Materias y Cursos...")
            legacy_m = {}
            for row in self.parse_sql_lines(sql_file, 'materias'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    legacy_m[str(parts[0])] = normalize(str(parts[1]))
                except: pass
            materias_db = {normalize(m.nombre): m for m in Materia.objects.all()}
            
            legacy_cursos = {}
            for row in self.parse_sql_lines(sql_file, 'cursos'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    c_id = str(parts[0])
                    anio = int(parts[2])
                    m_id_leg = str(parts[6])
                    norm_mat = legacy_m.get(m_id_leg)
                    if norm_mat and norm_mat in materias_db: legacy_cursos[c_id] = (materias_db[norm_mat].id, anio)
                except: pass

            self.stdout.write(">> Indexando Comisiones locales...")
            comisiones_map = {}
            for c in Comision.objects.exclude(ciclo_lectivo=1900): comisiones_map[(c.materia_id, c.ciclo_lectivo)] = c
                
            self.stdout.write(">> Mapeando Usuarios...")
            legacy_u = {}
            for row in self.parse_sql_lines(sql_file, 'users'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    u_id = str(parts[0])
                    l_dni = str(parts[4])
                    if l_dni and l_dni != 'None':
                        l_dni_limpio = ''.join(filter(str.isdigit, l_dni.split('.')[0].split(',')[0]))
                        if l_dni_limpio: legacy_u[u_id] = l_dni_limpio
                except: pass
                
            self.stdout.write(">> Mapeando Alumnos-Usuarios...")
            alumnos_map = {} 
            for row in self.parse_sql_lines(sql_file, 'alumnos'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    alumnos_map[str(parts[0])] = str(parts[5])
                except: pass

            alumnos_db = {a.dni: a for a in Alumno.objects.all()}

            self.stdout.write(">> Inyectando alumnos_cursos (Inscripciones Reales)...")
            created_insc = 0
            updated_insc = 0
            
            estado_map = {
                'promociona': 'PROM', 'final': 'APR', 'libre': 'LIB', 'baja': 'LIB',
                'cursando': 'REG', 'pierde_promo': 'APR', 'reincorpora': 'REG',
                'reincorpor sin promocin': 'APR', 'reincorpor con promocin': 'PROM', 'No Aprueba': 'LIB'
            }
            
            for row in self.parse_sql_lines(sql_file, 'alumnos_cursos'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    l_alumno_id = str(parts[1])
                    l_curso_id = str(parts[2])
                    l_estado = str(parts[6]) if len(parts) > 6 else 'cursando'
                    l_nota = str(parts[9]) if len(parts) > 9 else 'None'
                    
                    u_id = alumnos_map.get(l_alumno_id)
                    u_dni = legacy_u.get(u_id)
                    curso_info = legacy_cursos.get(l_curso_id)
                    
                    if u_dni and curso_info:
                        al = alumnos_db.get(u_dni)
                        m_db_id, anio = curso_info
                        comision_real = comisiones_map.get((m_db_id, anio))
                        
                        if al and comision_real:
                            estado_nuevo = estado_map.get(l_estado, 'REG')
                            if not dry_run:
                                insc, c_created = Inscripcion.objects.get_or_create(
                                    alumno=al, comision=comision_real, defaults={'estado': estado_nuevo}
                                )
                                mod = False
                                jerarquia = {'LIB': 0, 'REG': 1, 'APR': 2, 'PROM': 3}
                                if not c_created:
                                    if jerarquia.get(estado_nuevo, 1) > jerarquia.get(insc.estado, 1):
                                        insc.estado = estado_nuevo
                                        mod = True
                                
                                if c_created: created_insc += 1
                                elif mod: 
                                    insc.save()
                                    updated_insc += 1
                                    
                                if l_nota != 'None' and l_nota != 'ausente' and l_nota:
                                    try:
                                        n_val = int(l_nota)
                                        Nota.objects.get_or_create(inscripcion=insc, instancia='Nota Final', defaults={'valor_nota': n_val})
                                    except: pass
                            else:
                                created_insc += 1
                except: pass

            self.stdout.write(self.style.SUCCESS(f">> Migracion Fase 6b completa. {created_insc} inscripciones creadas, {updated_insc} actualizadas."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
        finally:
            if not dry_run: post_save.connect(sync_inscripcion_classroom, sender=Inscripcion)
