import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone
from gestion.models import Alumno, Materia, Inscripcion, Nota, PlanDeEstudio, Comision, InscripcionCarrera, MesaExamen, InscripcionMesa
from django.contrib.auth.models import User
from gestion.signals import sync_inscripcion_classroom

class Command(BaseCommand):
    help = 'Importa Fase 3 Final y Distingue Promociones'

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
                
                plan_default = PlanDeEstudio.objects.first()
                if not plan_default:
                    plan_default, _ = PlanDeEstudio.objects.get_or_create(nombre='Plan Default Histórico', activo=False)

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
                            m_obj = Materia.objects.create(nombre=m_name, plan=plan_default, año_dictado=1, cuatrimestre_dictado='AN')
                        materia_dict[m_id] = m_obj
                        
                        c_obj, _ = Comision.objects.get_or_create(
                            materia=m_obj,
                            ciclo_lectivo=1900,
                            defaults={'cuatrimestre': 'AN', 'tipo_aprobacion': 'FIN', 'modalidad': 'P', 'cerrada': True}
                        )
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
                
                if alumno_dotti:
                    InscripcionCarrera.objects.get_or_create(alumno=alumno_dotti, plan=plan_default, defaults={'estado': 'EGRESADO'})
                if alumno_britos:
                    InscripcionCarrera.objects.get_or_create(alumno=alumno_britos, plan=plan_default, defaults={'estado': 'EGRESADO'})
                
                count_inscripciones = 0
                count_finales = 0
                count_promociones = 0
                
                for row in libretas_rows:
                    parts = row.split(',')
                    if len(parts) > 15:
                        l_materia_id = parts[2].strip()
                        l_user_id = parts[3].strip()
                        l_motivo_id = parts[4].strip()
                        
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
                            if l_motivo_id in ['40', '95']:  # Aprobo cursada o debe final
                                estado_cursada = 'APR'
                            elif l_motivo_id == '90': # Aprobo asignatura
                                # Distinguimos si es PROMOCION o FINAL
                                if l_libro or l_folio:
                                    estado_cursada = 'APR'  # Rindio final, la cursada esta aprobada
                                else:
                                    estado_cursada = 'PROM' # No hay acta, es promocion directa
                            
                            insc, created = Inscripcion.objects.get_or_create(
                                alumno=al, 
                                comision=comision_dict[l_materia_id], 
                                defaults={'estado': estado_cursada}
                            )
                            # Actualizamos estado si es de mayor jerarquia
                            jerarquia = {'REG': 1, 'APR': 2, 'PROM': 3}
                            if not created and jerarquia.get(estado_cursada, 1) > jerarquia.get(insc.estado, 1):
                                insc.estado = estado_cursada
                                insc.save()
                                
                            count_inscripciones += 1
                            
                            if l_motivo_id == '90':
                                if l_libro or l_folio:
                                    # Es un Final
                                    mesa_act = mesa_dict[l_materia_id]
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
                                    # Es una Promocion, guardamos la nota final
                                    Nota.objects.get_or_create(inscripcion=insc, instancia='Nota Final', defaults={'valor_nota': nota_real})
                                    count_promociones += 1

                self.stdout.write(self.style.SUCCESS(f'>> Notas reales procesadas. Total: {count_inscripciones} cursadas, {count_finales} finales, {count_promociones} promociones.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la migración: {e}'))
        finally:
            post_save.connect(sync_inscripcion_classroom, sender=Inscripcion)
