# Generated by Django 3.2.5 on 2021-08-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0015_auto_20210807_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='subscribers',
            field=models.IntegerField(default=0),
        ),
    ]
