# Generated by Django 2.1.7 on 2019-03-07 00:38

import challenge.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0006_auto_20190307_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='filename',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='submission',
            name='filepath',
            field=models.FileField(default='', upload_to='submit_files/', validators=[challenge.models.validate_file_size], verbose_name=''),
        ),
    ]
