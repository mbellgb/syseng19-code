# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0008_participant_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='isMentor',
            field=models.BooleanField(),
        ),
    ]