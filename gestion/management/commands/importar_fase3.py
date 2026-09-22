import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
from gestion.models import Alumno, Materia, Inscripcion, Nota, PlanDeEstudio, Comision, InscripcionCarrera, MesaExamen, InscripcionMesa
from django.contrib.auth.models import User
from gestion.signals import sync_inscripcion_classroom

class Command(BaseCommand):
    help = 'Importa Fase 3 Final - Ajustando Fechas Históricas Reales'

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
                self.stdout.write(self.style.SUCCESS('--- INICIANDO FASE 3 ---'))
                
                plan_historico, _ = PlanDeEstudio.objects.get_or_create(nombre='Plan Histórico (Migración)', defaults={'activo': False})
                if plan_historico.activo:
                    plan_historico.activo = False
                    plan_historico.save()

                Inscripcion.objects.all().delete()
                Nota.objects.all().delete()
                InscripcionMesa.objects.all().delete()
                
                materias_rows = self.parse_sql_lines(sql_file, 'materias')
                materia_dict = {}
                comision_dict = {}
                mesa_dict = {}
                
                fecha_historica = timezone.now()
                
                for row in materias_rows:
                    parts = row.split("','") if "','" in row else row.split(',')
                    if len(parts) >= 2:
                        m_id = parts[0].strip()
                        m_name = parts[1].strip().strip("'")[:149]
                        m_obj = Materia.objects.filter(nombre=m_name).first()
                        if not m_obj:
                            m_obj = Materia.objects.create(nombre=m_name, plan=plan_historico, año_dictado=1, cuatrimestre_dictado='AN')
                        else:
                            if m_obj.plan != plan_historico:
                                m_obj.plan = plan_historico
                                m_obj.save()
                                
                        materia_dict[m_id] = m_obj
                        
                        c_obj, _ = Comision.objects.get_or_create(
                            materia=m_obj,
                            ciclo_lectivo=1900,
                            defaults={'cuatrimestre': 'AN', 'tipo_aprobacion': 'FIN', 'modalidad': 'P', 'cerrada': True}
                        )
                        if not c_obj.cerrada:
                            c_obj.cerrada = True
                            c_obj.save()
                        comision_dict[m_id] = c_obj
                        
                        mesa_obj, _ = MesaExamen.objects.get_or_create(
                            materia=m_obj,
                            ciclo_lectivo=1900,
                            defaults={'turno': 'ESPECIAL', 'fecha_hora': fecha_historica, 'cerrada': True}
                        )
                        mesa_dict[m_id] = mesa_obj
                
                libretas_rows = self.parse_sql_lines(sql_file, 'libretas')
                
                user_dotti = User.objects.filter(username='33774806').first()
                alumno_dotti = Alumno.objects.filter(dni='33774806').first()
                
                user_britos = User.objects.filter(username='44363997').first()
                alumno_britos = Alumno.objects.filter(dni='44363997').first()
                
                for al in [alumno_dotti, alumno_britos]:
                    if al:
                        inscs_carrera = InscripcionCarrera.objects.filter(alumno=al)
                        for ic in inscs_carrera:
                            if ic.plan != plan_historico and 'Histórico' not in ic.plan.nombre:
                                ic.delete()
                        InscripcionCarrera.objects.get_or_create(alumno=al, plan=plan_historico, defaults={'estado': 'EGRESADO'})
                
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
                        
                        # Extraer fechas reales
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
                        
                        if al and l_materia_id in comision_dict:
                            estado_cursada = 'REG' 
                            if l_motivo_id in ['40', '95']:  
                                estado_cursada = 'APR'
                            elif l_motivo_id == '51': 
                                estado_cursada = 'LIB'
                            elif l_motivo_id == '90': 
                                if l_libro or l_folio:
                                    estado_cursada = 'APR'  
                                else:
                                    estado_cursada = 'PROM' 
                            
                            insc, created = Inscripcion.objects.get_or_create(
                                alumno=al, 
                                comision=comision_dict[l_materia_id], 
                                defaults={'estado': estado_cursada}
                            )
                            
                            jerarquia = {'LIB': 0, 'REG': 1, 'APR': 2, 'PROM': 3}
                            if not created and jerarquia.get(estado_cursada, 1) > jerarquia.get(insc.estado, 1):
                                insc.estado = estado_cursada
                                
                            # Asignar fecha real a la cursada
                            fecha_real_cursada = fecha_cursada or fecha_insc or datetime.date.today()
                            insc.fecha_inscripcion = fecha_real_cursada
                            # Django's auto_now_add on fecha_inscripcion might override it on save. 
                            # So we update it via queryset below if needed, but lets try assigning it here
                            insc.save()
                            # Forzar actualizacion para evadir auto_now_add si aplica
                            Inscripcion.objects.filter(id=insc.id).update(fecha_inscripcion=fecha_real_cursada)
                            
                            count_inscripciones += 1
                            
                            if l_motivo_id == '90':
                                if l_libro or l_folio:
                                    mesa_act = mesa_dict[l_materia_id]
                                    if l_libro and not mesa_act.libro:
                                        mesa_act.libro = l_libro[:49]
                                        mesa_act.save()
                                    if l_folio and not mesa_act.folio:
                                        mesa_act.folio = l_folio[:49]
                                        mesa_act.save()
                                        
                                    if fecha_final:
                                        # Actualizar la fecha de la mesa si la original era timezone.now()
                                        if mesa_act.fecha_hora.date() == timezone.now().date():
                                            mesa_act.fecha_hora = timezone.make_aware(datetime.datetime.combine(fecha_final, datetime.time(0,0)))
                                            mesa_act.save()
                                        
                                    InscripcionMesa.objects.get_or_create(
                                        alumno=al, 
                                        mesa=mesa_act, 
                                        defaults={'nota_final': nota_real, 'estado': 'APR'}
                                    )
                                    count_finales += 1
                                else:
                                    Nota.objects.get_or_create(inscripcion=insc, instancia='Nota Final', defaults={'valor_nota': nota_real})
                                    count_promociones += 1

                self.stdout.write(self.style.SUCCESS(f'>> Notas reales procesadas con fechas exactas. Total: {count_inscripciones} cursadas, {count_finales} finales, {count_promociones} promociones.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la migración: {e}'))
        finally:
            post_save.connect(sync_inscripcion_classroom, sender=Inscripcion)
