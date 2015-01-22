# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_auto_20150122_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='path',
            field=models.CharField(default=datetime.date(2015, 1, 22), max_length=70),
            preserve_default=False,
        ),
    ]
