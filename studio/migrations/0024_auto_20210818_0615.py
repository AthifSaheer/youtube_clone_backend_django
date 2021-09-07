# Generated by Django 3.2.5 on 2021-08-18 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studio', '0023_auto_20210815_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislike',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_liked_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_liked_channel', to='studio.channel')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authtoken.token')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('which_comment_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='which_comment_like', to='studio.comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dislike', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_disliked_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_disliked_channel', to='studio.channel')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authtoken.token')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('which_comment_dislike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='which_comment_dislike', to='studio.comment')),
            ],
        ),
    ]