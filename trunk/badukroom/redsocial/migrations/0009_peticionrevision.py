# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20150220_1941'),
        ('redsocial', '0008_notificacion_revision'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeticionRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.CharField(max_length=300)),
                ('revision', models.BooleanField(default=False)),
                ('emisor', models.ForeignKey(related_name=b'sender1', to='login.Perfil')),
                ('receptor', models.ForeignKey(related_name=b'receiver1', to='login.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
