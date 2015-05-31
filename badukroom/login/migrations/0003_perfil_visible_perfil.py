# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150530_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='visible_perfil',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
