# Generated by Django 2.1.5 on 2019-03-27 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0029_auto_20190126_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='use_name_entities',
            field=models.BooleanField(default=False, help_text='When enabling name entities you will receive name of people, companies and places as results of your predictions.', verbose_name='Use name entities'),
        ),
        migrations.AddField(
            model_name='repositoryupdate',
            name='use_name_entities',
            field=models.BooleanField(default=False),
        ),
    ]
