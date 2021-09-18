# Generated by Django 2.2.16 on 2021-09-17 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('u', 'user'), ('m', 'moderator'), ('a', 'admin')], default='user', max_length=50),
        ),
    ]