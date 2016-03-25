#pylint: skip-file
# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0009_auto_20160325_0242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enlarger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Condenser'), (1, 'Diffuser')])),
                ('color_head', models.BooleanField()),
                ('formats', models.ManyToManyField(to='photo.FilmFormat')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='frame',
            unique_together=set([('index', 'film_roll')]),
        ),
        migrations.AddField(
            model_name='print',
            name='enlarger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='photo.Enlarger'),
        ),
    ]
