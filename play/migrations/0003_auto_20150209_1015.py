# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0002_auto_20150202_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='computer_subject',
            field=models.ForeignKey(related_name='computer_subject', to='play.Subject'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='player_subject',
            field=models.ForeignKey(related_name='player_subject', to='play.Subject'),
            preserve_default=True,
        ),
    ]
