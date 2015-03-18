# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0022_auto_20150313_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugador',
            name='es_profesional',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
