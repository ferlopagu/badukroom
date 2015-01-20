# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0004_auto_20150115_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='path',
        ),
        migrations.AddField(
            model_name='partida',
            name='fichero',
            field=models.FileField(default=datetime.date(2015, 1, 16), upload_to=b'/static/sgf'),
            preserve_default=False,
        ),
    ]
