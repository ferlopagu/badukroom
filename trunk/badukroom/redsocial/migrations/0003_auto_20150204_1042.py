# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsocial', '0002_peticionamistad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='peticionamistad',
            old_name='sender',
            new_name='emisor',
        ),
        migrations.RenameField(
            model_name='peticionamistad',
            old_name='receiver',
            new_name='receptor',
        ),
    ]
