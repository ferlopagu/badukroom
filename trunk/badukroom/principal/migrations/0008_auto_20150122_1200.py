# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_partida_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partida',
            name='path',
            field=models.CharField(default=None, max_length=70),
        ),
    ]
