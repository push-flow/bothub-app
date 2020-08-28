# Generated by Django 2.2.12 on 2020-08-28 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("common", "0086_auto_20200828_1828")]

    operations = [
        migrations.AlterField(
            model_name="repositoryreports",
            name="repository_version_language",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="repository_reports",
                to="common.RepositoryVersionLanguage",
            ),
        )
    ]
