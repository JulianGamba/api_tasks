from rest_framework.test import APITestCase
from WorkStream.models.tasks import Task
from WorkStream.models.state import State
from WorkStream.models.priority import Priority
from WorkStream.models.customUser import CustomUser
from WorkStream.serializers.stateSerializers import StateSerializer
from WorkStream.serializers.prioritySerializers import PrioritySerializer
from WorkStream.serializers.customUserSerializers import CustomUserSerializer
from WorkStream.serializers.taskSerializers import TaskReadSerializer, TaskWriteSerializer

class TaskSerializerTest(APITestCase):

    def setUp(self):
        self.state = State.objects.create(name='Doing')
        self.priority = Priority.objects.create(name='Alta')
        self.user = CustomUser.objects.create_user(username='user_test', password='password')
        self.task_data = {
            "name": "Test tarea 1",
            "description": "Este es el test de la tarea 1",
            "deadline": "2024-06-08",
            "comment": "null",
            "state": self.state.id,
            "priority": self.priority.id,
            "assigned_users": [self.user.id],
            "owner": self.user.id
        }
        self.task = Task.objects.create(
            name="Test tarea 1",
            description="Este es un test para la tarea 1",
            deadline="2024-06-08",
            comment="null",
            state=self.state,
            priority=self.priority,
            owner=self.user
        )
        self.task.assigned_users.set([self.user])

    def test_task_serializaion(self):
        serializer = TaskReadSerializer
