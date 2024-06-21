from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from WorkStream.models import CustomUser, Priority, State, Task


class StateModelTest(TestCase):

    def test_create_state(self):
        state = State.objects.create(name="Backlog")
        self.assertEqual(state.name, "Backlog")

    def test_str_representation(self):
        state = State.objects.create(name="To do")
        self.assertEqual(str(state), "To do")

    def test_name_max_length(self):
        state = State(name="A" * 31)
        with self.assertRaises(ValidationError):
            state.full_clean()  # This will raise a ValueError if max_length is exceeded

    def test_unique_name(self):
        State.objects.create(name="Completed")
        with self.assertRaises(
            IntegrityError
        ):  # Captura IntegrityError en lugar de Exception
            State.objects.create(name="Completed")

    def test_update_state(self):
        state = State.objects.create(name="To Do")
        state.name = "Done"
        state.save()
        self.assertEqual(state.name, "Done")

    def test_delete_state(self):
        state = State.objects.create(name="Doing")
        state_id = state.id
        state.delete()
        with self.assertRaises(State.DoesNotExist):
            State.objects.get(id=state_id)


class PriorityModelTest(TestCase):
    def test_create_priority(self):
        priority = Priority.objects.create(name="Baja")
        self.assertEqual(priority.name, "Baja")

    def test_str_representation(self):
        priority = Priority.objects.create(name="Baja")
        self.assertEqual(str(priority), "Baja")

    def test_name_max_length(self):
        priority = Priority(name="A" * 31)
        with self.assertRaises(ValidationError):
            priority.full_clean()  # This will raise a ValueError if max_length is exceeded

    def test_unique_name(self):
        Priority.objects.create(name="Alta")
        with self.assertRaises(
            IntegrityError
        ):  # Captura IntegrityError en lugar de Exception
            Priority.objects.create(name="Alta")

    def test_update_priority(self):
        priority = Priority.objects.create(name="Media")
        priority.name = "Alta"
        priority.save()
        self.assertEqual(priority.name, "Alta")

    def test_delete_priority(self):
        priority = Priority.objects.create(name="Media")
        priority_id = priority.id
        priority.delete()
        with self.assertRaises(Priority.DoesNotExist):
            Priority.objects.get(id=priority_id)


class CustomUserModelTest(TestCase):
    def test_create_custom_user(self):
        user = CustomUser.objects.create(username="usuario1", password="password")
        self.assertEqual(user.username, "usuario1")

    def test_str_representation(self):
        user = CustomUser.objects.create(username="usuario2", password="password")
        self.assertEqual(str(user), "usuario2")

    def test_unique_username(self):
        CustomUser.objects.create(username="usuario3", password="password")
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(username="usuario3", password="password")

    def test_update_user(self):
        user = CustomUser.objects.create(username="usuario4", password="password")
        user.username = "usuario_actualizado"
        user.save()
        self.assertEqual(user.username, "usuario_actualizado")

    def test_delete_user(self):
        user = CustomUser.objects.create(username="usuario5", password="password")
        user_id = user.id
        user.delete()
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    def test_username_max_length(self):
        user = CustomUser(username="A" * 151, password="password")
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_unique_email(self):
        CustomUser.objects.create(
            username="usuario6", email="test@example.com", password="password"
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create(
                username="usuario7", email="test@example.com", password="password"
            )


class TaskModelTest(TestCase):
    def setUp(self):
        self.state = State.objects.create(name="Doing")
        self.priority = Priority.objects.create(name="Media")
        self.user = CustomUser.objects.create(username="admin", password="password")

    def test_create_task(self):
        task = Task.objects.create(
            name="Test tarea 1",
            description="Este es un test para la tarea 1",
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        task.assigned_users.set([self.user])
        self.assertEqual(task.name, "Test tarea 1")
        self.assertEqual(task.description, "Este es un test para la tarea 1")
        self.assertEqual(task.deadline, "2024-06-08")
        self.assertEqual(task.state, self.state)
        self.assertEqual(task.priority, self.priority)
        self.assertIn(self.user, task.assigned_users.all())
        self.assertEqual(task.owner, self.user)

    def test_str_representation(self):
        task = Task.objects.create(
            name="Test tarea 2",
            description="Descripción de la tarea 2",
            deadline="2024-06-09",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        self.assertEqual(str(task), f"tarea: Test tarea 2 en estado {self.state}")

    def test_task_name_max_length(self):
        task = Task(
            name="A" * 41,
            description="Descripción con nombre demasiado largo",
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_description_max_length(self):
        task = Task(
            name="Test tarea",
            description="A" * 256,
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_delete_task(self):
        task = Task.objects.create(
            name="Test tarea 3",
            description="Descripción de la tarea 3",
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        task_id = task.id
        task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

    def test_update_task(self):
        task = Task.objects.create(
            name="Test tarea 4",
            description="Descripción de la tarea 4",
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        task.name = "Tarea actualizada"
        task.save()
        self.assertEqual(task.name, "Tarea actualizada")

    def test_ordering_by_deadline(self):
        task1 = Task.objects.create(
            name="Task 1",
            description="First task",
            deadline="2024-06-08",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        task2 = Task.objects.create(
            name="Task 2",
            description="Second task",
            deadline="2024-06-07",
            state=self.state,
            priority=self.priority,
            owner=self.user,
        )
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)
        self.assertEqual(tasks[1], task1)
