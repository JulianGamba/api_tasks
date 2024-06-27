import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

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


@pytest.mark.django_db
def test_list_comments(api_client, comment):
    url = reverse("comment-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["text"] == comment.text


@pytest.mark.django_db
def test_create_comment(api_client, task):
    url = reverse("comment-create")
    data = {"text": "New test comment", "task": task.id}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == "New test comment"


@pytest.mark.django_db
def test_retrieve_comment(api_client, comment):
    url = reverse("comment-detail", args=[comment.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == comment.text


@pytest.mark.django_db
def test_update_comment(api_client, comment, task):
    url = reverse("comment-detail", args=[comment.id])
    data = {"text": "Updated comment text", "task": task.id}
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK, (
        f"Expected status 200, but got {response.status_code}. "
        f"Response data: {response.data}"
    )
    comment.refresh_from_db()

    assert (
        comment.text == "Updated comment text"
    ), f"Expected comment text 'Updated comment text', but got '{comment.text}'"


@pytest.mark.django_db
def test_delete_comment(api_client, comment):
    url = reverse("comment-detail", args=[comment.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_delete_comment_unauthorized(api_client, user, another_user, task):
    comment = Comment.objects.create(text="Test Comment", user=user, task=task)
    url = reverse("comment-detail", args=[comment.id])

    # Forzar autenticación con otro usuario
    api_client.force_authenticate(user=another_user)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Comment.objects.count() == 1


class AuthViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def test_register(self):
        # Prueba para registrar un usuario

        data = {
            "password": "password1234",
            "email": "test@gmail.com",
            "full_name": "nuevo usuario registrado",
            "avatar": None,
            "birth_date": "1990-01-01",
            "identification": "123456789",
        }

        # Verificar que no existe un usuario con el mismo correo electrónico
        self.assertFalse(
            CustomUser.objects.filter(email=data["email"]).exists(),
            f'User with email {data["email"]} already exists.',
        )

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar que se haya creado el usuario y que el username sea el correo electrónico sin la parte del dominio
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())
        user = CustomUser.objects.get(email=data["email"])
        expected_username = data["email"].split("@")[0]
        self.assertEqual(user.username, expected_username)

        # Verificar que solo haya un usuario registrado
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_login(self):
        # Prueba para iniciar sesión
        data_register = {"password": "password1234", "email": "test@gmail.com"}
        self.client.post(self.register_url, data_register, format="json")

        data_login = {"password": "password1234", "username": "test"}
        response = self.client.post(self.login_url, data_login, format="json")
        print(response.json())
        print(CustomUser.objects.first().email, CustomUser.objects.first().username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que el token de acceso esté en la respuesta
        self.assertIn("access", response.data)

    def tearDown(self):
        CustomUser.objects.all().delete()
