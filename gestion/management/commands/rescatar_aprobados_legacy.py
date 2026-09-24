from django.core.management.base import BaseCommand
from gestion.models import Inscripcion, Alumno, Materia, Comision
import os
import ast

class Command(BaseCommand):
    help = 'Corrige el estado Aprobado del sistema legacy que se mezclo con Regular'

    def parse_sql_lines(self, file_path, table_name):
        lines = []
        capture = False
        if not os.path.exists(file_path):
            return lines
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith(f"INSERT INTO `{table_name}`"):
                    capture = True
                    # Extraer los values
                    start_idx = line.find("VALUES") + 6
                    values_str = line[start_idx:].strip()
                    if values_str.endswith(';'):
                        values_str = values_str[:-1]
                    
                    import re
                    pattern = r'\((.*?)\)(?:,|$)'
                    matches = re.finditer(pattern, values_str)
                    for match in matches:
                        yield match.group(1)

    def handle(self, *args, **kwargs):
        file_path = r'/tmp/redarg_pdb.sql'
        if not os.path.exists(file_path): 
            file_path = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'
            
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"No se encontro el backup en {file_path}. Debes subirlo a /tmp/redarg_pdb.sql"))
            return

        def limpiar_dni(d): return ''.join(filter(str.isdigit, str(d).split('.')[0].split(',')[0]))
        def normalize(n): return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')
        
        alumnos_db = {limpiar_dni(a.dni): a for a in Alumno.objects.all()}
        
        # Mapear legacy users
        legacy_u = {}
        for row in self.parse_sql_lines(file_path, 'users'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_u[int(parts[0])] = limpiar_dni(parts[4])
            except: pass
            
        # Mapear legacy alumnos
        legacy_alumnos = {}
        for row in self.parse_sql_lines(file_path, 'alumnos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_alumnos[int(parts[0])] = int(parts[1])
            except: pass
            
        # Mapear legacy cursos
        target_cursos = {}
        for row in self.parse_sql_lines(file_path, 'cursos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                target_cursos[int(parts[0])] = {'m_id': int(parts[6]), 'anio': int(parts[2])}
            except: pass
            
        # Mapear legacy materias names
        legacy_m_names = {}
        for row in self.parse_sql_lines(file_path, 'materias'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_m_names[int(parts[0])] = normalize(str(parts[1]))
            except: pass

        corregidas = 0
        for row in self.parse_sql_lines(file_path, 'alumnos_cursos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                al_id = int(parts[1])
                c_id = int(parts[2])
                l_estado = str(parts[3]).strip().lower()
                
                # Si era 'aprobado' o 'promocionado' o 'promocion' en la BD vieja
                if l_estado in ['aprobado', 'promocionado', 'promocion']:
                    u_id = legacy_alumnos.get(al_id)
                    if not u_id: continue
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    c_info = target_cursos.get(c_id)
                    if not c_info: continue
                    
                    legacy_name = legacy_m_names.get(c_info['m_id'], "")
                    
                    # Buscar inscripciones de este alumno que esten en APR o REG
                    for insc in al.inscripciones.filter(estado__in=['APR', 'REG']):
                        materia_nombre = normalize(insc.comision.materia.nombre)
                        if materia_nombre == legacy_name:
                            insc.estado = 'PROM'
                            insc.save(update_fields=['estado'])
                            corregidas += 1
            except Exception as e:
                pass
                
        self.stdout.write(self.style.SUCCESS(f'Exito: Se han restaurado {corregidas} materias a estado PROM (Aprobado/Promocionado) desde el backup legacy.'))