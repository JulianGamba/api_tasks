from django.db import models

class Priority(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre de la prioridad')

    def __str__(self):
        return self.name