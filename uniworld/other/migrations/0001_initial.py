# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-10 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import mptt.fields
import other.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ch', models.CharField(max_length=10, unique=True)),
                ('name_en', models.CharField(max_length=30, unique=True)),
                ('description_ch', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to=other.models.upload_to)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='other.Label')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TitleLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ch', models.CharField(max_length=10)),
                ('name_en', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ch', models.CharField(max_length=10)),
                ('name_en', models.CharField(max_length=30)),
                ('email_suffix', models.CharField(max_length=20)),
            ],
        ),
    ]
