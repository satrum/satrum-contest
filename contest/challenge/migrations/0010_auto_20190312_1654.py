# Generated by Django 2.1.7 on 2019-03-12 13:54

import challenge.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0009_auto_20190307_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='filepath',
            field=models.FileField(default='', upload_to=challenge.models.content_file_name, validators=[challenge.models.validate_file_size], verbose_name=''),
        ),
    ]