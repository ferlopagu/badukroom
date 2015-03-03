# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0018_auto_20150302_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partida',
            name='path',
            field=models.CharField(max_length=70, blank=True),
        ),
    ]
