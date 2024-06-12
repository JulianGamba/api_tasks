from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from WorkStream.models import State, Priority, CustomUser

class ViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='usuario', password='1234', email='test@gmail.com')
        self.client.force_authenticate(user=self.user)
        self.state = State.objects.create(name='pendiente')
        self.priority = Priority.objects.create(name='urgente')

    def test_state_list(self):
        # Prueba para listar estados
        url = reverse('state-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica que se obtenga el estado creado

    def test_create_state(self):
        # Prueba para crear un estado
        url = reverse('state-list')
        data = {'name': 'en progreso'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(State.objects.count(), 2)  # Verifica que se haya creado un nuevo estado
        self.assertEqual(State.objects.get(id=response.data['id']).name, 'en progreso')

    def test_priority_list(self):
        # Prueba para listar prioridades
        url = reverse('priority-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica que se obtenga la prioridad creada

    def test_create_priority(self):
        # Prueba para crear una prioridad
        url = reverse('priority-list')
        data = {'name': 'Media'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Priority.objects.count(), 2)  # Verifica que se haya creado una nueva prioridad

    def test_customuser_list(self):
        # Prueba para listar usuarios personalizados
        url = reverse('customuser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Verifica que se haya obtenido el usuario creado

    def test_create_customuser(self):
        # Prueba para crear un usuario personalizado
        url = reverse('customuser-list')
        data = {
            'username': 'nuevo usuario',
            'password': 'password1234',
            'email': 'test@gmail.com',
            'full_name': 'usuario',
            'avatar': None,
            'birth_date': '2001-08-13',
            'identification': '1198774233'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # Verifica que se haya creado un nuevo usuario

class AuthViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        # Prueba para registrar un usuario
        url = reverse('register')
        data = {
            'username': 'nuevo usuario',
            'password': 'password1234',
            'email': 'test@gmail.com',
            'full_name': 'nuevo usuario registrado',
            'avatar': None,
            'birth_date': '1990-01-01',
            'identification': '123456789'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)  # Verifica que se haya registrado un nuevo usuario

    def test_login(self):
        # Prueba para iniciar sesión
        self.user = CustomUser.objects.create_user(username='test usuario', password='12345', email='test@gmail.com')
        url = reverse('login')
        data = {
            'username': 'test usuario',
            'password': '12345'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Verifica que el token de acceso esté en la respuesta
