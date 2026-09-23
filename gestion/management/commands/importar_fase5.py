import os
from django.core.management.base import BaseCommand
import ast

class Command(BaseCommand):
    help = 'Migracion masiva de Docentes y Comisiones (Fase 5)'
    def add_arguments(self, parser): parser.add_argument('--dry-run', action='store_true', help='Ejecuta un simulacro')
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
        def clean_name(full_name, legacy_slug):
            ape, nom = "", ""
            full_name = full_name.strip()
            if ',' in full_name:
                parts = full_name.split(',', 1)
                ape = parts[0].strip().title()
                nom = parts[1].strip().title()
            else:
                words = full_name.split()
                if len(words) == 1: ape = words[0].title(); nom = "-"
                elif len(words) == 2: ape = words[0].title(); nom = words[1].title()
                elif len(words) >= 3: ape = words[0].title(); nom = " ".join(words[1:]).title()
                else: ape = full_name.title(); nom = "-"
            return ape[:99], nom[:99] if nom else "-"

        from gestion.models import Docente, Materia, Comision
        from django.contrib.auth.models import User, Group
        
        try:
            self.stdout.write(">> Mapeando Materias legacy...")
            legacy_m = {}
            for row in self.parse_sql_lines(sql_file, 'materias'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    legacy_m[str(parts[0])] = normalize(str(parts[1]))
                except: pass

            self.stdout.write(">> Extrayendo Docentes legacy...")
            legacy_docentes_map = {}
            for row in self.parse_sql_lines(sql_file, 'docentes'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    legacy_docentes_map[str(parts[0])] = str(parts[1])
                except: pass

            self.stdout.write(">> Extrayendo perfiles de usuario...")
            legacy_users_data = {}
            for row in self.parse_sql_lines(sql_file, 'users'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    u_id = str(parts[0])
                    if u_id in legacy_docentes_map.values():
                        l_name = str(parts[1])
                        l_slug = str(parts[2])
                        l_email = str(parts[3])
                        l_dni = str(parts[4])
                        if l_dni and l_dni != 'None':
                            l_dni_limpio = ''.join(filter(str.isdigit, l_dni.split('.')[0].split(',')[0]))
                            if l_dni_limpio:
                                ape, nom = clean_name(l_name, l_slug)
                                if l_email == 'None' or not l_email: l_email = f"docente_{l_dni_limpio}@sigeet.com"
                                legacy_users_data[u_id] = {'dni': l_dni_limpio, 'nombre': nom, 'apellido': ape, 'email': l_email}
                except: pass

            self.stdout.write(">> Creando perfiles de Docentes...")
            docentes_group = Group.objects.filter(name='Docentes').first() if not dry_run else None
            if not docentes_group and not dry_run: docentes_group, _ = Group.objects.get_or_create(name='Docentes')
            
            docente_obj_map = {} 
            created_docs = 0
            for d_id, u_id in legacy_docentes_map.items():
                u_data = legacy_users_data.get(u_id)
                if not u_data: continue
                dni = u_data['dni'][:15]
                if not dry_run:
                    docente = Docente.objects.filter(dni=dni).first()
                    if not docente:
                        user, u_created = User.objects.get_or_create(username=dni, defaults={'email': u_data['email'][:149], 'first_name': u_data['nombre'][:149], 'last_name': u_data['apellido'][:149]})
                        if u_created:
                            user.set_password(dni)
                            user.groups.add(docentes_group)
                            user.save()
                        docente = Docente.objects.create(usuario=user, dni=dni, nombre=u_data['nombre'], apellido=u_data['apellido'])
                        created_docs += 1
                    docente_obj_map[d_id] = docente
                else:
                    created_docs += 1
                    class Mock: pass
                    docente_obj_map[d_id] = Mock()

            self.stdout.write(">> Cacheando materias locales...")
            materias_db = {normalize(m.nombre): m for m in Materia.objects.all()}

            self.stdout.write(">> Parseando Cursos para recrear Comisiones...")
            created_coms = 0
            updated_coms = 0
            for row in self.parse_sql_lines(sql_file, 'cursos'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    anio = int(parts[2])
                    periodo_raw = str(parts[3])
                    m_id = str(parts[6])
                    d_id = str(parts[8])
                    p_id = str(parts[9])
                    
                    cuat = 'AN'
                    if periodo_raw == '1': cuat = '1C'
                    elif periodo_raw == '2': cuat = '2C'
                    
                    norm_mat = legacy_m.get(m_id)
                    if not norm_mat: continue
                    m_obj = materias_db.get(norm_mat)
                    if not m_obj: continue
                    
                    docente_principal = docente_obj_map.get(d_id)
                    docente_aux = docente_obj_map.get(p_id) if p_id != 'None' else None
                    
                    if not dry_run:
                        comision, c_created = Comision.objects.get_or_create(
                            materia=m_obj, ciclo_lectivo=anio,
                            defaults={'cuatrimestre': cuat, 'tipo_aprobacion': 'FIN', 'modalidad': 'P', 'cerrada': (anio < 2025)}
                        )
                        mod = False
                        if comision.docente != docente_principal:
                            comision.docente = docente_principal
                            mod = True
                        if docente_aux and comision.docente_auxiliar != docente_aux:
                            comision.docente_auxiliar = docente_aux
                            mod = True
                        
                        if c_created: created_coms += 1
                        elif mod: 
                            comision.save()
                            updated_coms += 1
                    else:
                        created_coms += 1
                except Exception as e:
                    pass

            self.stdout.write(self.style.SUCCESS(f">> Migracion Fase 5 completa. {created_coms} comisiones nuevas, {updated_coms} actualizadas."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
