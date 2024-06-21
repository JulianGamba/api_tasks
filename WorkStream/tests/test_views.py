import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from WorkStream.models import Comment, CustomUser, Priority, State, Task


class ViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="usuario", password="1234", email="test@gmail.com"
        )
        self.client.force_authenticate(user=self.user)
        self.state = State.objects.create(name="pendiente")
        self.priority = Priority.objects.create(name="urgente")

    def test_state_list(self):
        # Prueba para listar estados
        url = reverse("state-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Verifica que se obtenga el estado creado

    def test_create_state(self):
        # Prueba para crear un estado
        url = reverse("state-list")
        data = {"name": "en progreso"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            State.objects.count(), 2
        )  # Verifica que se haya creado un nuevo estado
        self.assertEqual(State.objects.get(id=response.data["id"]).name, "en progreso")

    def test_priority_list(self):
        # Prueba para listar prioridades
        url = reverse("priority-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Verifica que se obtenga la prioridad creada

    def test_create_priority(self):
        # Prueba para crear una prioridad
        url = reverse("priority-list")
        data = {"name": "Media"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Priority.objects.count(), 2
        )  # Verifica que se haya creado una nueva prioridad

    def test_customuser_list(self):
        # Prueba para listar usuarios personalizados
        url = reverse("customuser-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # Verifica que se haya obtenido el usuario creado

    def test_create_customuser(self):
        # Prueba para crear un usuario personalizado
        url = reverse("customuser-list")
        data = {
            "username": "nuevo ",
            "password": "1234",
            "email": "testing@gmail.com",
            "full_name": "usuario",
            "avatar": None,
            "birth_date": "2001-08-13",
            "identification": "1198774233",
        }
        # Verificar que no existe un usuario con el mismo nombre de usuario
        try:
            CustomUser.objects.get(username=data["username"])
            self.fail(f'User with username {data["username"]} already exists.')
        except CustomUser.DoesNotExist:
            pass

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            CustomUser.objects.count(), 2
        )  # Verifica que se haya creado un nuevo usuario


User = get_user_model()


@pytest.mark.django_db
class TestCommentViews:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass123"
        )

    @pytest.fixture
    def task(self, user):
        return Task.objects.create(
            title="Test Task", description="Task description", user=user
        )

    @pytest.fixture
    def client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_list_comments(self, client, task):
        Comment.objects.bulk_create(
            [
                Comment(text="Comment 1", task=task, user=task.user),
                Comment(text="Comment 2", task=task, user=task.user),
                Comment(text="Comment 3", task=task, user=task.user),
            ]
        )
        url = reverse("comment-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_comment(self, client, user, task):
        url = reverse("comment-create")
        data = {
            "text": "This is a test comment",
            "task": task.id,
            "assigned_users": [user.id],
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["text"] == "This is a test comment"
        assert response.data["task"] == task.id

    def test_create_comment_invalid_task(self, client):
        url = reverse("comment-create")
        data = {
            "text": "This is a test comment",
            "task": 999,  # Asume que esta tarea no existe
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_retrieve_comment(self, client, task):
        comment = Comment.objects.create(text="Test comment", task=task, user=task.user)
        url = reverse("comment-detail", kwargs={"comment_id": comment.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == comment.text

    def test_update_comment(self, client, task):
        comment = Comment.objects.create(text="Test comment", task=task, user=task.user)
        url = reverse("comment-detail", kwargs={"comment_id": comment.id})
        data = {"text": "Updated comment text"}
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == "Updated comment text"

    def test_delete_comment(self, client, task):
        comment = Comment.objects.create(text="Test comment", task=task, user=task.user)
        url = reverse("comment-detail", kwargs={"comment_id": comment.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Comment.objects.filter(id=comment.id).count() == 0


class AuthViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def test_register(self):
        # Prueba para registrar un usuario

        data = {
            "username": "nuevo_usuario",
            "password": "password1234",
            "email": "test@gmail.com",
            "full_name": "nuevo usuario registrado",
            "avatar": None,
            "birth_date": "1990-01-01",
            "identification": "123456789",
        }

        # Verificar que no existe un usuario con el mismo nombre de usuario
        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists(),
            f'User with username {data["username"]} already exists.',
        )

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username=data["username"]).exists())
        self.assertEqual(
            CustomUser.objects.count(), 1
        )  # Verifica que se haya registrado un nuevo usuario

    def test_login(self):
        # Prueba para iniciar sesión
        self.user = CustomUser.objects.create_user(
            username="nuevo_usuario", password="password1234", email="test@gmail.com"
        )

        data = {"username": "nuevo_usuario", "password": "password1234"}

        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "access", response.data
        )  # Verifica que el token de acceso esté en la respuesta

    def tearDown(self):
        CustomUser.objects.all().delete()
