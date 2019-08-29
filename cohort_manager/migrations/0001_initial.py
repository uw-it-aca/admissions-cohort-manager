# Generated by Django 2.2.4 on 2019-08-29 16:36

import cohort_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_key', models.CharField(max_length=30, validators=[cohort_manager.models.validate_system_key])),
                ('campus', models.PositiveSmallIntegerField(choices=[(0, 'Seattle'), (1, 'Tacoma'), (2, 'Bothell')], default=0)),
                ('year', models.PositiveSmallIntegerField(validators=[cohort_manager.models.validate_year])),
                ('quarter', models.PositiveSmallIntegerField(choices=[(1, 'Winter'), (2, 'Spring'), (3, 'Summer'), (4, 'Autumn')], default=4)),
                ('application_number', models.PositiveIntegerField(validators=[cohort_manager.models.validate_application_number])),
                ('admission_selection_id', models.CharField(max_length=30)),
                ('cohort', models.CharField(blank=True, max_length=30, validators=[cohort_manager.models.validate_cohort])),
                ('major', models.CharField(blank=True, max_length=30, validators=[cohort_manager.models.validate_major])),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssignmentImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.TextField()),
                ('comment', models.TextField()),
                ('is_file_upload', models.NullBooleanField(default=True)),
                ('upload_filename', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=30)),
                ('imported_date', models.DateTimeField(null=True)),
                ('imported_status', models.SmallIntegerField(null=True)),
                ('imported_message', models.TextField(null=True)),
                ('cohort', models.CharField(blank=True, max_length=30, validators=[cohort_manager.models.validate_cohort])),
                ('major', models.CharField(blank=True, max_length=30, validators=[cohort_manager.models.validate_major])),
            ],
        ),
    ]
