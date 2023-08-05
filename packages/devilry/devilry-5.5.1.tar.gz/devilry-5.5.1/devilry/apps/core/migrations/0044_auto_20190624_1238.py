# Generated by Django 2.2.1 on 2019-06-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20180302_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentgroup',
            name='is_open',
            field=models.BooleanField(blank=True, default=True, help_text='If this is checked, the group can add deliveries.'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='successful',
            field=models.BooleanField(blank=True, default=True, help_text='Has the delivery and all its files been uploaded successfully?'),
        ),
    ]
