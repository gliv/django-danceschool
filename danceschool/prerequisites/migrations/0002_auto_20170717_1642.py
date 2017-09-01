# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-17 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prerequisites', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerrequirement',
            options={'verbose_name': 'Customer-level requirement record', 'verbose_name_plural': 'Customer-level requirement records'},
        ),
        migrations.AlterModelOptions(
            name='requirement',
            options={'permissions': (('ignore_requirements', 'Can register users for series regardless of any prerequisites or requirements'),), 'verbose_name': 'Class requirements'},
        ),
        migrations.AlterModelOptions(
            name='requirementitem',
            options={'verbose_name': 'Requirement item', 'verbose_name_plural': 'Requirement items'},
        ),
        migrations.AlterField(
            model_name='customerrequirement',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Customer', verbose_name='Customer'),
        ),
        migrations.AlterField(
            model_name='customerrequirement',
            name='modifiedDate',
            field=models.DateTimeField(auto_now=True, verbose_name='Last modified date'),
        ),
        migrations.AlterField(
            model_name='customerrequirement',
            name='requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prerequisites.Requirement', verbose_name='Requirement'),
        ),
        migrations.AlterField(
            model_name='customerrequirement',
            name='role',
            field=models.ForeignKey(blank=True, help_text='Role must be specified only for requirements for which roles are enforced.', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DanceRole', verbose_name='Dance role'),
        ),
        migrations.AlterField(
            model_name='customerrequirement',
            name='submissionDate',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Submission date'),
        ),
        migrations.AlterField(
            model_name='requirementitem',
            name='requiredClass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ClassDescription', verbose_name='Required class'),
        ),
        migrations.AlterField(
            model_name='requirementitem',
            name='requiredLevel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DanceTypeLevel', verbose_name='Required Dance type/level'),
        ),
        migrations.AlterField(
            model_name='requirementitem',
            name='requirement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prerequisites.Requirement', verbose_name='Requirement'),
        ),
    ]
