from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    BACKLOG = 'BACKLOG'
    TO_DO = 'TO DO'
    DOING = 'DOING'
    TEST = 'TEST'
    DONE = 'DONE'

    STATE_CHOICES = [
        (BACKLOG, 'Backlog'),
        (TO_DO, 'To do'),
        (DOING, 'Doing'),
        (TEST, 'Test'),
        (DONE, 'Done'),
    ]

    name = models.CharField(max_length=40, verbose_name='Nombre de la tarea')
    description = models.CharField(max_length=255, verbose_name='Descripción de la tarea')
    state = models.CharField(max_length=30, choices=STATE_CHOICES, verbose_name='Estado de la tarea')
    date = models.DateField(verbose_name='Fecha de la tarea')
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE, verbose_name='Dueño de la tarea')

    def __str__(self):
        return f"tarea: {self.name} en estado {self.state}"
    
    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['date']