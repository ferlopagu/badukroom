# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0015_auto_20150226_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisor',
            name='perfil',
            field=models.OneToOneField(to='login.Perfil'),
        ),
    ]
