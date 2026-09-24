import os
import ast
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import datetime

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

        from gestion.models import Alumno, Docente, Materia, Comision, Inscripcion, MesaExamen, InscripcionMesa, Nota
        def normalize(n): return n.lower().strip().replace('ǭ','a').replace('Ǹ','e').replace('','i').replace('','o').replace('ǧ','u').replace('','n').replace(' ', '')

        self.stdout.write(f">> Mapeando datos para Legacy Carrera {carrera_legacy} -> Nuevo Plan {plan_nuevo} | AÑO: {anio}")
        
        legacy_u = {}
        for row in self.parse_sql_lines(file_path, 'users'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_u[int(parts[0])] = str(parts[4]).strip()
            except: pass
            
        legacy_docentes_to_uid = {}
        for row in self.parse_sql_lines(file_path, 'docentes'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_docentes_to_uid[int(parts[0])] = int(parts[1])
            except: pass
            
        legacy_m_names = {}
        for row in self.parse_sql_lines(file_path, 'materias'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                legacy_m_names[int(parts[0])] = str(parts[1]).strip()
            except: pass

        target_materias_regimen = {}
        for row in self.parse_sql_lines(file_path, 'carreras_materias'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                cm_car = int(parts[1])
                cm_mat = int(parts[2])
                regimen = str(parts[5]).strip().lower()
                if cm_car == carrera_legacy:
                    target_materias_regimen[cm_mat] = 'PROM' if 'promocionable' in regimen else 'FIN'
            except: pass

        target_cursos = {}
        for row in self.parse_sql_lines(file_path, 'cursos'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                c_id = int(parts[0])
                c_anio = int(parts[2])
                c_periodo = str(parts[3])
                if c_periodo == '1': cuatrimestre = '1C'
                elif c_periodo == '2': cuatrimestre = '2C'
                else: cuatrimestre = 'AN'
                
                m_id = int(parts[6])
                c_car = int(parts[7])
                doc_id = int(parts[8]) if len(parts) > 8 and parts[8] is not None else None
                par_id = int(parts[9]) if len(parts) > 9 and parts[9] is not None else None
                
                if c_car == carrera_legacy and c_anio == anio:
                    target_cursos[c_id] = {'m_id': m_id, 'cuat': cuatrimestre, 'd_id': doc_id, 'p_id': par_id}
            except: pass

        target_examens = {}
        for row in self.parse_sql_lines(file_path, 'examens'):
            try:
                parts = ast.literal_eval(row.replace('NULL', 'None'))
                e_id = int(parts[0])
                e_car = int(parts[1])
                m_id = int(parts[2])
                d_id = int(parts[3]) if parts[3] is not None else None
                fecha = str(parts[5]).strip()
                if e_car == carrera_legacy and fecha.startswith(str(anio)):
                    target_examens[e_id] = {'m_id': m_id, 'fecha': fecha, 'd_id': d_id}
            except: pass

        alumnos_db = {a.dni: a for a in Alumno.objects.all()}
        docentes_db = {}
        for d in Docente.objects.all():
            docentes_db[d.dni] = d
            
        def get_docente(legacy_d_id):
            if not legacy_d_id: return None
            u_id = legacy_docentes_to_uid.get(legacy_d_id)
            if not u_id: return None
            dni = legacy_u.get(u_id)
            if not dni: return None
            dni_limpio = ''.join(filter(str.isdigit, str(dni).split('.')[0].split(',')[0]))
            doc = docentes_db.get(dni_limpio)
            if doc: return doc
            for d_dni, obj in docentes_db.items():
                if dni_limpio in str(d_dni) or str(d_dni) in dni_limpio:
                    return obj
            return None

        materias_plan = {normalize(m.nombre): m for m in Materia.objects.filter(plan_id=plan_nuevo)}

        estado_map = {'cursando': 'REG', 'libre': 'LIB', 'regular': 'APR', 'promocionado': 'PROM', 'aprobado': 'APR'}
        insc_creadas = 0
        notas_cursada_creadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_cursos'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    u_id = int(parts[1])
                    c_id = int(parts[2])
                    l_estado = str(parts[6]).strip().lower() 
                    
                    if c_id not in target_cursos: continue
                    
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    c_info = target_cursos[c_id]
                    legacy_name = legacy_m_names.get(c_info['m_id'], "")
                    mat_real = materias_plan.get(normalize(legacy_name))
                    if not mat_real: continue
                        
                    estado_nuevo = estado_map.get(l_estado, 'REG')
                    
                    # HEREDAR tipo_aprobacion de la tabla carreras_materias vieja
                    tipo_ap = target_materias_regimen.get(c_info['m_id'], 'FIN')
                    
                    if mat_real.tipo_aprobacion != tipo_ap and not dry_run:
                        mat_real.tipo_aprobacion = tipo_ap
                        mat_real.save(update_fields=['tipo_aprobacion'])
                    
                    comision_obj, _ = Comision.objects.get_or_create(
                        materia=mat_real, ciclo_lectivo=anio, cuatrimestre=c_info['cuat'],
                        defaults={'cerrada': (anio < 2025), 'tipo_aprobacion': tipo_ap}
                    )
                    if comision_obj.tipo_aprobacion != tipo_ap and not dry_run:
                        comision_obj.tipo_aprobacion = tipo_ap
                        comision_obj.save(update_fields=['tipo_aprobacion'])
                    
                    doc_pr = get_docente(c_info['d_id'])
                    doc_aux = get_docente(c_info['p_id'])
                    mod_c = False
                    if comision_obj.docente != doc_pr:
                        comision_obj.docente = doc_pr
                        mod_c = True
                    if comision_obj.docente_auxiliar != doc_aux:
                        comision_obj.docente_auxiliar = doc_aux
                        mod_c = True
                    if mod_c and not dry_run: comision_obj.save(update_fields=['docente', 'docente_auxiliar'])
                    
                    insc, created = Inscripcion.objects.get_or_create(alumno=al, comision=comision_obj, defaults={'estado': estado_nuevo})
                    if created: insc_creadas += 1
                    
                    if not created and insc.estado != estado_nuevo:
                        insc.estado = estado_nuevo
                        insc.save(update_fields=['estado'])
                        
                    if len(parts) > 9 and parts[9] is not None and parts[9] != 'ausente':
                        try:
                            nota_val = int(parts[9])
                            if not Nota.objects.filter(inscripcion=insc, instancia='Nota Final').exists():
                                Nota.objects.create(inscripcion=insc, valor_nota=nota_val, instancia='Nota Final', fecha=timezone.now().date())
                                notas_cursada_creadas += 1
                        except: pass
                except Exception as e: pass

        self.stdout.write(f"Inscripciones a Cursada ({anio}): {insc_creadas} creadas, {notas_cursada_creadas} notas de cursada cargadas.")

        estado_mesa_map = {'inscripto': 'REG', 'presente': 'APR', 'ausente': 'AUS'}
        mesas_creadas = 0
        
        with transaction.atomic():
            for row in self.parse_sql_lines(file_path, 'alumnos_examens'):
                try:
                    parts = ast.literal_eval(row.replace('NULL', 'None'))
                    u_id = int(parts[1])
                    e_id = int(parts[2])
                    l_estado = str(parts[3]).strip().lower()
                    raw_nota = parts[4]
                    
                    if e_id not in target_examens: continue
                    
                    dni = legacy_u.get(u_id)
                    al = alumnos_db.get(dni)
                    if not al: continue
                    
                    examen_info = target_examens[e_id]
                    legacy_name = legacy_m_names.get(examen_info['m_id'], "")
                    mat_real = materias_plan.get(normalize(legacy_name))
                    if not mat_real: continue
                    
                    estado_nuevo = 'APR' if raw_nota and int(raw_nota) >= 4 else 'REP'
                    if l_estado == 'ausente': estado_nuevo = 'AUS'
                    
                    fecha_str = examen_info['fecha']
                    doc_mesa = get_docente(examen_info['d_id'])
                    
                    mesa_obj = MesaExamen.objects.filter(materia=mat_real, fecha_hora__startswith=fecha_str[:10]).first()
                    if not mesa_obj:
                        if not dry_run: mesa_obj = MesaExamen.objects.create(materia=mat_real, fecha_hora=f"{fecha_str[:10]} 18:00:00", cerrada=True)
                            
                    if mesa_obj:
                        mod_m = False
                        if mesa_obj.presidente_mesa != doc_mesa:
                            mesa_obj.presidente_mesa = doc_mesa
                            mod_m = True
                        if mod_m and not dry_run: mesa_obj.save(update_fields=['presidente_mesa'])
                            
                        nota_val = int(raw_nota) if raw_nota is not None else 0
                        ins_mesa, created = InscripcionMesa.objects.get_or_create(
                            alumno=al, mesa=mesa_obj,
                            defaults={'estado': estado_nuevo, 'nota_final': nota_val}
                        )
                        if created:
                            mesas_creadas += 1
                        else:
                            ins_mesa.estado = estado_nuevo
                            ins_mesa.nota_final = nota_val
                            ins_mesa.save(update_fields=['estado', 'nota_final'])
                except: pass

        self.stdout.write(f"Inscripciones a Finales ({anio}): {mesas_creadas} cargadas.")
        self.stdout.write(self.style.SUCCESS(">>> IMPORTACION SEGMENTADA COMPLETADA <<<"))
