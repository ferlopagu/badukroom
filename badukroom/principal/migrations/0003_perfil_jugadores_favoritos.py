# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_auto_20141230_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='jugadores_favoritos',
            field=models.ManyToManyField(to='principal.Jugador'),
            preserve_default=True,
        ),
    ]
