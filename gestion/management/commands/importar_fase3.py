import os
import django
import datetime
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Migracion masiva de Alumnos (Fase 3)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecuta un simulacro sin guardar cambios en la base de datos',
        )

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
            self.stdout.write(self.style.WARNING("Ningun dato sera modificado realmente.\n"))

        sql_file = '/tmp/redarg_pdb.sql'
        if not os.path.exists(sql_file):
            sql_file = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'
            if not os.path.exists(sql_file):
                self.stdout.write(self.style.ERROR('No se encontr redarg_pdb.sql en /tmp/ ni local.'))
                return

        from gestion.models import Alumno, PlanDeEstudio, InscripcionCarrera
        from gestion.signals import sync_inscripcion_classroom
        from gestion.models import Inscripcion
        
        if not dry_run:
            post_save.disconnect(sync_inscripcion_classroom, sender=Inscripcion)

        try:
            plan_locucion = PlanDeEstudio.objects.filter(nombre__icontains='Locuci').filter(nombre__icontains='19').first()
            plan_locucion_2025 = PlanDeEstudio.objects.filter(nombre__icontains='Locuci').filter(nombre__icontains='2025').first()
            plan_television = PlanDeEstudio.objects.filter(nombre__icontains='Televis').first()
            plan_sistemas = PlanDeEstudio.objects.filter(nombre__icontains='Sistemas').first()
            plan_sagradas = PlanDeEstudio.objects.filter(nombre__icontains='Sagradas').first()
            plan_historico = PlanDeEstudio.objects.filter(nombre__icontains='Hist').first()

            map_carrera = {
                '16': plan_locucion,
                '8': plan_locucion,
                '24': plan_locucion_2025,
                '17': plan_television,
                '9': plan_sagradas,
                '13': plan_sistemas,
            }

            self.stdout.write(">> Parseando carreras_alumnos...")
            ca_rows = self.parse_sql_lines(sql_file, 'carreras_alumnos')
            user_carreras = {}
            for row in ca_rows:
                try:
                    parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                    c_id = parts[1].strip()
                    u_id = parts[2].strip()
                    if u_id not in user_carreras:
                        user_carreras[u_id] = set()
                    user_carreras[u_id].add(c_id)
                except: pass

            self.stdout.write(">> Procesando alumnos (users)...")
            users_rows = self.parse_sql_lines(sql_file, 'users')
            
            created_count = 0
            updated_count = 0
            
            estudiantes_group = Group.objects.filter(name='Estudiantes').first() if not dry_run else None
            if not estudiantes_group and not dry_run:
                estudiantes_group, _ = Group.objects.get_or_create(name='Estudiantes')

            for row_str in users_rows:
                try:
                    parts = next(csv.reader(StringIO(row_str), delimiter=',', quotechar="'", skipinitialspace=True, escapechar='\\'))
                except: continue
                    
                if len(parts) > 13:
                    u_id = parts[0]
                    l_nombre = parts[1].strip()
                    l_ape = parts[2].strip()
                    l_email = parts[3].strip()
                    l_dni = parts[4].strip()
                    
                    if not l_dni or l_dni == 'NULL': continue
                    if l_email == 'NULL' or not l_email: l_email = f"{l_dni}@test.com"
                    
                    l_tel = parts[7].strip() if parts[7] != 'NULL' else None
                    l_dir = parts[9].strip() if parts[9] != 'NULL' else None
                    l_nac = parts[13].strip() if parts[13] != 'NULL' else None
                    
                    l_nac_date = None
                    if l_nac and len(l_nac) >= 10:
                        try: l_nac_date = datetime.datetime.strptime(l_nac[:10], '%Y-%m-%d').date()
                        except: pass
                        
                    # Evaluar carreras
                    carreras_legacy = user_carreras.get(u_id, set())
                    planes_a_asignar = set()
                    for c_leg in carreras_legacy:
                        if c_leg in map_carrera and map_carrera[c_leg]:
                            planes_a_asignar.add(map_carrera[c_leg])
                    
                    if not planes_a_asignar:
                        planes_a_asignar.add(plan_historico)
                        
                    if not dry_run:
                        alumno = Alumno.objects.filter(dni=l_dni).first()
                        if not alumno:
                            user, u_created = User.objects.get_or_create(username=l_dni, defaults={'email': l_email[:149], 'first_name': l_nombre[:29], 'last_name': l_ape[:29]})
                            if u_created:
                                user.set_password(l_dni)
                                user.groups.add(estudiantes_group)
                                user.save()
                                
                            alumno = Alumno.objects.create(
                                usuario=user, dni=l_dni[:15], nombre=l_nombre[:49], apellido=l_ape[:49],
                                email=l_email[:99], celular=l_tel[:19] if l_tel else None,
                                direccion=l_dir[:199] if l_dir else None, fecha_nacimiento=l_nac_date
                            )
                            created_count += 1
                        else:
                            # Update demograficos si faltan
                            mod = False
                            if not alumno.celular and l_tel: alumno.celular = l_tel[:19]; mod = True
                            if not alumno.direccion and l_dir: alumno.direccion = l_dir[:199]; mod = True
                            if not alumno.fecha_nacimiento and l_nac_date: alumno.fecha_nacimiento = l_nac_date; mod = True
                            if mod: alumno.save(); updated_count += 1
                            
                        # Asignar carreras (aditivo)
                        for p in planes_a_asignar:
                            InscripcionCarrera.objects.get_or_create(alumno=alumno, plan=p, defaults={'estado': 'CURSANDO'})
                    else:
                        if Alumno.objects.filter(dni=l_dni).exists():
                            updated_count += 1
                        else:
                            created_count += 1

            self.stdout.write(self.style.SUCCESS(f">> Alumnos: {created_count} nuevos, {updated_count} actualizados."))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la migracion: {e}'))
            import traceback; traceback.print_exc()
        finally:
            if not dry_run:
                post_save.connect(sync_inscripcion_classroom, sender=Inscripcion)
