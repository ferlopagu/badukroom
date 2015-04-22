# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_auto_20150422_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='partidarevisada',
            name='resultado',
            field=models.CharField(default='W+R', max_length=50),
            preserve_default=False,
        ),
    ]
