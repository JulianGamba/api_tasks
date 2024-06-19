from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Nombre completo')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    identification = models.PositiveIntegerField(null=True, blank=True, verbose_name='Número de identificación')

    def __str__(self):
        return self.username