from django.db import models

class State(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre del estado')

    def __str__(self):
        return self.name