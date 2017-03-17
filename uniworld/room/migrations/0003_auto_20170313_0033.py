# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-13 00:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('room', '0002_auto_20170310_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchRoom',
            fields=[
                ('room_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='room.Room')),
                ('matching_time', models.DateTimeField()),
                ('matched', models.BooleanField(default=False)),
                ('groups', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=('room.room',),
        ),
        migrations.RemoveField(
            model_name='advancedroom',
            name='options',
        ),
        migrations.RemoveField(
            model_name='room',
            name='expense',
        ),
        migrations.RemoveField(
            model_name='room',
            name='reward',
        ),
        migrations.RemoveField(
            model_name='room',
            name='welcome',
        ),
        migrations.AddField(
            model_name='room',
            name='is_advanced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='is_chatroom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='is_matchroom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='options',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_room.room_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='room',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]