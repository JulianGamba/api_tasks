from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from WorkStream.models import Task, State, Priority, CustomUser, Comment


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
            'username': 'nuevo ',
            'password': '1234',
            'email': 'testing@gmail.com',
            'full_name': 'usuario',
            'avatar': None,
            'birth_date': '2001-08-13',
            'identification': '1198774233'
        }
          # Verificar que no existe un usuario con el mismo nombre de usuario
        try:
            CustomUser.objects.get(username=data['username'])
            self.fail(f'User with username {data["username"]} already exists.')
        except CustomUser.DoesNotExist:
            pass
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # Verifica que se haya creado un nuevo usuario
        
        
class CommentAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.comment = Comment.objects.create(content="Test comment", user=self.user)
        self.comment_url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        self.comments_url = reverse('comment-list')

    def test_create_comment(self):
        data = {'content': 'New test comment'}
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.latest('id').content, 'New test comment')

    def test_list_comments(self):
        response = self.client.get(self.comments_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.comment.content)

    def test_retrieve_comment(self):
        response = self.client.get(self.comment_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.comment.content)

    def test_update_comment(self):
        data = {'content': 'Updated test comment'}
        response = self.client.put(self.comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated test comment')

    def test_partial_update_comment(self):
        data = {'content': 'Partially updated test comment'}
        response = self.client.patch(self.comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Partially updated test comment')

    def test_delete_comment(self):
        response = self.client.delete(self.comment_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
        
class AuthViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_register(self):
        # Prueba para registrar un usuario
        
        data = {
            'username': 'nuevo_usuario',
            'password': 'password1234',
            'email': 'test@gmail.com',
            'full_name': 'nuevo usuario registrado',
            'avatar': None,
            'birth_date': '1990-01-01',
            'identification': '123456789'
        }

        # Verificar que no existe un usuario con el mismo nombre de usuario
        self.assertFalse(CustomUser.objects.filter(username=data['username']).exists(), 
                         f'User with username {data["username"]} already exists.')

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username=data['username']).exists())
        self.assertEqual(CustomUser.objects.count(), 1)  # Verifica que se haya registrado un nuevo usuario

    def test_login(self):
        # Prueba para iniciar sesión
        self.user = CustomUser.objects.create_user(username='nuevo_usuario', password='password1234', email='test@gmail.com')
        
        data = {
            'username': 'nuevo_usuario',
            'password': 'password1234'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Verifica que el token de acceso esté en la respuesta

    def tearDown(self):
        CustomUser.objects.all().delete()
        
