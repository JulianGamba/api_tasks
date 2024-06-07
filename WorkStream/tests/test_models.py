from django.test import TestCase
from WorkStream.models import State, Priority, CustomUser, Task

class StateModelTest(TestCase):
    def test_create_state(self):
        state = State.objects.create(name="Backlog")
        self.assertEqual(state.name, "Backlog")


class PriorityModelTest(TestCase):
    def test_create_priority(self):
        priority = Priority.objects.create(name="Baja")
        self.assertEqual(priority.name, "Baja")


class CustomUserModelTest(TestCase):
    def test_create_custom_user(self):
        user = CustomUser.objects.create(username="usuario1", password="password")
        self.assertEqual(user.username, "usuario1")

class TaskModelTest(TestCase):
    def test_create_task(self):
        state = State.objects.create(name="Doing")
        priority = Priority.objects.create(name="Media")
        user = CustomUser.objects.create(username="admin", password="password")
        task = Task.objects.create(
            name = "Test tarea 1",
            description = "Este es un test para la tarea 1",
            deadline = "2024-06-08",
            comment = "null",
            state = state,
            priority = priority,
            assigned_users = user,
            owner = user
        )
        self.assertEqual(task.name, "Test tarea 1")
        self.assertEqual(task.description, "Este es un test para la tarea 1")
        self.assertEqual(task.deadline, "2024-06-08")
        self.assertEqual(task.comment, "null")
        self.assertEqual(task.state, state)
        self.assertEqual(task.priority, priority)
        self.assertEqual(task.assigned_users, user)
        self.assertEqual(task.owner, user)