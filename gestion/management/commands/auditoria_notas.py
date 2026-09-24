import os
import ast
from collections import defaultdict
from django.core.management.base import BaseCommand
from gestion.models import Inscripcion, InscripcionMesa, Nota

class Command(BaseCommand):
    help = 'Audita las notas importadas vs la base legacy'

    def handle(self, *args, **options):
        file_path = r'/tmp/redarg_pdb.sql'
        if not os.path.exists(file_path): file_path = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'

        def normalize(n): return n.lower().strip().replace('ǭ','a').replace('Ǹ','e').replace('','i').replace('','o').replace('ǧ','u').replace('','n').replace(' ', '')
        def limpiar_dni(d): return ''.join(filter(str.isdigit, str(d).split('.')[0].split(',')[0]))

        legacy_u = {}
        legacy_alumnos = {}
        legacy_m_names = {}
        legacy_cursos = {}
        legacy_examens = {}

        def parse_sql_lines(table_name):
            in_table = False
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.startswith(f"INSERT INTO `{table_name}`"): in_table = True; continue
                    if in_table:
                        line = line.strip()
                        is_end = line.endswith(';')
                        if line.endswith(';') or line.endswith(','): line = line[:-1]
                        if line.startswith('('): yield line
                        if is_end: in_table = False

        for row in parse_sql_lines('users'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_u[int(parts[0])] = limpiar_dni(parts[4])
            except: pass

        for row in parse_sql_lines('alumnos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_alumnos[int(parts[0])] = int(parts[5])
            except: pass

        for row in parse_sql_lines('materias'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_m_names[int(parts[0])] = normalize(str(parts[1]))
            except: pass

        for row in parse_sql_lines('cursos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                c_id = int(parts[0])
                c_anio = int(parts[2])
                m_id = int(parts[6])
                legacy_cursos[c_id] = {'materia': legacy_m_names.get(m_id, ''), 'anio': c_anio}
            except: pass

        for row in parse_sql_lines('examens'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                e_id = int(parts[0])
                m_id = int(parts[2])
                fecha = str(parts[5]).strip()[:4]
                legacy_examens[e_id] = {'materia': legacy_m_names.get(m_id, ''), 'anio': int(fecha)}
            except: pass

        legacy_cursadas = {}
        for row in parse_sql_lines('alumnos_cursos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                al_id = int(parts[1])
                c_id = int(parts[2])
                raw_nota = parts[9] if len(parts) > 9 else None
                
                u_id = legacy_alumnos.get(al_id)
                if not u_id: continue
                dni = legacy_u.get(u_id)
                if not dni: continue
                
                c_info = legacy_cursos.get(c_id)
                if not c_info: continue
                
                if raw_nota is not None and raw_nota != 'ausente':
                    try:
                        nota = int(raw_nota)
                        legacy_cursadas[(dni, c_info['materia'], c_info['anio'])] = nota
                    except: pass
            except: pass

        legacy_finales = {}
        for row in parse_sql_lines('alumnos_examens'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                al_id = int(parts[1])
                e_id = int(parts[2])
                raw_nota = parts[4]
                
                u_id = legacy_alumnos.get(al_id)
                if not u_id: continue
                dni = legacy_u.get(u_id)
                if not dni: continue
                
                e_info = legacy_examens.get(e_id)
                if not e_info: continue
                
                if raw_nota is not None and raw_nota != 'ausente' and str(raw_nota).strip() != '':
                    try:
                        nota = int(raw_nota)
                        legacy_finales[(dni, e_info['materia'], e_info['anio'])] = nota
                    except: pass
            except: pass

        new_cursadas = {}
        for insc in Inscripcion.objects.select_related('alumno', 'comision__materia').all():
            n = Nota.objects.filter(inscripcion=insc, instancia='Nota Final').first()
            if n:
                dni = limpiar_dni(insc.alumno.dni)
                mat = normalize(insc.comision.materia.nombre)
                anio = insc.comision.ciclo_lectivo
                new_cursadas[(dni, mat, anio)] = n.valor_nota

        new_finales = {}
        for m in InscripcionMesa.objects.select_related('alumno', 'mesa__materia').all():
            if m.nota_final > 0:
                dni = limpiar_dni(m.alumno.dni)
                mat = normalize(m.mesa.materia.nombre)
                anio = m.mesa.fecha_hora.year
                new_finales[(dni, mat, anio)] = m.nota_final

        def compare_dicts(legacy, new, name):
            self.stdout.write(f"\n--- REPORTE DE {name.upper()} ---")
            coinciden = 0
            difieren = []
            faltan_en_nueva = []
            sobran_en_nueva = [] # Solo para ver si hay creadas que no estaban en legacy
            
            for k, v in legacy.items():
                if k in new:
                    if new[k] == v:
                        coinciden += 1
                    else:
                        difieren.append((k, v, new[k]))
                else:
                    faltan_en_nueva.append((k, v))
            
            for k, v in new.items():
                if k not in legacy:
                    sobran_en_nueva.append((k, v))
                    
            self.stdout.write(f"Total Evaluadas en DB Legacy: {len(legacy)}")
            self.stdout.write(f"Coincidencias Exactas: {coinciden}")
            self.stdout.write(f"Difieren (Nota Legacy != Nota Nueva): {len(difieren)}")
            if difieren:
                self.stdout.write("Ejemplos de diferencias:")
                for k, old_val, new_val in difieren[:5]:
                    self.stdout.write(f"  DNI: {k[0]}, Materia: {k[1]}, Año: {k[2]} -> Legacy: {old_val}, Nueva: {new_val}")
                    
            # Faltan en DB Nueva significa que estaban en Legacy pero no migraron.
            # Sin embargo, como importamos segmentado, MUCHAS faltarán porque aún no importó todas las carreras.
            # Así que mostramos solo unas pocas como info.
            self.stdout.write(f"Faltan en DB Nueva (Estaban en legacy y no pasaron): {len(faltan_en_nueva)}")
            
        compare_dicts(legacy_cursadas, new_cursadas, "Cursadas")
        compare_dicts(legacy_finales, new_finales, "Finales")
        self.stdout.write("\n>>> AUDITORIA COMPLETADA <<<")
