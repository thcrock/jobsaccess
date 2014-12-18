# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitfuture', '0003_auto_20141116_2010'),
    ]

    operations = [
        migrations.RunSQL(
            "update block_locations set latitude = substring(latitude, 0, 8), longitude = substring(longitude, 0, 9)"
        ),
        migrations.RunSQL(
            "update reachable_coordinates set latitude_reachable = substring(latitude_reachable, 0, 8), longitude_reachable = substring(longitude_reachable, 0, 9)"
        ),
        migrations.AlterField(
            model_name='blocklocations',
            name='latitude',
            field=models.CharField(max_length=7),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blocklocations',
            name='longitude',
            field=models.CharField(max_length=8),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reachablecoordinates',
            name='latitude_reachable',
            field=models.CharField(max_length=7),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reachablecoordinates',
            name='longitude_reachable',
            field=models.CharField(max_length=8),
            preserve_default=True,
        ),
    ]
