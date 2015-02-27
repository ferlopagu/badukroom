# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0016_auto_20150226_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisor',
            name='nickname_kgs',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
