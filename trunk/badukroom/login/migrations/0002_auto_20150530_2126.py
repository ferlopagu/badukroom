# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='jugadores_favoritos',
            field=models.ManyToManyField(to='principal.Jugador', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
