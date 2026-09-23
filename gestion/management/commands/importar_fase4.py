import os
import django
import datetime
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models.signals import post_save

class Command(BaseCommand):
    help = 'Migracion masiva de Cursadas y Finales (Fase 4)'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Ejecuta un simulacro')

    def parse_sql_lines(self, file_path, table_name):
        in_table = False
        rows = []
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith(f"INSERT INTO `{table_name}`"):
                    in_table = True
                    continue
                if in_table:
                    line = line.strip()
                    is_end = line.endswith(';')
                    if line.endswith(';') or line.endswith(','):
                        line = line[:-1]
                    if line.startswith('('):
                        rows.append(line[1:-1])
                    if is_end:
                        in_table = False
        return rows

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING("--- EJECUTANDO EN MODO DRY-RUN (SIMULACRO) ---"))

        sql_file = '/tmp/redarg_pdb.sql'
        if not os.path.exists(sql_file):
            sql_file = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'
            if not os.path.exists(sql_file): return
            
        def normalize(n):
            return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')

        from gestion.models import Alumno, Materia, Comision, MesaExamen, Inscripcion, InscripcionMesa, Nota
        from gestion.signals import sync_inscripcion_classroom
        if not dry_run: post_save.disconnect(sync_inscripcion_classroom, sender=Inscripcion)

        try:
            self.stdout.write(">> Mapeando Materias legacy...")
            m_rows = self.parse_sql_lines(sql_file, 'materias')
            legacy_m = {}
            for row in m_rows:
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                    m_id = parts[0].strip()
                    m_name = parts[1].strip()
                    legacy_m[m_id] = normalize(m_name)
                except: pass

            self.stdout.write(">> Mapeando Usuarios legacy...")
            u_rows = self.parse_sql_lines(sql_file, 'users')
            legacy_u = {}
            for row in u_rows:
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                    u_id = parts[0].strip()
                    l_dni = parts[4].strip()
                    if l_dni and l_dni != 'NULL':
                        l_dni_limpio = ''.join(filter(str.isdigit, l_dni.split('.')[0].split(',')[0]))
                        if l_dni_limpio: legacy_u[u_id] = l_dni_limpio
                except: pass

            self.stdout.write(">> Cacheando BD local...")
            alumnos_db = {a.dni: a for a in Alumno.objects.all()}
            
            # Cachear comisiones histricas para materias
            comisiones_cache = {}
            materias_db = Materia.objects.all()
            for m in materias_db:
                n = normalize(m.nombre)
                if n not in comisiones_cache:
                    comisiones_cache[n] = m # guardamos la materia, la comision la creamos on-demand para ahorrar ram
            
            def get_comision(materia):
                c = Comision.objects.filter(materia=materia, ciclo_lectivo=1900).first()
                if not c and not dry_run:
                    c = Comision.objects.create(materia=materia, ciclo_lectivo=1900, cuatrimestre='AN', tipo_aprobacion='FIN', modalidad='P', cerrada=True)
                return c
            
            def str_to_date(d_str):
                if not d_str or d_str == 'NULL' or len(d_str) < 10: return None
                try: return datetime.datetime.strptime(d_str[:10], '%Y-%m-%d').date()
                except: return None

            self.stdout.write(">> Parseando Libretas (Notas)...")
            lib_rows = self.parse_sql_lines(sql_file, 'libretas')
            
            count_insc = 0
            count_fin = 0
            count_prom = 0
            
            for row in lib_rows:
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                except: continue
                
                if len(parts) > 15:
                    l_materia_id = parts[2].strip()
                    l_user_id = parts[3].strip()
                    l_motivo_id = parts[4].strip()
                    
                    fecha_insc = str_to_date(parts[6].strip())
                    fecha_cursada = str_to_date(parts[7].strip())
                    fecha_final = str_to_date(parts[8].strip())
                    
                    l_calif_raw = parts[9].strip()
                    try: nota_real = int(l_calif_raw)
                    except ValueError: nota_real = 7 
                        
                    l_libro = parts[13].strip()
                    l_folio = parts[14].strip()
                    if l_libro == 'NULL': l_libro = ''
                    if l_folio == 'NULL': l_folio = ''
                    
                    u_dni = legacy_u.get(l_user_id)
                    norm_mat = legacy_m.get(l_materia_id)
                    
                    if u_dni and norm_mat:
                        al = alumnos_db.get(u_dni)
                        m_obj = comisiones_cache.get(norm_mat)
                        
                        if al and m_obj:
                            c_act = get_comision(m_obj) if not dry_run else None
                            if not c_act and not dry_run: continue
                            
                            estado_cursada = 'REG' 
                            
                            if l_motivo_id in ['40', '95']: estado_cursada = 'APR'
                            elif l_motivo_id == '51': estado_cursada = 'LIB'
                            elif l_motivo_id == '10': estado_cursada = 'REG'
                            elif l_motivo_id == '90': 
                                if l_libro or l_folio: estado_cursada = 'APR'
                                else: estado_cursada = 'PROM' 
                            
                            if not dry_run:
                                insc, created = Inscripcion.objects.get_or_create(alumno=al, comision=c_act, defaults={'estado': estado_cursada})
                                jerarquia = {'LIB': 0, 'REG': 1, 'APR': 2, 'PROM': 3}
                                if not created and jerarquia.get(estado_cursada, 1) > jerarquia.get(insc.estado, 1):
                                    insc.estado = estado_cursada
                                    
                                fecha_real_cursada = fecha_cursada or fecha_insc or datetime.date.today()
                                if insc.fecha_inscripcion != fecha_real_cursada:
                                    Inscripcion.objects.filter(id=insc.id).update(fecha_inscripcion=fecha_real_cursada)
                            
                            count_insc += 1
                            
                            if l_motivo_id == '90':
                                if l_libro or l_folio:
                                    if not dry_run:
                                        mesa_fecha = timezone.make_aware(datetime.datetime.combine(fecha_final, datetime.time(0,0))) if fecha_final else timezone.now()
                                        mesa_act = MesaExamen.objects.filter(materia=m_obj, fecha_hora__date=mesa_fecha.date(), ciclo_lectivo=1900).first()
                                        if not mesa_act:
                                            mesa_act = MesaExamen.objects.create(materia=m_obj, fecha_hora=mesa_fecha, ciclo_lectivo=1900, turno='ESPECIAL', cerrada=True)
                                        if l_libro and not mesa_act.libro:
                                            mesa_act.libro = l_libro[:49]
                                            mesa_act.save()
                                        if l_folio and not mesa_act.folio:
                                            mesa_act.folio = l_folio[:49]
                                            mesa_act.save()
                                            
                                        InscripcionMesa.objects.get_or_create(alumno=al, mesa=mesa_act, defaults={'nota_final': nota_real, 'estado': 'APR'})
                                    count_fin += 1
                                else:
                                    if not dry_run:
                                        n, _ = Nota.objects.get_or_create(inscripcion=insc, instancia='Nota Final', defaults={'valor_nota': nota_real})
                                        if n.fecha != (fecha_final or fecha_real_cursada):
                                            Nota.objects.filter(id=n.id).update(fecha=fecha_final or fecha_real_cursada)
                                    count_prom += 1

            self.stdout.write(self.style.SUCCESS(f">> Migracion Fase 4 completa. {count_insc} inscripciones, {count_fin} finales, {count_prom} promociones."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            import traceback; traceback.print_exc()
        finally:
            if not dry_run: post_save.connect(sync_inscripcion_classroom, sender=Inscripcion)