# Generated by Django 3.2.5 on 2021-08-07 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0013_auto_20210806_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='token',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
    ]
