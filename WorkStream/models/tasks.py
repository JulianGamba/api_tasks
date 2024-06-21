from django.db import models

from core import settings
from WorkStream.models.priority import Priority
from WorkStream.models.state import State


class Task(models.Model):

    name = models.CharField(max_length=40, verbose_name="Nombre de la tarea")
    description = models.CharField(
        max_length=255, verbose_name="Descripción de la tarea"
    )
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, verbose_name="Estado de la tarea"
    )
    priority = models.ForeignKey(
        Priority, on_delete=models.CASCADE, verbose_name="Prioridad de la tarea"
    )
    deadline = models.DateField(verbose_name="Fecha de la tarea")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks_owned",
        verbose_name="Dueño tarea",
    )
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks_assigned",
        verbose_name="usuario asignado ",
    )

    def __str__(self):
        return f"tarea: {self.name} en estado {self.state}"

    class Meta:

        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["deadline"]
