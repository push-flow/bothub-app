# Generated by Django 2.2.12 on 2020-07-24 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20200716_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='locale',
        ),
        migrations.AddField(
            model_name='repositoryowner',
            name='locale',
            field=models.CharField(blank=True, help_text="User's locale.", max_length=48, verbose_name='locale'),
        ),
    ]