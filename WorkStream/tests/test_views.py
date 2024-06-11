from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from WorkStream.models import Task, State, Priority, CustomUser

class TaskViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.state = State.objects.create(name="Doing")
        self.priority = Priority.objects.create(name="Media")
        