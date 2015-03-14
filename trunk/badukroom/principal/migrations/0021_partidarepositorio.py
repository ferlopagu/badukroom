# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0020_auto_20150311_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartidaRepositorio',
            fields=[
                ('partida_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='principal.Partida')),
                ('es_profesional', models.BooleanField()),
            ],
            options={
            },
            bases=('principal.partida',),
        ),
    ]
