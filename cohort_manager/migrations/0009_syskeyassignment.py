# Generated by Django 2.2.17 on 2021-01-19 23:36

import cohort_manager.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cohort_manager', '0008_syskeyimport'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyskeyAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_key', models.CharField(max_length=30, validators=[cohort_manager.models.validate_system_key])),
                ('application_number', models.PositiveIntegerField(validators=[cohort_manager.models.validate_application_number])),
                ('admission_selection_id', models.CharField(max_length=30)),
                ('assigned_cohort', models.IntegerField(null=True)),
                ('assigned_major', models.CharField(max_length=30, null=True)),
                ('major_program_code', models.TextField(null=True)),
                ('campus', models.PositiveSmallIntegerField(choices=[(1, 'Seattle'), (2, 'Tacoma'), (3, 'Bothell')], default=1)),
                ('assignment_import', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cohort_manager.SyskeyImport')),
            ],
        ),
    ]
