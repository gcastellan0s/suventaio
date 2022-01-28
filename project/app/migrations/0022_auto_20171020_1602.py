# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-20 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20170414_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfc', models.CharField(help_text='RFC de la empresa', max_length=250, verbose_name='RFC')),
                ('razon_social', models.CharField(help_text='Raz\xf3n social de la empresa', max_length=250, verbose_name='Razon social')),
                ('telefono', models.CharField(blank=True, max_length=250, null=True, verbose_name='Tel\xe9fono')),
                ('contacto', models.CharField(help_text='Nombre del contacto que requiere la factura', max_length=250, verbose_name='Nombre de contacto')),
                ('email_contacto', models.CharField(help_text='Email para enviar la factura timbrada', max_length=250, verbose_name='Email de contacto')),
                ('calle', models.CharField(blank=True, max_length=250, null=True, verbose_name='Calle')),
                ('numero_exterior', models.CharField(blank=True, max_length=250, null=True, verbose_name='Numero exterior')),
                ('numero_interior', models.CharField(blank=True, max_length=250, null=True, verbose_name='Numero interior')),
                ('colonia', models.CharField(blank=True, max_length=250, null=True, verbose_name='Colonia')),
                ('municipio_o_delegacion', models.CharField(blank=True, max_length=250, null=True, verbose_name='Delegaci\xf3n o Municipio')),
                ('estado', models.CharField(blank=True, max_length=250, null=True, verbose_name='Estado')),
                ('codigo_postal', models.CharField(blank=True, max_length=250, null=True, verbose_name='Codigo Postal')),
                ('pais', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pais')),
            ],
        ),
        migrations.AlterField(
            model_name='sell_point',
            name='domain',
            field=models.CharField(blank=True, help_text='Dominio de la sucursal', max_length=40, null=True, verbose_name='Dominio'),
        ),
    ]
