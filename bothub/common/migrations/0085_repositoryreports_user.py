# Generated by Django 2.2.12 on 2020-08-28 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0006_auto_20200729_1220"),
        ("common", "0084_repositoryreports"),
    ]

    operations = [
        migrations.AddField(
            model_name="repositoryreports",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="authentication.RepositoryOwner",
            ),
            preserve_default=False,
        )
    ]