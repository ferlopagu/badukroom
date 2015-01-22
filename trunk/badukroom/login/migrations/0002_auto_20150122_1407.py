# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='amigos',
            field=models.ManyToManyField(related_name='amigos_rel_+', to='login.Perfil'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='foto_portada',
            field=models.ImageField(default=datetime.date(2015, 1, 22), upload_to=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='perfil',
            name='foto_principal',
            field=models.ImageField(default=datetime.date(2015, 1, 22), upload_to=b''),
            preserve_default=False,
        ),
    ]
