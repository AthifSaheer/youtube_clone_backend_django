# Generated by Django 3.2.5 on 2021-08-06 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('studio', '0011_alter_subscription_user_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='token',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authtoken.token'),
        ),
    ]
