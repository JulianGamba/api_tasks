from datetime import datetime

from rest_framework.test import APIRequestFactory, APITestCase

from WorkStream.models import Comment, CustomUser, Priority, State, Task
from WorkStream.serializers import (
    CommentSerializer,
    CustomUserSerializer,
    LoginSerializer,
    PrioritySerializer,
    StateSerializer,
    TaskReadSerializer,
    TaskWriteSerializer,
)


class StateSerializerTest(APITestCase):

    def setUp(self):
        self.state_data = {"name": "Backlog"}
        self.state_data2 = {"name": "Done"}
        self.state = State.objects.create(name="Backlog")
        self.state2 = State.objects.create(name="Doing")
        self.factory = APIRequestFactory()

    def test_state_serialization(self):
        serializer = StateSerializer(self.state)
        data = serializer.data
        self.assertEqual(data["name"], self.state.name)

    def test_state_deserialization(self):
        request = self.factory.post("/states/", self.state_data2, format="json")
        serializer = StateSerializer(
            data=self.state_data2, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        state = serializer.save()
        self.assertEqual(state.name, self.state_data2["name"])

    def test_state_invalid_data(self):
        invalid_data = {"name": ""}
        request = self.factory.post("/states/", invalid_data, format="json")
        serializer = StateSerializer(data=invalid_data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_state_partial_update(self):
        partial_data = {"name": "In pogress"}
        request = self.factory.patch(
            f"/states/{self.state.id}", partial_data, format="json"
        )
        serializer = StateSerializer(
            self.state, data=partial_data, partial=True, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        state = serializer.save()
        self.assertEqual(state.name, partial_data["name"])


class PrioritySerializerTest(APITestCase):

    def setUp(self):
        self.priority_data = {"name": "Alta"}
        self.priority_data2 = {"name": "Media"}
        self.priority = Priority.objects.create(name="Alta")
        self.factory = APIRequestFactory()

    def test_priority_serialization(self):
        serializer = PrioritySerializer(self.priority)
        data = serializer.data
        self.assertEqual(self.priority.name, data["name"])

    def test_priority_deserialization(self):
        request = self.factory.post("/prioritys/", self.priority_data2, format="json")
        serializer = PrioritySerializer(
            data=self.priority_data2, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        priority = serializer.save()
        self.assertEqual(priority.name, self.priority_data2["name"])

    def test_priority_invalid_data(self):
        invalid_data = {"name": ""}
        request = self.factory.post("/prioritys/", invalid_data, format="json")
        serializer = PrioritySerializer(data=invalid_data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_priority_partial_update(self):
        partial_data = {"name": "Baja"}
        request = self.factory.patch(
            f"/prioritys/{self.priority.id}", partial_data, format="json"
        )
        serializer = PrioritySerializer(
            self.priority, data=partial_data, partial=True, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        priority = serializer.save()
        self.assertEqual(priority.name, partial_data["name"])


class CustomUserSerializerTest(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "user_test",
            "password": "password",
            "email": "user_test@example.com",
            "full_name": "User Test",
            "avatar": None,
            "birth_date": "1990-01-01",
            "identification": 1234567890,
        }
        self.user = CustomUser.objects.create_user(
            username="user_test",
            password="password",
            email="user_test@example.com",
            full_name="User Test",
            avatar=None,
            birth_date="1990-01-01",
            identification=1234567890,
        )
        self.factory = APIRequestFactory()

    def test_user_serialization(self):
        serializer = CustomUserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["full_name"], self.user.full_name)
        self.assertEqual(data["birth_date"], str(self.user.birth_date))
        self.assertEqual(data["identification"], self.user.identification)

    def test_user_deserialization(self):
        CustomUser.objects.filter(
            username=self.user_data["username"]
        ).delete()  # Eliminar si existe
        request = self.factory.post("/users/", self.user_data, format="json")
        serializer = CustomUserSerializer(
            data=self.user_data, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, self.user_data["username"])
        self.assertTrue(
            user.check_password(self.user_data["password"])
        )  # Verifica que la contraseña se estableció correctamente
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.full_name, self.user_data["full_name"])
        self.assertEqual(
            user.birth_date,
            datetime.strptime(self.user_data["birth_date"], "%Y-%m-%d").date(),
        )
        self.assertEqual(user.identification, self.user_data["identification"])

    def test_user_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data["username"] = ""
        request = self.factory.post("/users/", invalid_data, format="json")
        serializer = CustomUserSerializer(
            data=invalid_data, context={"request": request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_user_partial_update(self):
        self.user = CustomUser.objects.create_user(
            username="user_test2",
            password="password",
            email="user_test2@example.com",
            full_name="User Test 2",
            avatar=None,
            birth_date="1990-01-01",
            identification=1234567890,
        )
        partial_data = {"full_name": "New Name"}
        request = self.factory.patch(
            f"/users/{self.user.id}/", partial_data, format="json"
        )
        serializer = CustomUserSerializer(
            self.user, data=partial_data, partial=True, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.full_name, partial_data["full_name"])
        self.assertEqual(
            user.username, self.user.username
        )  # Ensure other fields are unchanged


class TaskSerializerTest(APITestCase):

    def setUp(self):
        self.state = State.objects.create(name="Doing")
        self.priority = Priority.objects.create(name="Alta")
        self.user = CustomUser.objects.create_user(
            username="user_test", email="user_test@gmail.com", password="password"
        )
        self.another_user = CustomUser.objects.create_user(
            username="anotheruser", email="anotheruser@gmail.com", password="password"
        )

        # Primero crea la tarea
        self.task = Task.objects.create(
            name="Test tarea 1",
            description="Este es un test para la tarea 1",
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        self.task.assigned_users.set([self.user, self.another_user])

        # Luego crea el comentario y asocialo a la tarea
        self.comment = Comment.objects.create(
            task=self.task,
            user=self.user,
            text="Este es un comentario asociado a la tarea",
        )

        self.task_data = {
            "name": "Test tarea 1",
            "description": "Este es el test de la tarea 1",
            "deadline": "2024-06-08",
            "comments": [{"text": "Comentario 1"}, {"text": "Comentario 2"}],
            "state": self.state.id,
            "priority": self.priority.id,
            "assigned_users": [self.user.id, self.another_user.id],
            "owner": self.user.id,
        }

        self.factory = APIRequestFactory()

    def test_task_read_serialization(self):
        serializer = TaskReadSerializer(self.task)
        data = serializer.data
        self.assertEqual(data["name"], self.task.name)
        self.assertEqual(data["description"], self.task.description)
        self.assertEqual(data["deadline"], str(self.task.deadline))
        self.assertEqual(data["state"]["id"], self.task.state.id)
        self.assertEqual(data["priority"]["id"], self.task.priority.id)
        self.assertEqual(len(data["assigned_users"]), 2)
        self.assertEqual(data["owner"]["id"], self.task.owner.id)
        self.assertEqual(len(data["comments"]), 1)
        self.assertEqual(data["comments"][0]["text"], self.comment.text)

    def test_task_write_serialization(self):
        request = self.factory.post("/tasks/", self.task_data, format="json")
        request.user = self.user
        serializer = TaskWriteSerializer(
            data=self.task_data, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        task = serializer.save()
        self.assertEqual(task.name, self.task_data["name"])
        self.assertEqual(task.description, self.task_data["description"])
        task_deadline = datetime.strptime(self.task_data["deadline"], "%Y-%m-%d").date()
        self.assertEqual(task.deadline, task_deadline)
        # self.assertEqual(task.comment.id, self.comment.id)
        self.assertEqual(task.state.id, self.task_data["state"])
        self.assertEqual(task.priority.id, self.task_data["priority"])
        self.assertEqual(
            list(task.assigned_users.all()), [self.user, self.another_user]
        )
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.comments.count(), 2)
        self.assertEqual(task.comments.first().text, "Comentario 1")

    def test_task_invalid_data(self):
        invalid_data = self.task_data.copy()
        invalid_data["deadline"] = "invalid-date"
        request = self.factory.post("/tasks/", invalid_data, format="json")
        request.user = self.user
        serializer = TaskWriteSerializer(
            data=invalid_data, context={"request": request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("deadline", serializer.errors)

    def test_task_missing_name(self):
        """Test serialization with missing name field."""
        invalid_data = self.task_data.copy()
        del invalid_data["name"]
        request = self.factory.post("/tasks/", invalid_data, format="json")
        request.user = self.user
        serializer = TaskWriteSerializer(
            data=invalid_data, context={"request": request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_task_missing_comment(self):
        """Test serialization without comments field."""
        valid_data = self.task_data.copy()
        if "comments" in valid_data:
            del valid_data["comments"]
        request = self.factory.post("/tasks/", valid_data, format="json")
        request.user = self.user
        serializer = TaskWriteSerializer(data=valid_data, context={"request": request})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("comments", serializer.errors)

    def test_task_partial_update(self):
        """Test partial update serialization of a Task."""
        partial_data = {"description": "Nueva descripción"}
        request = self.factory.patch(
            f"/tasks/{self.task.id}/", partial_data, format="json"
        )
        request.user = self.user
        serializer = TaskWriteSerializer(
            self.task, data=partial_data, partial=True, context={"request": request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        task = serializer.save()
        self.assertEqual(task.description, partial_data["description"])
        self.assertEqual(task.name, self.task.name)  # Ensure other fields are unchanged
