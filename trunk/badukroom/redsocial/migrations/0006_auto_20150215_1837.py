# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0013_auto_20150122_1455'),
        ('redsocial', '0005_auto_20150209_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respuesta',
            name='fichero',
        ),
        migrations.AddField(
            model_name='respuesta',
            name='partida',
            field=models.ForeignKey(blank=True, to='principal.Partida', null=True),
            preserve_default=True,
        ),
    ]
