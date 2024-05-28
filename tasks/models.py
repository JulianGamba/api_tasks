from django.db import models
from django.contrib.auth.models import User

class State(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre del estado')

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre de la prioridad')

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=40, verbose_name='Nombre de la tarea')
    description = models.CharField(max_length=255, verbose_name='Descripción de la tarea')
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='Estado de la tarea')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, verbose_name='Prioridad de la tarea')
    deadline = models.DateField(verbose_name='Fecha de la tarea')
    comment = models.CharField(max_length=255, verbose_name='Comentarios de la tarea', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE, verbose_name='Dueño de la tarea')
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks', verbose_name='usuario asignado')

    def __str__(self):
        return f"tarea: {self.name} en estado {self.state}"
    
    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['deadline']