import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
import unicodedata
from gestion.models import Alumno, Materia, Inscripcion, Nota, PlanDeEstudio, Comision, InscripcionCarrera, MesaExamen, InscripcionMesa
from django.contrib.auth.models import User
from gestion.signals import sync_inscripcion_classroom

def normalize_string(s):
    s = s.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

class Command(BaseCommand):
    help = 'Importa Fase 3 - Reparacion de Duplicados y Fechas'

    def add_arguments(self, parser):
        parser.add_argument('sql_file', type=str, help='Ruta al archivo redarg_pdb.sql')

    def parse_sql_lines(self, file_path, table_name):
        rows = []
        in_insert = False
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith(f"INSERT INTO `{table_name}`"):
                    in_insert = True
                    continue
                if in_insert:
                    line = line.strip()
                    if line.endswith(';'):
                        if line != ';':
                            row = line[:-1].strip()
                            if row.startswith('('): row = row[1:]
                            if row.endswith(')'): row = row[:-1]
                            rows.append(row)
                        in_insert = False
                    elif line.endswith(','):
                        if line != ',':
                            row = line[:-1].strip()
                            if row.startswith('('): row = row[1:]
                            if row.endswith(')'): row = row[:-1]
                            rows.append(row)
        return rows

    def handle(self, *args, **options):
        sql_file = options['sql_file']
        
        try:
            post_save.disconnect(sync_inscripcion_classroom, sender=Inscripcion)
            
            with transaction.atomic():
                self.stdout.write(self.style.SUCCESS('--- INICIANDO FASE 3 (REPARACION FINAL) ---'))
                
                plan_historico, _ = PlanDeEstudio.objects.get_or_create(nombre='Plan Histórico (Migración)', defaults={'activo': False})
                if plan_historico.activo:
                    plan_historico.activo = False
                    plan_historico.save()

                Inscripcion.objects.all().delete()
                Nota.objects.all().delete()
                InscripcionMesa.objects.all().delete()
                MesaExamen.objects.filter(ciclo_lectivo=1900).delete()
                Comision.objects.filter(ciclo_lectivo=1900).delete()
                
                # ELIMINAR DUPLICADOS EN MAYUSCULA (Fuzzy Match)
                self.stdout.write('Limpiando Materias duplicadas en mayuscula...')
                all_materias = list(Materia.objects.all())
                norm_dict = {}
                for m in all_materias:
                    norm = normalize_string(m.nombre)
                    if norm not in norm_dict:
                        norm_dict[norm] = []
                    norm_dict[norm].append(m)
                    
                for norm, m_list in norm_dict.items():
                    if len(m_list) > 1:
                        # Priorizar la que NO es toda mayuscula
                        m_list.sort(key=lambda x: (x.nombre.isupper(), x.id))
                        keeper = m_list[0]
                        for duplicate in m_list[1:]:
                            duplicate.delete()
                
                plan_locucion = PlanDeEstudio.objects.filter(nombre__icontains='Locuci').filter(nombre__icontains='19').first() or PlanDeEstudio.objects.filter(nombre__icontains='Locuci').first()
                plan_television = PlanDeEstudio.objects.filter(nombre__icontains='Televis').first()
                plan_sistemas = PlanDeEstudio.objects.filter(nombre__icontains='Sistemas').first()
                
                map_carrera = {
                    '16': plan_locucion or plan_historico,
                    '8': plan_locucion or plan_historico,
                    '17': plan_television or plan_historico,
                    '18': plan_sistemas or plan_historico,
                    '1': plan_sistemas or plan_historico,
                }
                
                cm_rows = self.parse_sql_lines(sql_file, 'carreras_materias')
                materia_to_carrera = {}
                for row in cm_rows:
                    parts = row.split(',')
                    if len(parts) > 2:
                        c_id = parts[1].strip()
                        m_id = parts[2].strip()
                        materia_to_carrera[m_id] = c_id
                
                materias_rows = self.parse_sql_lines(sql_file, 'materias')
                materia_dict = {}
                comision_dict = {}
                mesa_dict = {}
                
                fecha_historica = timezone.now()
                
                # Volver a cachear las materias luego de la limpieza
                materias_existentes = {normalize_string(m.nombre): m for m in Materia.objects.all()}
                
                for row in materias_rows:
                    parts = row.split("','") if "','" in row else row.split(',')
                    if len(parts) >= 2:
                        m_id = parts[0].strip()
                        m_name = parts[1].strip().strip("'")[:149]
                        norm_name = normalize_string(m_name)
                        
                        legacy_c_id = materia_to_carrera.get(m_id)
                        plan_correcto = map_carrera.get(legacy_c_id, plan_historico)
                        
                        if norm_name in materias_existentes:
                            m_obj = materias_existentes[norm_name]
                            if m_obj.plan != plan_correcto:
                                m_obj.plan = plan_correcto
                                m_obj.save()
                        else:
                            m_obj = Materia.objects.create(nombre=m_name, plan=plan_correcto, año_dictado=1, cuatrimestre_dictado='AN')
                            materias_existentes[norm_name] = m_obj
                                
                        materia_dict[m_id] = m_obj
                        
                        # Usar 1900 para que el template sepa que es historica y muestre el año de la fecha real
                        c_obj = Comision.objects.filter(materia=m_obj, ciclo_lectivo=1900).first()
                        if not c_obj:
                            c_obj = Comision.objects.create(materia=m_obj, ciclo_lectivo=1900, cuatrimestre='AN', tipo_aprobacion='FIN', modalidad='P', cerrada=False)
                        comision_dict[m_id] = c_obj
                        
                        mesa_obj = MesaExamen.objects.filter(materia=m_obj, ciclo_lectivo=1900).first()
                        if not mesa_obj:
                            mesa_obj = MesaExamen.objects.create(materia=m_obj, ciclo_lectivo=1900, turno='ESPECIAL', fecha_hora=fecha_historica, cerrada=True)
                        mesa_dict[m_id] = mesa_obj
                
                libretas_rows = self.parse_sql_lines(sql_file, 'libretas')
                
                user_dotti, _ = User.objects.get_or_create(username='33774806', defaults={'email': 'fdotti@pioix.edu.ar', 'first_name': 'FERNANDO', 'last_name': 'DOTTI'})
                alumno_dotti, _ = Alumno.objects.get_or_create(dni='33774806', defaults={'usuario': user_dotti, 'nombre': 'FERNANDO', 'apellido': 'DOTTI'})
                
                user_britos, _ = User.objects.get_or_create(username='44363997', defaults={'email': 'vbritos@pioix.edu.ar', 'first_name': 'VICTORIA', 'last_name': 'BRITOS'})
                alumno_britos, _ = Alumno.objects.get_or_create(dni='44363997', defaults={'usuario': user_britos, 'nombre': 'VICTORIA', 'apellido': 'BRITOS'})
                
                user_micieli, _ = User.objects.get_or_create(username='30149595', defaults={'email': 'dmicieli@pioix.edu.ar', 'first_name': 'ESTEFANIA', 'last_name': 'MICIELI'})
                if not user_micieli.password:
                    user_micieli.set_password('30149595')
                    user_micieli.save()
                alumno_micieli, _ = Alumno.objects.get_or_create(dni='30149595', defaults={'usuario': user_micieli, 'nombre': 'ESTEFANIA', 'apellido': 'MICIELI', 'email': 'dmicieli@pioix.edu.ar'})
                
                for al in [alumno_dotti, alumno_britos, alumno_micieli]:
                    if al and plan_locucion:
                        InscripcionCarrera.objects.get_or_create(alumno=al, plan=plan_locucion, defaults={'estado': 'CURSANDO'})
                        InscripcionCarrera.objects.filter(alumno=al, plan=plan_historico).delete()
                        InscripcionCarrera.objects.filter(alumno=al, plan=plan_sistemas).delete()
                
                def str_to_date(d_str):
                    if not d_str or d_str == 'NULL' or len(d_str) < 10: return None
                    try:
                        return datetime.datetime.strptime(d_str[:10], '%Y-%m-%d').date()
                    except:
                        return None
                        
                count_inscripciones = 0
                count_finales = 0
                count_promociones = 0
                
                for row in libretas_rows:
                    parts = row.split(',')
                    if len(parts) > 15:
                        l_materia_id = parts[2].strip()
                        l_user_id = parts[3].strip()
                        l_motivo_id = parts[4].strip()
                        
                        fecha_insc = str_to_date(parts[6].strip().strip("'"))
                        fecha_cursada = str_to_date(parts[7].strip().strip("'"))
                        fecha_final = str_to_date(parts[8].strip().strip("'"))
                        
                        l_calif_raw = parts[9].strip().strip("'")
                        try:
                            nota_real = int(l_calif_raw)
                        except ValueError:
                            nota_real = 7 
                            
                        l_libro = parts[13].strip().strip("'")
                        l_folio = parts[14].strip().strip("'")
                        if l_libro == 'NULL': l_libro = ''
                        if l_folio == 'NULL': l_folio = ''
                        
                        al = None
                        if l_user_id == '2080' and alumno_dotti: al = alumno_dotti
                        elif l_user_id == '2226' and alumno_britos: al = alumno_britos
                        elif l_user_id == '2255' and alumno_micieli: al = alumno_micieli
                        
                        if al and l_materia_id in comision_dict:
                            estado_cursada = 'REG' 
                            c_cerrada = True
                            
                            if l_motivo_id in ['40', '95']:  
                                estado_cursada = 'APR'
                            elif l_motivo_id == '51': 
                                estado_cursada = 'LIB'
                            elif l_motivo_id == '10':
                                estado_cursada = 'REG'
                                c_cerrada = False 
                            elif l_motivo_id == '90': 
                                if l_libro or l_folio:
                                    estado_cursada = 'APR'  
                                else:
                                    estado_cursada = 'PROM' 
                            
                            c_act = comision_dict[l_materia_id]
                            if c_cerrada and not c_act.cerrada:
                                c_act.cerrada = True
                                c_act.save()
                            
                            insc, created = Inscripcion.objects.get_or_create(
                                alumno=al, 
                                comision=c_act, 
                                defaults={'estado': estado_cursada}
                            )
                            
                            jerarquia = {'LIB': 0, 'REG': 1, 'APR': 2, 'PROM': 3}
                            if not created and jerarquia.get(estado_cursada, 1) > jerarquia.get(insc.estado, 1):
                                insc.estado = estado_cursada
                                
                            # LA CLAVE ESTA AQUI: fecha_cursada es fechaCursadaAprobada (el final de la cursada)
                            # Si no hay, fallback a la de inscripcion.
                            fecha_real_cursada = fecha_cursada or fecha_insc or datetime.date.today()
                            insc.fecha_inscripcion = fecha_real_cursada
                            insc.save()
                            Inscripcion.objects.filter(id=insc.id).update(fecha_inscripcion=fecha_real_cursada)
                            
                            count_inscripciones += 1
                            
                            if l_motivo_id == '90':
                                if l_libro or l_folio:
                                    # Para que no compartan la misma fecha los que rindieron distintos dias
                                    mesa_fecha = timezone.make_aware(datetime.datetime.combine(fecha_final, datetime.time(0,0))) if fecha_final else fecha_historica
                                    
                                    mesa_act = MesaExamen.objects.filter(materia=c_act.materia, fecha_hora=mesa_fecha, ciclo_lectivo=1900).first()
                                    if not mesa_act:
                                        mesa_act = MesaExamen.objects.create(materia=c_act.materia, fecha_hora=mesa_fecha, ciclo_lectivo=1900, turno='ESPECIAL', cerrada=True)
                                    if l_libro and not mesa_act.libro:
                                        mesa_act.libro = l_libro[:49]
                                        mesa_act.save()
                                    if l_folio and not mesa_act.folio:
                                        mesa_act.folio = l_folio[:49]
                                        mesa_act.save()
                                        
                                    InscripcionMesa.objects.get_or_create(
                                        alumno=al, 
                                        mesa=mesa_act, 
                                        defaults={'nota_final': nota_real, 'estado': 'APR'}
                                    )
                                    count_finales += 1
                                else:
                                    n, _ = Nota.objects.get_or_create(inscripcion=insc, instancia='Nota Final', defaults={'valor_nota': nota_real})
                                    Nota.objects.filter(id=n.id).update(fecha=fecha_final or fecha_real_cursada)
                                    count_promociones += 1

                self.stdout.write(self.style.SUCCESS(f'>> Notas reales procesadas con fechas exactas. Total: {count_inscripciones} cursadas, {count_finales} finales, {count_promociones} promociones.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la migración: {e}'))
        finally:
            post_save.connect(sync_inscripcion_classroom, sender=Inscripcion)
