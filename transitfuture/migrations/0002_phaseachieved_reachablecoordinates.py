# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitfuture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhaseAchieved',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'phases_achieved',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReachableCoordinates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude_start', models.CharField(max_length=12)),
                ('longitude_start', models.CharField(max_length=12)),
                ('depart_time', models.DateTimeField()),
                ('transit_time', models.IntegerField()),
                ('latitude_reachable', models.CharField(max_length=12)),
                ('longitude_reachable', models.CharField(max_length=12)),
                ('phase_achieved', models.ForeignKey(to='transitfuture.PhaseAchieved')),
            ],
            options={
                'db_table': 'reachable_coordinates',
            },
            bases=(models.Model,),
        ),
    ]
