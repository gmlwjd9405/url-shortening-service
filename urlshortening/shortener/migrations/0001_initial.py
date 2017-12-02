# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-02 16:33
from __future__ import unicode_literals

from django.db import migrations, models
import shortener.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenerURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=220, validators=[shortener.validators.validate_url])),
                ('shortcode', models.CharField(blank=True, max_length=8, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
