# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-16 02:35
from __future__ import unicode_literals

import danceschool.core.models
from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170809_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Give this room a name.', max_length=80, verbose_name='Name')),
                ('defaultCapacity', models.PositiveIntegerField(blank=True, default=danceschool.core.models.get_defaultEventCapacity, help_text='If set, this will be used to determine capacity for class series in this room.', null=True, verbose_name='Default Venue Capacity')),
                ('description', djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='By default, only room names are listed publicly.  However, you may insert any descriptive information that you would like about this room here.', null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
                'verbose_name': 'Room',
                'ordering': ('location__name', 'name'),
            },
        ),
        migrations.RemoveField(
            model_name='eventstaffcategory',
            name='defaultRate',
        ),
        migrations.RemoveField(
            model_name='location',
            name='rentalRate',
        ),
        migrations.AlterUniqueTogether(
            name='eventstaffmember',
            unique_together=set([('staffMember', 'event', 'category', 'replacedStaffMember')]),
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Location', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='event',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Room', verbose_name='Room'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('location', 'name')]),
        ),
    ]
