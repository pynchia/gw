# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0004_auto_20150211_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='difficulty',
            field=models.IntegerField(default=0, choices=[(0, b'Easy'), (1, b'Hard')]),
            preserve_default=True,
        ),
    ]
