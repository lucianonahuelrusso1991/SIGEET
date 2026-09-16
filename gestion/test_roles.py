from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from gestion.models import PlanDeEstudio, Docente
from gestion.views import obtener_planes_visibles, es_solo_tutor

class RolesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear un usuario admin para loguear y crear datos si es necesario (o lo creamos directo)
        self.user = User.objects.create_user(username='tutor', password='password123', is_staff=True)
        
        # Crear Plan de Estudio de prueba
        self.plan1 = PlanDeEstudio.objects.create(nombre='Plan 1', resolucion_ministerial='RES-1')
        self.plan2 = PlanDeEstudio.objects.create(nombre='Plan 2', resolucion_ministerial='RES-2')
        
        # Crear Docente de prueba vinculado al usuario
        self.docente = Docente.objects.create(
            nombre='Juan', apellido='Perez', dni='12345678', email='tutor@test.com',
            usuario=self.user
        )
        # Asignarle el rol de tutor
        self.docente.carreras_tutoriadas.add(self.plan1)
        
    def test_es_solo_tutor(self):
        self.assertTrue(es_solo_tutor(self.user))
        
    def test_obtener_planes_visibles(self):
        planes = obtener_planes_visibles(self.user)
        self.assertEqual(list(planes), [self.plan1.id])
        
    def test_accesos_tutor(self):
        self.client.login(username='tutor', password='password123')
        
        # alta_alumno
        response = self.client.get(reverse('alta_alumno'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('lista_alumnos'))
        
        # alta_comision
        response = self.client.get(reverse('alta_comision'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
        
        # apertura_masiva
        response = self.client.get(reverse('apertura_masiva'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_asignar_coordinador(self):
        self.docente.carreras_coordinadas.add(self.plan2)
        self.assertFalse(es_solo_tutor(self.user))
