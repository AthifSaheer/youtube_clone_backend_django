# Generated by Django 3.2.5 on 2021-08-11 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0021_replaycomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replaycomment',
            name='received_parent_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_parent_comment', to='studio.comment'),
        ),
    ]
