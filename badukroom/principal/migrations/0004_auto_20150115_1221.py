# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_perfil_jugadores_favoritos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='jugadores_favoritos',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='user',
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
