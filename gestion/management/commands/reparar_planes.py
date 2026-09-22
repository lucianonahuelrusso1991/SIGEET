import os
from django.core.management.base import BaseCommand
from gestion.models import PlanDeEstudio, Materia
import csv
from io import StringIO

class Command(BaseCommand):
    help = 'Repara los planes de estudio extrayendo las materias exactas del SQL de produccion'

    def handle(self, *args, **options):
        sql_file = '/tmp/redarg_pdb.sql'
        if not os.path.exists(sql_file):
            self.stdout.write(self.style.ERROR('No se encontro el archivo /tmp/redarg_pdb.sql'))
            return
            
        def normalize(n):
            return n.lower().strip().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace(' ', '')
        
        cm_map = {}
        in_cm = False
        with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('INSERT INTO `carreras_materias`'): in_cm = True; continue
                if in_cm:
                    line = line.strip()
                    is_end = line.endswith(';')
                    if line.endswith(';') or line.endswith(','): line = line[:-1]
                    if line.startswith('('):
                        sio = StringIO(line[1:-1])
                        try:
                            parts = next(csv.reader(sio, delimiter=',', quotechar="'", escapechar='\\', skipinitialspace=True))
                            c_id = parts[1].strip()
                            m_id = parts[2].strip()
                            anio = parts[4].strip() if len(parts) > 4 else '1'
                            if c_id not in cm_map: cm_map[c_id] = []
                            cm_map[c_id].append((m_id, anio))
                        except: pass
                    if is_end: in_cm = False
                            
        m_map = {}
        in_m = False
        with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('INSERT INTO `materias`'): in_m = True; continue
                if in_m:
                    line = line.strip()
                    is_end = line.endswith(';')
                    if line.endswith(';') or line.endswith(','): line = line[:-1]
                    if line.startswith('('):
                        sio = StringIO(line[1:-1])
                        try:
                            parts = next(csv.reader(sio, delimiter=',', quotechar="'", escapechar='\\', skipinitialspace=True))
                            m_id = parts[0].strip()
                            m_name = parts[1].strip()
                            m_map[m_id] = m_name
                        except: pass
                    if is_end: in_m = False
                    
        plan_sagradas = PlanDeEstudio.objects.filter(nombre__icontains='Sagradas').first()
        plan_tv = PlanDeEstudio.objects.filter(nombre__icontains='Televis').first()
        plan_sistemas = PlanDeEstudio.objects.filter(nombre__icontains='Sistemas').first()
        plan_loc19 = PlanDeEstudio.objects.filter(nombre__icontains='Locuci').filter(nombre__icontains='19').first()
        plan_loc25 = PlanDeEstudio.objects.filter(nombre__icontains='Locuci').filter(nombre__icontains='2025').first()
        plan_hist = PlanDeEstudio.objects.filter(nombre__icontains='Hist').first()
        
        target_carreras = {
            '9': plan_sagradas,
            '17': plan_tv,
            '13': plan_sistemas,
            '16': plan_loc19,
            '8': plan_loc19,
            '24': plan_loc25
        }
        
        for c_id, django_plan in target_carreras.items():
            if not django_plan: continue
            self.stdout.write(f"\n--- Sincronizando {django_plan.nombre} (ID Legacy: {c_id}) ---")
            
            legacy_items = cm_map.get(c_id, [])
            if not legacy_items:
                self.stdout.write(f"No se encontraron materias legacy en SQL para carrera {c_id}")
                continue
                
            legacy_names = []
            for m_id, anio in legacy_items:
                n = m_map.get(m_id)
                if n: legacy_names.append((n, anio))
                
            self.stdout.write(f"Materias legacy esperadas en base de datos vieja: {len(legacy_names)}")
            
            django_subjects = list(Materia.objects.filter(plan=django_plan))
            django_names_norm = [normalize(s.nombre) for s in django_subjects]
            
            agregadas = 0
            for l_name, anio in legacy_names:
                norm_l = normalize(l_name)
                match = False
                for dn in django_names_norm:
                    if norm_l in dn or dn in norm_l:
                        match = True
                        break
                
                if not match:
                    hist_match = None
                    for hm in Materia.objects.filter(plan=plan_hist):
                        if normalize(hm.nombre) == norm_l or norm_l in normalize(hm.nombre) or normalize(hm.nombre) in norm_l:
                            hist_match = hm
                            break
                    
                    if hist_match:
                        self.stdout.write(f"Recuperando de Histórico: {hist_match.nombre}")
                        hist_match.plan = django_plan
                        hist_match.save()
                        django_names_norm.append(normalize(hist_match.nombre))
                        agregadas += 1
                    else:
                        try: anio_int = int(anio)
                        except: anio_int = 1
                        self.stdout.write(f"Creando nueva materia que faltaba: {l_name}")
                        Materia.objects.create(nombre=l_name, plan=django_plan, ao_dictado=anio_int, cuatrimestre_dictado='AN')
                        django_names_norm.append(norm_l)
                        agregadas += 1
                        
            self.stdout.write(f"Agregadas/Recuperadas: {agregadas}")
            
            sobrantes = 0
            legacy_norm = [normalize(n) for n, _ in legacy_names]
            
            for ds in Materia.objects.filter(plan=django_plan):
                norm_d = normalize(ds.nombre)
                match = False
                for ln in legacy_norm:
                    if norm_d in ln or ln in norm_d:
                        match = True
                        break
                
                if not match:
                    ds.plan = plan_hist
                    ds.save()
                    sobrantes += 1
                    self.stdout.write(f"  -> Movida a Historico (sobraba segun SQL viejo): {ds.nombre}")
                    
            self.stdout.write(f"Sobrantes movidas a hist: {sobrantes}")

        self.stdout.write(self.style.SUCCESS('Sincronizacion de planes completa!'))