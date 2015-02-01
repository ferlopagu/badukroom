# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20150122_1451'),
        ('redsocial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeticionAmistad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('es_aceptada', models.BooleanField(default=False)),
                ('es_rechazada', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(related_name=b'receiver', to='login.Perfil')),
                ('sender', models.ForeignKey(related_name=b'sender', to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
