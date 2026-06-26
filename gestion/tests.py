from django.test import TestCase, Client
from django.contrib.auth.models import User
from gestion.models import PlanDeEstudio, Materia, Correlatividad, Comision, Alumno, Inscripcion

class InscripcionCursadaTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alumno1', password='password123')
        self.plan = PlanDeEstudio.objects.create(nombre='Plan Test', resolucion_ministerial='123/20')
        
        self.materia1 = Materia.objects.create(nombre='Materia 1', plan=self.plan, año_dictado=1, cuatrimestre_dictado='1C')
        self.materia2 = Materia.objects.create(nombre='Materia 2', plan=self.plan, año_dictado=1, cuatrimestre_dictado='2C')
        
        # M1 es requisito (CUR) para M2
        Correlatividad.objects.create(materia=self.materia2, requisito=self.materia1, tipo='CUR')
        
        self.comision_m2 = Comision.objects.create(
            materia=self.materia2, 
            ciclo_lectivo=2026, 
            cuatrimestre='2C', 
            inscripciones_abiertas=True, 
            cerrada=False
        )
        
        self.alumno = Alumno.objects.create(
            usuario=self.user,
            dni='12345678',
            nombre='Juan',
            apellido='Perez',
            plan=self.plan,
            estado_alumno='ACT'
        )

    def test_inscripcion_cursada_permite_sin_correlativa(self):
        # El alumno no tiene M1 aprobada ni regularizada
        self.client.login(username='alumno1', password='password123')
        
        response = self.client.post('/mi-inscripcion-cursadas/', {
            'action': 'inscribir',
            'comision_id': self.comision_m2.id
        })
        
        # SÍ debería haberse creado la inscripción porque las correlativas no bloquean cursadas (por regla de negocio)
        inscrito = Inscripcion.objects.filter(alumno=self.alumno, comision=self.comision_m2).exists()
        self.assertTrue(inscrito, "El sistema NO permitió la inscripción, pero debería permitir cursar sin correlativas.")

    def test_inscripcion_alumno_inactivo(self):
        self.alumno.estado_alumno = 'INA'
        self.alumno.save()
        
        # Forzar que M1 no sea requerida para probar solo el estado
        Correlatividad.objects.all().delete()

        self.client.login(username='alumno1', password='password123')
        
        response = self.client.post('/mi-inscripcion-cursadas/', {
            'action': 'inscribir',
            'comision_id': self.comision_m2.id
        })
        
        inscrito = Inscripcion.objects.filter(alumno=self.alumno, comision=self.comision_m2).exists()
        self.assertFalse(inscrito, "El sistema permitió la inscripción de un alumno con estado INACTIVO.")
