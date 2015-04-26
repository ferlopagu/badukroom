# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_perfil_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto_portada',
            field=models.ImageField(default=b'/imagenes/sin_portada.jpg', upload_to=b'imagenes', blank=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_principal',
            field=models.ImageField(default=b'/imagenes/sin_foto.jpg', upload_to=b'imagenes', blank=True),
        ),
    ]
