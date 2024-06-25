import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from WorkStream.models import Comment, Task, Priority, State  # Asegúrate de importar los modelos correctos

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='anotheruser', password='anotherpass')

@pytest.fixture
def priority(db):
    return Priority.objects.create(name="High")

@pytest.fixture
def state(db):
    return State.objects.create(name="Open")

@pytest.fixture
def task(db, user, priority, state):

    return Task.objects.create(
        name='Test Task',
        description='Test description',
        state=state,
        priority=priority,
        deadline='2024-12-31',
        owner=user
    )

@pytest.fixture
def comment(db, user, task):
    return Comment.objects.create(text='Test Comment', user=user, task=task)

@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
