# Generated by Django 2.1.7 on 2019-03-06 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_auto_20190304_1910'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='submission',
            unique_together=set(),
        ),
    ]
