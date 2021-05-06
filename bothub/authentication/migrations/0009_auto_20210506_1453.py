# Generated by Django 2.2.22 on 2021-05-06 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('en-us', 'English'), ('pt-br', 'Brazilian Portuguese')], max_length=5, null=True),
        ),
    ]