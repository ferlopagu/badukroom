# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0008_auto_20150122_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partida',
            name='path',
            field=models.CharField(default=None, max_length=70, blank=True),
        ),
    ]
