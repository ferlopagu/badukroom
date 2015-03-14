# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0019_auto_20150302_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='rango_blanco',
            field=models.CharField(default='5k', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partida',
            name='rango_negro',
            field=models.CharField(default='1k', max_length=50),
            preserve_default=False,
        ),
    ]
