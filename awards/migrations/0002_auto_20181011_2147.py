# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rating',
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]
