from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from core import settings


class State(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre del estado')

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre de la prioridad')

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre completo')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    identification =models.PositiveIntegerField(null=True, blank=True, verbose_name='numero de identificacion')
    def __str__(self):
        return self.username

class Task(models.Model):
    name = models.CharField(max_length=40, verbose_name='Nombre de la tarea')
    description = models.CharField(max_length=255, verbose_name='Descripción de la tarea')
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='Estado de la tarea')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, verbose_name='Prioridad de la tarea')
    deadline = models.DateField(verbose_name='Fecha de la tarea')
    comment = models.CharField(max_length=255, verbose_name='Comentarios de la tarea', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dueño tarea')
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='usuario a desarrollar la tarea')

    def __str__(self):
        return f"tarea: {self.name} en estado {self.state}"
    
    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['deadline']
        
    
