# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-09 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='abc'),
        ),
    ]
