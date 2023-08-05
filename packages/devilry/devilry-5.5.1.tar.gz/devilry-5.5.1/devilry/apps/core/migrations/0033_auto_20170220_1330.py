# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-20 13:30


import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_datamigrate_update_for_no_none_values_in_assignment_firstdeadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='first_deadline',
            field=models.DateTimeField(default=datetime.datetime(2100, 1, 1, 0, 0)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='points_to_grade_mapper',
            field=models.CharField(blank=True, choices=[('passed-failed', 'Passed or failed'), ('raw-points', 'Points'), ('custom-table', 'Lookup in a table defined by you (A-F, and other grading systems)')], default='passed-failed', max_length=25, null=True),
        ),
    ]
