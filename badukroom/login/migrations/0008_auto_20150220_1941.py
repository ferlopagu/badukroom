# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20150220_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='path_portada',
            field=models.CharField(default=b'imagenes/sin_portada.jpg', max_length=70, blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='path_principal',
            field=models.CharField(default=b'imagenes/sin_foto.jpg', max_length=70, blank=True),
        ),
    ]
