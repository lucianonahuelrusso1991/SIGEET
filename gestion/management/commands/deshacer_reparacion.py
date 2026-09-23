import os
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Revierte reparar_inscripciones moviendo todo de vuelta a las comisiones por nombre'
    def handle(self, *args, **options):
        from gestion.models import Alumno, Materia, Comision, Inscripcion, MesaExamen, InscripcionMesa
        def normalize(n): return n.lower().strip().replace('ǭ','a').replace('Ǹ','e').replace('','i').replace('','o').replace('ǧ','u').replace('','n').replace(' ', '')

        self.stdout.write(">> Revirtiendo inscripciones...")
        
        # 1. Encontrar todas las comisiones nuevas creadas (tienen docente=None y cuatrimestre='AN' y no hay ID legado)
        # O ms fcil: iterar todas las Inscripciones y si la Comision actual NO tiene docente, y hay OTRA con docente o creada antes para el MISMO nombre y ao, la movemos ah.
        
        # Primero indexamos las comisiones "buenas" (las que cre fase5 con ids legados o profesores)
        comisiones_buenas = {}
        # Asumimos que las creadas por fase5 tienen id <= 50000 o docente != None.
        for c in Comision.objects.all():
            n = normalize(c.materia.nombre)
            key = (n, c.ciclo_lectivo)
            # Preferir las que tienen docente o id menor
            if key not in comisiones_buenas:
                comisiones_buenas[key] = c
            else:
                curr = comisiones_buenas[key]
                if (c.docente is not None and curr.docente is None) or (c.id < curr.id and c.docente == curr.docente):
                    comisiones_buenas[key] = c

        movidas = 0
        with transaction.atomic():
            for ins in Inscripcion.objects.select_related('comision__materia'):
                c = ins.comision
                # Si la comision actual parece una generada por mi script (docente=None, cuatrimestre='AN')
                # Y existe una mejor en el cache
                n = normalize(c.materia.nombre)
                mejor = comisiones_buenas.get((n, c.ciclo_lectivo))
                if mejor and mejor.id != c.id:
                    # si la "mejor" fue creada antes (id menor), la movemos
                    if mejor.id < c.id:
                        ins.comision = mejor
                        ins.save(update_fields=['comision'])
                        movidas += 1
                        
        self.stdout.write(f"Inscripciones devueltas a su lugar original: {movidas}")

        self.stdout.write(">> Revirtiendo mesas...")
        mesas_buenas = {}
        for m in MesaExamen.objects.all():
            n = normalize(m.materia.nombre)
            fecha = m.fecha_hora.date()
            key = (n, fecha)
            if key not in mesas_buenas:
                mesas_buenas[key] = m
            else:
                curr = mesas_buenas[key]
                if m.id < curr.id:
                    mesas_buenas[key] = m
                    
        movidas_mesas = 0
        with transaction.atomic():
            for ins in InscripcionMesa.objects.select_related('mesa__materia'):
                m = ins.mesa
                n = normalize(m.materia.nombre)
                fecha = m.fecha_hora.date()
                mejor = mesas_buenas.get((n, fecha))
                if mejor and mejor.id != m.id:
                    if mejor.id < m.id:
                        ins.mesa = mejor
                        ins.save(update_fields=['mesa'])
                        movidas_mesas += 1

        self.stdout.write(f"Inscripciones a Mesas devueltas a su lugar original: {movidas_mesas}")
