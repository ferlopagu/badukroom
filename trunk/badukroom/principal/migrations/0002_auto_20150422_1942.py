# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartidaRevisada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('jugador_negro', models.CharField(max_length=100)),
                ('rango_negro', models.CharField(max_length=50)),
                ('jugador_blanco', models.CharField(max_length=100)),
                ('rango_blanco', models.CharField(max_length=50)),
                ('fichero', models.FileField(upload_to=b'revision')),
                ('path', models.CharField(max_length=70, blank=True)),
                ('sgf_size', models.IntegerField(default=0)),
                ('revisor', models.ForeignKey(blank=True, to='principal.Revisor', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='partidarevisada',
            unique_together=set([('jugador_negro', 'jugador_blanco', 'fecha', 'sgf_size')]),
        ),
        migrations.RemoveField(
            model_name='partida',
            name='revisor',
        ),
    ]
