# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockLocations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.CharField(max_length=12)),
                ('longitude', models.CharField(max_length=12)),
            ],
            options={
                'db_table': 'block_locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CensusBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('census_block', models.CharField(max_length=15)),
                ('workforce_segment', models.CharField(max_length=6)),
                ('C000', models.IntegerField()),
                ('CA01', models.IntegerField()),
                ('CA02', models.IntegerField()),
                ('CA03', models.IntegerField()),
                ('CE01', models.IntegerField()),
                ('CE02', models.IntegerField()),
                ('CE03', models.IntegerField()),
                ('CNS01', models.IntegerField()),
                ('CNS02', models.IntegerField()),
                ('CNS03', models.IntegerField()),
                ('CNS04', models.IntegerField()),
                ('CNS05', models.IntegerField()),
                ('CNS06', models.IntegerField()),
                ('CNS07', models.IntegerField()),
                ('CNS08', models.IntegerField()),
                ('CNS09', models.IntegerField()),
                ('CNS10', models.IntegerField()),
                ('CNS11', models.IntegerField()),
                ('CNS12', models.IntegerField()),
                ('CNS13', models.IntegerField()),
                ('CNS14', models.IntegerField()),
                ('CNS15', models.IntegerField()),
                ('CNS16', models.IntegerField()),
                ('CNS17', models.IntegerField()),
                ('CNS18', models.IntegerField()),
                ('CNS19', models.IntegerField()),
                ('CNS20', models.IntegerField()),
                ('CR01', models.IntegerField()),
                ('CR02', models.IntegerField()),
                ('CR03', models.IntegerField()),
                ('CR04', models.IntegerField()),
                ('CR05', models.IntegerField()),
                ('CR07', models.IntegerField()),
                ('CT01', models.IntegerField()),
                ('CT02', models.IntegerField()),
                ('CD01', models.IntegerField()),
                ('CD02', models.IntegerField()),
                ('CD03', models.IntegerField()),
                ('CD04', models.IntegerField()),
                ('CS01', models.IntegerField()),
                ('CS02', models.IntegerField()),
                ('CFA01', models.IntegerField()),
                ('CFA02', models.IntegerField()),
                ('CFA03', models.IntegerField()),
                ('CFA04', models.IntegerField()),
                ('CFA05', models.IntegerField()),
                ('CFS01', models.IntegerField()),
                ('CFS02', models.IntegerField()),
                ('CFS03', models.IntegerField()),
                ('CFS04', models.IntegerField()),
                ('CFS05', models.IntegerField()),
            ],
            options={
                'db_table': 'census_blocks',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blocklocations',
            name='census_block',
            field=models.ForeignKey(to='transitfuture.CensusBlock'),
            preserve_default=True,
        ),
    ]
