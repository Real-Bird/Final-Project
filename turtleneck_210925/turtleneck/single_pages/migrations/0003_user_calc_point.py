# Generated by Django 3.2.6 on 2021-09-11 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('single_pages', '0002_user_user_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='calc_point',
            field=models.IntegerField(default=1000),
        ),
    ]
