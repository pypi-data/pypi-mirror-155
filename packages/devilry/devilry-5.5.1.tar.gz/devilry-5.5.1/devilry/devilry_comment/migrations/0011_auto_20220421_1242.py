# Generated by Django 3.2.6 on 2022-04-21 10:42

import devilry.devilry_comment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devilry_comment', '0010_commentedithistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentfile',
            name='file',
            field=models.FileField(blank=True, db_index=True, default='', max_length=512, upload_to=devilry.devilry_comment.models.commentfile_directory_path),
        ),
        migrations.AlterField(
            model_name='commentfileimage',
            name='image',
            field=models.FileField(blank=True, db_index=True, default='', max_length=512, upload_to=devilry.devilry_comment.models.commentfileimage_directory_path),
        ),
        migrations.AlterField(
            model_name='commentfileimage',
            name='thumbnail',
            field=models.FileField(blank=True, db_index=True, default='', max_length=512, upload_to=devilry.devilry_comment.models.commentfileimage_thumbnail_directory_path),
        ),
    ]
