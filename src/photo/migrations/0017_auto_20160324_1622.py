#pylint: skip-file
# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 16:22
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0016_auto_20160321_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmroll',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
