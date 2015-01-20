# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('resultado', models.CharField(max_length=50)),
                ('path', models.CharField(max_length=70)),
                ('jugador_blanco', models.ForeignKey(related_name=b'Jugador_jugador_blanco', to='principal.Jugador')),
                ('jugador_negro', models.ForeignKey(related_name=b'Jugador_jugador_negro', to='principal.Jugador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaNacimiento', models.DateField()),
                ('rango', models.CharField(max_length=50, choices=[(b'30k', b'30k'), (b'29k', b'29k'), (b'28k', b'28k'), (b'27k', b'27k'), (b'26k', b'26k'), (b'25k', b'25k'), (b'24k', b'24k'), (b'23k', b'23k'), (b'22k', b'22k'), (b'21k', b'21k'), (b'20k', b'20k'), (b'19k', b'19k'), (b'18k', b'18k'), (b'17k', b'17k'), (b'16k', b'16k'), (b'15k', b'15k'), (b'14k', b'14k'), (b'13k', b'13k'), (b'12k', b'12k'), (b'11k', b'11k'), (b'10k', b'10k'), (b'9k', b'9k'), (b'8k', b'8k'), (b'7k', b'7k'), (b'6k', b'6k'), (b'5k', b'5k'), (b'4k', b'4k'), (b'3k', b'3k'), (b'2k', b'2k'), (b'1k', b'1k'), (b'1D', b'1D'), (b'2D', b'2D'), (b'3D', b'3D'), (b'4D', b'4D'), (b'5D', b'5D'), (b'6D', b'6D'), (b'7D', b'7D'), (b'8D', b'8D'), (b'9D', b'9D')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='partida',
            unique_together=set([('jugador_negro', 'jugador_blanco', 'fecha')]),
        ),
    ]
