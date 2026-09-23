import os
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from gestion.models import Materia, PlanDeEstudio

class Command(BaseCommand):
    help = 'Repara el plan_id de las materias basado en carreras_materias original'

    def handle(self, *args, **options):
        file_path = r'/tmp/redarg_pdb.sql'
        if not os.path.exists(file_path):
            file_path = r'D:\Escritorio\Migracion\sql\redarg_pdb.sql'

        # Mapping of Legacy Carrera ID -> New PlanDeEstudio ID
        # 13 -> 1 (Sistemas)
        # 9, 10, 11 -> 2 (Cs Sagradas)
        # 16 -> 4 (Locucion 2019)
        # 17 -> 5 (Produccion TV)
        # 24 -> 8 (Locucion 2025)
        # Rest -> 9 (Historico)
        
        legacy_to_new = {
            13: 1,
            9: 2, 10: 2, 11: 2,
            16: 4, 7: 4, 8: 4, # Fallback older locucion to plan 4? Wait, new Plan 4 is "Res 63/SSPLINED/19" (ID 16). Legacy 7 and 8 are older locucion. I will map 7 and 8 to 9 (Historico) unless they want them merged. But let's map them to 9.
            17: 5,
            24: 8
        }

        materia_to_legacy_carrera = {}
        
        in_cm = False
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith("INSERT INTO `carreras_materias`"):
                    in_cm = True
                    continue
                if in_cm:
                    line = line.strip()
                    is_end = line.endswith(';')
                    if line.endswith(';') or line.endswith(','): line = line[:-1]
                    if line.startswith('('):
                        row = line[1:-1]
                        parts = next(csv.reader(StringIO(row), delimiter=',', quotechar="'", escapechar='\\'))
                        carrera_id = int(parts[1])
                        materia_id = int(parts[2])
                        # If a materia belongs to multiple careers (unlikely but possible), the latest one might override.
                        # Let's keep the highest priority mapping (e.g. non-historical > historical)
                        
                        current_carrera = materia_to_legacy_carrera.get(materia_id)
                        
                        # Si ya está y su carrera actual va a un plan válido (no 9), preferimos la válida
                        if current_carrera:
                            cur_new = legacy_to_new.get(current_carrera, 9)
                            prop_new = legacy_to_new.get(carrera_id, 9)
                            if prop_new != 9 and cur_new == 9:
                                materia_to_legacy_carrera[materia_id] = carrera_id
                            elif prop_new != 9 and cur_new != 9:
                                # Both valid? just overwrite or keep. We will keep current.
                                pass
                            else:
                                pass # Keep current if proposed is 9
                        else:
                            materia_to_legacy_carrera[materia_id] = carrera_id

                    if is_end:
                        break

        plan_historico = 9
        modificadas = 0
        
        for materia in Materia.objects.all():
            carrera_id_legacy = materia_to_legacy_carrera.get(materia.id)
            if carrera_id_legacy:
                nuevo_plan_id = legacy_to_new.get(carrera_id_legacy, plan_historico)
            else:
                nuevo_plan_id = plan_historico # No mapping? Historico
                
            if materia.plan_id != nuevo_plan_id:
                materia.plan_id = nuevo_plan_id
                materia.save(update_fields=['plan_id'])
                modificadas += 1
                
        self.stdout.write(f"Modificadas {modificadas} materias de plan.")