# Generated by Django 3.2.5 on 2021-08-06 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studio', '0009_auto_20210804_0751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authtoken.token')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_channel', to='studio.channel')),
                ('which_channels', models.ManyToManyField(related_name='which_channels', to='studio.Channel')),
            ],
        ),
    ]
