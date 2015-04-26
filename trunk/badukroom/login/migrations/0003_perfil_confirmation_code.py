# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150422_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='confirmation_code',
            field=models.CharField(default='Prueba', max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
