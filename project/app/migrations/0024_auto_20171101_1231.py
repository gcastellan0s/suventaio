# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-01 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_cortes_lectordecb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corte_lectordecb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_corte', models.DateTimeField(blank=True, null=True)),
                ('usuario', models.CharField(blank=True, max_length=250, null=True, verbose_name='Usuario')),
            ],
        ),
        migrations.DeleteModel(
            name='Cortes_lectordecb',
        ),
    ]
