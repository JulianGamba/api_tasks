from django.db import models
from django.contrib.auth.models import AbstractUser

    
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre completo')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    identification =models.PositiveIntegerField(null=True, blank=True, verbose_name='numero de identificacion')
    def __str__(self):
        return self.username
