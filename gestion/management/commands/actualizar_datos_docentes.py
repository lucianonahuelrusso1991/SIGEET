import os
import ast
from datetime import datetime
from django.core.management.base import BaseCommand
from gestion.models import Docente

class Command(BaseCommand):
    help = 'Actualiza los datos demograficos y de contacto de los docentes desde la BD vieja'

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

    def clean_date(self, d_str):
        if not d_str or d_str == 'None': return None
        try: return datetime.strptime(d_str[:10], "%Y-%m-%d").date()
        except: return None

    def handle(self, *args, **options):
        sql_file = '/tmp/redarg_pdb.sql'
        if not os.path.exists(sql_file): sql_file = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'

        self.stdout.write(">> Cargando mapa de docentes legacy...")
        legacy_docentes_map = {}
        for row in self.parse_sql_lines(sql_file, 'docentes'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_docentes_map[str(parts[0])] = str(parts[1])
            except: pass

        self.stdout.write(">> Actualizando datos demograficos de docentes...")
        updated = 0
        
        for row in self.parse_sql_lines(sql_file, 'users'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                u_id = str(parts[0])
                
                if u_id in legacy_docentes_map.values():
                    l_email = str(parts[3])
                    l_dni = str(parts[4])
                    l_telefono = str(parts[7])
                    l_nac = str(parts[8])
                    l_dir = str(parts[9])
                    l_sexo_raw = str(parts[11])
                    l_fnac = self.clean_date(str(parts[13]))
                    l_lnac = str(parts[14])
                    l_zona = str(parts[21]) if len(parts) > 21 else 'None'
                    l_cp = str(parts[22]) if len(parts) > 22 else 'None'
                    
                    clean_dni = ''.join(filter(str.isdigit, l_dni.split('.')[0].split(',')[0]))
                    
                    docente = Docente.objects.filter(dni=clean_dni).first()
                    if docente:
                        if l_email and l_email != 'None': docente.email = l_email[:254]
                        if l_telefono and l_telefono != 'None': docente.telefono = l_telefono[:20]
                        if l_nac and l_nac != 'None': docente.nacionalidad = l_nac[:100]
                        if l_dir and l_dir != 'None': docente.direccion = l_dir[:200]
                        
                        if l_sexo_raw == 'masculino': docente.sexo = 'M'
                        elif l_sexo_raw == 'femenino': docente.sexo = 'F'
                        else: docente.sexo = 'X'
                        
                        if l_fnac: docente.fecha_nacimiento = l_fnac
                        if l_lnac and l_lnac != 'None': docente.lugar_nacimiento = l_lnac[:100]
                        if l_zona and l_zona != 'None': docente.comuna_zona = l_zona[:100]
                        if l_cp and l_cp != 'None': docente.codigo_postal = l_cp[:20]
                        
                        docente.save()
                        updated += 1
            except: pass

        self.stdout.write(self.style.SUCCESS(f">> Exito: Se actualizaron los datos demograficos de {updated} docentes."))