# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitfuture', '0005_haltonpoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockBoundary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.CharField(max_length=7)),
                ('longitude', models.CharField(max_length=8)),
                ('census_block', models.ForeignKey(to='transitfuture.CensusBlock')),
            ],
            options={
                'db_table': 'block_boundaries',
            },
            bases=(models.Model,),
        ),
    ]
