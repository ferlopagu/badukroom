# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0006_auto_20150215_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='foto_portada',
            field=models.ImageField(default=b'/home/fla2727/workspace/tfg/badukroom/static//imagenes/sin_portada.jpg', upload_to=b'/home/fla2727/workspace/tfg/badukroom/static/imagenes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grupo',
            name='path_portada',
            field=models.CharField(default=b'imagenes/sin_portada.jpg', max_length=70, blank=True),
            preserve_default=True,
        ),
    ]
