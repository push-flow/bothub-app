# Generated by Django 2.2.12 on 2020-06-19 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("common", "0064_auto_20200616_1642")]

    operations = [
        migrations.AlterUniqueTogether(
            name="repositoryqueuetask", unique_together=set()
        )
    ]
