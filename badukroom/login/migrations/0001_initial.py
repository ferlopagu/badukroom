# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0004_auto_20150115_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_nacimiento', models.DateField()),
                ('rango', models.CharField(max_length=50, choices=[(b'30k', b'30k'), (b'29k', b'29k'), (b'28k', b'28k'), (b'27k', b'27k'), (b'26k', b'26k'), (b'25k', b'25k'), (b'24k', b'24k'), (b'23k', b'23k'), (b'22k', b'22k'), (b'21k', b'21k'), (b'20k', b'20k'), (b'19k', b'19k'), (b'18k', b'18k'), (b'17k', b'17k'), (b'16k', b'16k'), (b'15k', b'15k'), (b'14k', b'14k'), (b'13k', b'13k'), (b'12k', b'12k'), (b'11k', b'11k'), (b'10k', b'10k'), (b'9k', b'9k'), (b'8k', b'8k'), (b'7k', b'7k'), (b'6k', b'6k'), (b'5k', b'5k'), (b'4k', b'4k'), (b'3k', b'3k'), (b'2k', b'2k'), (b'1k', b'1k'), (b'1D', b'1D'), (b'2D', b'2D'), (b'3D', b'3D'), (b'4D', b'4D'), (b'5D', b'5D'), (b'6D', b'6D'), (b'7D', b'7D'), (b'8D', b'8D'), (b'9D', b'9D')])),
                ('jugadores_favoritos', models.ManyToManyField(to='principal.Jugador')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
