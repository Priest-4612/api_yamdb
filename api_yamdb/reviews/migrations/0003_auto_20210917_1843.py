# Generated by Django 2.2.16 on 2021-09-17 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_comment_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='score',
        ),
    ]