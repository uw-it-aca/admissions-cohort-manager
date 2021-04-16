# Generated by Django 2.2.17 on 2021-02-09 00:13

import cohort_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cohort_manager', '0010_auto_20210130_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='syskeyassignment',
            name='application_not_found',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='syskeyassignment',
            name='admission_selection_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='syskeyassignment',
            name='application_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
