# Generated by Django 3.2.5 on 2021-08-06 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0010_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='user_channel',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_channel', to='studio.channel'),
        ),
    ]
