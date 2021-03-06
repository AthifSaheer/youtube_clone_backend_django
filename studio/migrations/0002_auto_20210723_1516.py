# Generated by Django 3.2.5 on 2021-07-23 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadvideo',
            name='dislike',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='uploadvideo',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='uploadvideo',
            name='video',
            field=models.FileField(upload_to='videos'),
        ),
        migrations.AlterField(
            model_name='uploadvideo',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
