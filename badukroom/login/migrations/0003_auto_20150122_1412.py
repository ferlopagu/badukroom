# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150122_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='amigos',
            field=models.ManyToManyField(related_name='amigos_rel_+', to=b'login.Perfil', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_portada',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_principal',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='jugadores_favoritos',
            field=models.ManyToManyField(to=b'principal.Jugador', blank=True),
        ),
    ]
