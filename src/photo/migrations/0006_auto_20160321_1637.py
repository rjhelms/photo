# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0005_auto_20160321_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmroll',
            name='developer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='photo.Developer'),
        ),
    ]
