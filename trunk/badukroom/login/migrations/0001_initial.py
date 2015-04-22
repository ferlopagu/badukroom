# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_nacimiento', models.DateField(help_text=b'Formato: dd/mm/yyyy')),
                ('ciudad', models.CharField(max_length=50, blank=True)),
                ('rango', models.CharField(max_length=50, choices=[(b'30k', b'30k'), (b'29k', b'29k'), (b'28k', b'28k'), (b'27k', b'27k'), (b'26k', b'26k'), (b'25k', b'25k'), (b'24k', b'24k'), (b'23k', b'23k'), (b'22k', b'22k'), (b'21k', b'21k'), (b'20k', b'20k'), (b'19k', b'19k'), (b'18k', b'18k'), (b'17k', b'17k'), (b'16k', b'16k'), (b'15k', b'15k'), (b'14k', b'14k'), (b'13k', b'13k'), (b'12k', b'12k'), (b'11k', b'11k'), (b'10k', b'10k'), (b'9k', b'9k'), (b'8k', b'8k'), (b'7k', b'7k'), (b'6k', b'6k'), (b'5k', b'5k'), (b'4k', b'4k'), (b'3k', b'3k'), (b'2k', b'2k'), (b'1k', b'1k'), (b'1D', b'1D'), (b'2D', b'2D'), (b'3D', b'3D'), (b'4D', b'4D'), (b'5D', b'5D'), (b'6D', b'6D'), (b'7D', b'7D'), (b'8D', b'8D'), (b'9D', b'9D')])),
                ('foto_principal', models.ImageField(default=b'/home/fla2727/workspace/badukroom/media/imagenes/sin_foto.jpg', upload_to=b'/home/fla2727/workspace/badukroom/mediaimagenes', blank=True)),
                ('path_principal', models.CharField(default=b'imagenes/sin_foto.jpg', max_length=70, blank=True)),
                ('foto_portada', models.ImageField(default=b'/home/fla2727/workspace/badukroom/media/imagenes/sin_portada.jpg', upload_to=b'/home/fla2727/workspace/badukroom/mediaimagenes', blank=True)),
                ('path_portada', models.CharField(default=b'imagenes/sin_portada.jpg', max_length=70, blank=True)),
                ('amigos', models.ManyToManyField(related_name='amigos_rel_+', to='login.Perfil', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
