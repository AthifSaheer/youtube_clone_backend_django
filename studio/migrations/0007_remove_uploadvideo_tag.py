# Generated by Django 3.2.5 on 2021-07-25 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0006_auto_20210724_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadvideo',
            name='tag',
        ),
    ]
