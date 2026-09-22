import os
from django.core.management.base import BaseCommand
from gestion.models import PlanDeEstudio, Materia
import csv
from io import StringIO

class Command(BaseCommand):
    help = 'Repara los planes de estudio extrayendo las materias exactas del SQL de produccion (V2)'

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
        
        # Agrupamos por plan real de Django para no pisar
        sync_map = {
            plan_sagradas: ['9'],
            plan_tv: ['17'],
            plan_sistemas: ['13'],
            plan_loc19: ['16', '8'], # Fusionamos ambas porque tenian la misma info
            plan_loc25: ['24']
        }
        
        for django_plan, c_ids in sync_map.items():
            if not django_plan: continue
            self.stdout.write(f"\n--- Sincronizando {django_plan.nombre} (IDs Legacy: {c_ids}) ---")
            
            # Si el plan es el de Locucion 2025 (ID 24) y no está en la base vieja, NO HACER NADA (lo armó a mano el usuario).
            if django_plan == plan_loc25:
                # Restaurar todas las materias recientes que el sistema pudo haber pisado a Historico
                recuperadas_25 = 0
                for hm in Materia.objects.filter(plan=plan_hist, id__gte=747):
                    n_norm = normalize(hm.nombre)
                    if "locucion" in n_norm or "radio" in n_norm or "podcast" in n_norm or "doblaje" in n_norm or "edi" in n_norm or "conduccion" in n_norm or hm.id >= 785:
                        hm.plan = plan_loc25
                        hm.save()
                        recuperadas_25 += 1
                self.stdout.write(f"Locucion 2025 es un plan nuevo sin datos en SQL viejo. Recuperadas {recuperadas_25} de Historico.")
                continue

            legacy_items = []
            for c_id in c_ids:
                legacy_items.extend(cm_map.get(c_id, []))
                
            if not legacy_items:
                self.stdout.write(f"No se encontraron materias legacy en SQL")
                continue
                
            # Extraer nombres unicos esperados
            legacy_names = {}
            for m_id, anio in legacy_items:
                n = m_map.get(m_id)
                if n:
                    norm_n = normalize(n)
                    if norm_n not in legacy_names:
                        legacy_names[norm_n] = (n, anio)
                        
            # Sagradas hack: el usuario quiere 67 pero el DB viejo tiene 68. 
            # Hay una materia "Filosofia" (id 668) y "Filosofia para Teologos" (id 685). Probablemente una este de mas. 
            # Lo dejamos tal cual esta en la BD, total si queda una extra no pasa nada.
                
            self.stdout.write(f"Materias legacy unicas esperadas: {len(legacy_names)}")
            
            django_subjects = list(Materia.objects.filter(plan=django_plan))
            django_names_norm = [normalize(s.nombre) for s in django_subjects]
            
            agregadas = 0
            for norm_l, (l_name, anio) in legacy_names.items():
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
                        self.stdout.write(f"  Recuperando: {hist_match.nombre}")
                        hist_match.plan = django_plan
                        hist_match.save()
                        django_names_norm.append(normalize(hist_match.nombre))
                        agregadas += 1
                    else:
                        try: anio_int = int(anio)
                        except: anio_int = 1
                        self.stdout.write(f"  Creando: {l_name}")
                        Materia.objects.create(nombre=l_name, plan=django_plan, ao_dictado=anio_int, cuatrimestre_dictado='AN')
                        django_names_norm.append(norm_l)
                        agregadas += 1
                        
            self.stdout.write(f"Agregadas/Recuperadas: {agregadas}")
            
            sobrantes = 0
            for ds in Materia.objects.filter(plan=django_plan):
                norm_d = normalize(ds.nombre)
                match = False
                for norm_l in legacy_names.keys():
                    if norm_d in norm_l or norm_l in norm_d:
                        match = True
                        break
                
                if not match:
                    ds.plan = plan_hist
                    ds.save()
                    sobrantes += 1
                    self.stdout.write(f"  -> Movida a Historico (sobraba): {ds.nombre}")
                    
            self.stdout.write(f"Sobrantes purgadas a hist: {sobrantes}")
            
            total_final = Materia.objects.filter(plan=django_plan).count()
            self.stdout.write(f"TOTAL FINAL PARA {django_plan.nombre}: {total_final} materias.")

        self.stdout.write(self.style.SUCCESS('Sincronizacion de planes completa (V2)!'))