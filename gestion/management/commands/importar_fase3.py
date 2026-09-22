import os
from django.core.management.base import BaseCommand
from django.db import transaction
from gestion.models import Alumno, Materia, Inscripcion, Nota, PlanDeEstudio
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Importa Fase 3'

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
            with transaction.atomic():
                self.stdout.write(self.style.SUCCESS('--- INICIANDO FASE 3 ---'))
                
                plan_default = PlanDeEstudio.objects.first()
                if not plan_default:
                    plan_default, _ = PlanDeEstudio.objects.get_or_create(nombre='Plan Default Histórico', activo=False)

                Inscripcion.objects.all().delete()
                Nota.objects.all().delete()
                
                materias_rows = self.parse_sql_lines(sql_file, 'materias')
                materia_dict = {}
                for row in materias_rows:
                    parts = row.split(',')
                    if len(parts) >= 2:
                        m_id = parts[0].strip()
                        m_name = parts[1].strip().strip("'")[:149]
                        m_obj = Materia.objects.filter(nombre=m_name).first()
                        if not m_obj:
                            m_obj = Materia.objects.create(nombre=m_name, plan=plan_default, año_dictado=1, cuatrimestre_dictado='AN')
                        materia_dict[m_id] = m_obj
                
                self.stdout.write(f'Materias registradas/vinculadas: {len(materia_dict)}')
                
                libretas_rows = self.parse_sql_lines(sql_file, 'libretas')
                
                user_dotti = User.objects.filter(username='33774806').first()
                alumno_dotti = Alumno.objects.filter(dni='33774806').first()
                
                user_britos = User.objects.filter(username='44363997').first()
                alumno_britos = Alumno.objects.filter(dni='44363997').first()
                
                count_inscripciones = 0
                count_notas = 0
                
                for row in libretas_rows:
                    parts = row.split(',')
                    if len(parts) > 5:
                        l_materia_id = parts[2].strip()
                        l_user_id = parts[3].strip()
                        l_motivo_id = parts[4].strip()
                        
                        if l_user_id == '2080' and alumno_dotti and l_materia_id in materia_dict:
                            insc, _ = Inscripcion.objects.get_or_create(alumno=alumno_dotti, materia=materia_dict[l_materia_id], defaults={'estado': 'Regular'})
                            count_inscripciones += 1
                            if l_motivo_id in ['40', '41', '90', '95']:
                                Nota.objects.get_or_create(inscripcion=insc, tipo='Final', defaults={'calificacion': 7})
                                count_notas += 1
                                
                        if l_user_id == '2226' and alumno_britos and l_materia_id in materia_dict:
                            insc, _ = Inscripcion.objects.get_or_create(alumno=alumno_britos, materia=materia_dict[l_materia_id], defaults={'estado': 'Regular'})
                            count_inscripciones += 1
                            if l_motivo_id in ['40', '41', '90', '95']:
                                Nota.objects.get_or_create(inscripcion=insc, tipo='Final', defaults={'calificacion': 8})
                                count_notas += 1

                self.stdout.write(self.style.SUCCESS(f'>> Procesadas y limpiadas las materias.'))
                self.stdout.write(self.style.SUCCESS(f'>> Inyectadas inscripciones y notas para el lote actual ({count_inscripciones} inscripciones, {count_notas} finales).'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la migración: {e}'))
