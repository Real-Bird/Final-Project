# Generated by Django 3.2.5 on 2021-09-01 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_comment_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='update_at',
            new_name='updated_at',
        ),
    ]