# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitfuture', '0006_blockboundary'),
    ]

    operations = [
        migrations.AddField(
            model_name='reachablecoordinates',
            name='lookup_key',
            field=models.CharField(max_length=36, null=True),
            preserve_default=True,
        ),
    ]
