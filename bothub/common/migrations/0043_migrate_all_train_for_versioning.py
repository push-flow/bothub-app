# Generated by Django 2.1.11 on 2019-12-12 20:13

from django.db import migrations


def noop(apps, schema_editor):  # pragma: no cover
    pass


def current_version(
    repository, repositoryversionlanguage, language=None, is_default=True
):
    language = language or repository.language

    repository_version, created = repository.versions.get_or_create(
        is_default=is_default
    )

    repository_version_language, created = repositoryversionlanguage.objects.get_or_create(
        repository_version=repository_version, language=language
    )
    return repository_version_language


def migrate_data(apps, schema_editor):  # pragma: no cover
    Repository = apps.get_model("common", "Repository")
    RepositoryVersionLanguage = apps.get_model("common", "RepositoryVersionLanguage")
    RepositoryUpdate = apps.get_model("common", "RepositoryUpdate")
    RepositoryExample = apps.get_model("common", "RepositoryExample")
    RepositoryEvaluate = apps.get_model("common", "RepositoryEvaluate")
    RepositoryEvaluateResult = apps.get_model("common", "RepositoryEvaluateResult")
    RepositoryTranslatedExample = apps.get_model(
        "common", "RepositoryTranslatedExample"
    )

    current_updates = []
    for repo in Repository.objects.all():
        update = RepositoryUpdate.objects.filter(
            repository=repo, trained_at__isnull=False
        ).last()
        if update is None:
            update = RepositoryUpdate.objects.filter(repository=repo).last()

        RepositoryExample.objects.filter(repository_update__repository=repo).update(
            repository_update=update
        )
        RepositoryEvaluate.objects.filter(repository_update__repository=repo).update(
            repository_update=update
        )
        RepositoryEvaluateResult.objects.filter(
            repository_update__repository=repo
        ).update(repository_update=update)
        RepositoryTranslatedExample.objects.filter(
            repository_update__repository=repo
        ).update(repository_update=update)

        if not update in current_updates:
            if update is not None:
                current_updates.append(update.pk)

    if current_updates:
        delete_rows = RepositoryUpdate.objects

        for i in current_updates:
            delete_rows = delete_rows.exclude(pk=i)

        delete_rows.delete()

    for repo_update in RepositoryUpdate.objects.all():
        version_language = current_version(
            repository=Repository.objects.get(pk=repo_update.repository.pk),
            repositoryversionlanguage=RepositoryVersionLanguage,
            language=repo_update.language,
        )

        version_language.bot_data = repo_update.bot_data
        version_language.training_started_at = repo_update.training_started_at
        version_language.training_end_at = repo_update.trained_at
        version_language.failed_at = repo_update.failed_at
        version_language.use_analyze_char = repo_update.use_analyze_char
        version_language.use_name_entities = repo_update.use_name_entities
        version_language.use_competing_intents = repo_update.use_competing_intents
        version_language.algorithm = repo_update.algorithm
        version_language.training_log = repo_update.training_log
        version_language.last_update = repo_update.trained_at
        version_language.save(
            update_fields=[
                "bot_data",
                "training_started_at",
                "training_end_at",
                "failed_at",
                "use_analyze_char",
                "use_name_entities",
                "use_competing_intents",
                "algorithm",
                "training_log",
                "last_update",
            ]
        )

        RepositoryExample.objects.filter(repository_update=repo_update).update(
            repository_version_language=version_language
        )

        RepositoryEvaluate.objects.filter(repository_update=repo_update).update(
            repository_version_language=version_language
        )

        RepositoryEvaluateResult.objects.filter(repository_update=repo_update).update(
            repository_version_language=version_language
        )

        RepositoryTranslatedExample.objects.filter(
            repository_update=repo_update
        ).update(repository_version_language=version_language)


class Migration(migrations.Migration):
    dependencies = [("common", "0042_auto_20191212_2013")]

    operations = [migrations.RunPython(migrate_data, noop)]