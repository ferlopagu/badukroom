# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0010_auto_20150122_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partida',
            name='path',
            field=models.CharField(default=b'sgf/None', max_length=70, blank=True),
        ),
    ]
