from django.core.management.base import BaseCommand
from gestion.models import InscripcionMesa, Alumno, Materia, MesaExamen, Docente
from django.db import transaction
import os
import ast

class Command(BaseCommand):
    help = 'Restaura TODAS las mesas de examen del sistema legacy corrigiendo los errores de importacion.'

    def parse_sql_lines(self, file_path, table_name):
        lines = []
        if not os.path.exists(file_path):
            return lines
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith(f"INSERT INTO `{table_name}`"):
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
            self.stdout.write(self.style.ERROR(f"No se encontro el backup en {file_path}"))
            return

        def limpiar_dni(d): return ''.join(filter(str.isdigit, str(d).split('.')[0].split(',')[0]))
        def normalize(n): return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')
        
        alumnos_db = {limpiar_dni(a.dni): a for a in Alumno.objects.all()}
        docentes_db = {limpiar_dni(d.dni): d for d in Docente.objects.all()}
        materias_db = {normalize(m.nombre): m for m in Materia.objects.all()} # Global
        
        legacy_u = {}
        for row in self.parse_sql_lines(file_path, 'users'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_u[int(parts[0])] = limpiar_dni(parts[4])
            except: pass
            
        legacy_alumnos = {}
        for row in self.parse_sql_lines(file_path, 'alumnos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_alumnos[int(parts[0])] = int(parts[1])
            except: pass
            
        legacy_docentes_to_uid = {}
        for row in self.parse_sql_lines(file_path, 'docentes'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_docentes_to_uid[int(parts[0])] = int(parts[1])
            except: pass

        def get_docente(legacy_d_id):
            if not legacy_d_id: return None
            u_id = legacy_docentes_to_uid.get(legacy_d_id)
            if not u_id: return None
            dni = legacy_u.get(u_id)
            return docentes_db.get(dni)
            
        legacy_m_names = {}
        for row in self.parse_sql_lines(file_path, 'materias'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_m_names[int(parts[0])] = normalize(str(parts[1]))
            except: pass

        # Cargar TODOS los examenes sin filtrar por anio
        target_examens = {}
        for row in self.parse_sql_lines(file_path, 'examens'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                e_id = int(parts[0])
                m_id = int(parts[2])
                d_id = int(parts[3]) if parts[3] is not None else None
                fecha = str(parts[5]).strip()
                target_examens[e_id] = {'m_id': m_id, 'fecha': fecha, 'd_id': d_id}
            except: pass

        creadas = 0
        actualizadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_examens'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    al_id = int(parts[1])
                    e_id = int(parts[2])
                    l_estado = str(parts[3]).strip().lower()
                    raw_nota = parts[4]
                    
                    if e_id not in target_examens: continue
                    
                    u_id = legacy_alumnos.get(al_id)
                    if not u_id: continue
                    
                    dni_limpio = legacy_u.get(u_id)
                    al = alumnos_db.get(dni_limpio)
                    if not al: continue
                    
                    examen_info = target_examens[e_id]
                    legacy_name = legacy_m_names.get(examen_info['m_id'], "")
                    mat_real = materias_db.get(legacy_name)
                    if not mat_real: continue
                    
                    # LOGICA ROBUSTA DE NOTAS Y ESTADOS
                    nota_val = 0
                    if raw_nota is not None:
                        try:
                            nota_val = int(float(str(raw_nota).replace(',','.')))
                        except:
                            nota_val = 0
                            
                    if l_estado in ['aprobado', 'presente', 'promocionado']:
                        estado_nuevo = 'APR'
                        if nota_val == 0: nota_val = 6 # Nota minima si falta
                    elif l_estado == 'ausente':
                        estado_nuevo = 'AUS'
                    else:
                        estado_nuevo = 'REP' if nota_val < 4 else 'APR'
                        
                    fecha_str = examen_info['fecha']
                    doc_mesa = get_docente(examen_info['d_id'])
                    
                    # Buscar o crear la MesaExamen global
                    mesa_obj = MesaExamen.objects.filter(materia=mat_real, fecha_hora__startswith=fecha_str[:10]).first()
                    if not mesa_obj:
                        mesa_obj = MesaExamen.objects.create(materia=mat_real, fecha_hora=f"{fecha_str[:10]} 18:00:00", cerrada=True)
                            
                    if mesa_obj.presidente_mesa != doc_mesa and doc_mesa:
                        mesa_obj.presidente_mesa = doc_mesa
                        mesa_obj.save(update_fields=['presidente_mesa'])
                        
                    ins_mesa, created = InscripcionMesa.objects.get_or_create(
                        alumno=al, mesa=mesa_obj,
                        defaults={'estado': estado_nuevo, 'nota_final': nota_val}
                    )
                    if created:
                        creadas += 1
                    else:
                        # Si ya existia pero era REP por error, lo pisamos con el correcto
                        if ins_mesa.estado != estado_nuevo or ins_mesa.nota_final != nota_val:
                            ins_mesa.estado = estado_nuevo
                            ins_mesa.nota_final = nota_val
                            ins_mesa.save(update_fields=['estado', 'nota_final'])
                            actualizadas += 1
                except Exception as e:
                    pass

        self.stdout.write(self.style.SUCCESS(f'Exito: {creadas} nuevas actas importadas. {actualizadas} actas actualizadas/corregidas.'))