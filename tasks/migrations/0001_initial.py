# Generated by Django 5.0.6 on 2024-05-28 23:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre de la prioridad')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre del estado')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Nombre de la tarea')),
                ('description', models.CharField(max_length=255, verbose_name='Descripción de la tarea')),
                ('deadline', models.DateField(verbose_name='Fecha de la tarea')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Comentarios de la tarea')),
                ('assigned_users', models.ManyToManyField(related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='usuario asignado')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Dueño de la tarea')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.priority', verbose_name='Prioridad de la tarea')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.state', verbose_name='Estado de la tarea')),
            ],
            options={
                'verbose_name': 'Tarea',
                'verbose_name_plural': 'Tareas',
                'ordering': ['deadline'],
            },
        ),
    ]
