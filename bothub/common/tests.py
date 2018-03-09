from django.test import TestCase
from django.utils import timezone

from bothub.authentication.models import User
from .models import Repository
from .models import RepositoryExample
from .models import RepositoryExampleEntity
from .models import RepositoryTranslatedExample
from .models import RepositoryTranslatedExampleEntity
from .models import DoesNotHaveTranslation
from . import languages


class RepositoryUpdateTestCase(TestCase):
    EXPECTED_RASA_NLU_DATA = {
        'common_examples': [
            {
                'text': 'my name is Douglas',
                'intent': '',
                'entities': [
                    {
                        'start': 11,
                        'end': 18,
                        'value': 'Douglas',
                        'entity': 'name',
                    },
                ],
            }
        ],
    }

    def setUp(self):
        owner = User.objects.create_user('fake@user.com', 'user', '123456')
        self.repository = Repository.objects.create(
            owner=owner,
            slug='test')
        self.repository_update = self.repository.current_update('en')
        example = RepositoryExample.objects.create(
            repository_update=self.repository_update,
            text='my name is Douglas')
        self.entity = RepositoryExampleEntity.objects.create(
            repository_example=example,
            start=11,
            end=18,
            entity='name')

    def test_repository_example_entity(self):
        self.assertEqual(self.entity.value, 'Douglas')

    def test_get_rasa_nlu_data(self):
        self.assertDictEqual(
            self.repository_update.rasa_nlu_data,
            RepositoryUpdateTestCase.EXPECTED_RASA_NLU_DATA)

    def test_repository_current_update(self):
        update1 = self.repository.current_update('en')
        self.assertEqual(update1, self.repository.current_update('en'))
        update1.training_started_at = timezone.now()
        update1.save()
        self.assertNotEqual(update1, self.repository.current_update('en'))


class TranslateTestCase(TestCase):
    EXPECTED_RASA_NLU_DATA = {
        'common_examples': [
            {
                'text': 'meu nome é Douglas',
                'intent': 'greet',
                'entities': [],
            },
        ],
    }

    EXPECTED_RASA_NLU_DATA_WITH_ENTITIES = {
        'common_examples': [
            {
                'text': 'meu nome é Douglas',
                'intent': 'greet',
                'entities': [
                    {
                        'start': 11,
                        'end': 18,
                        'value': 'Douglas',
                        'entity': 'name',
                    }
                ],
            },
        ],
    }

    def setUp(self):
        owner = User.objects.create_user('fake@user.com', 'user', '123456')
        self.repository = Repository.objects.create(
            owner=owner,
            slug='test',
            language=languages.LANGUAGE_EN)
        self.repository_update = self.repository.current_update('en')
        self.example = RepositoryExample.objects.create(
            repository_update=self.repository_update,
            text='my name is Douglas',
            intent='greet')

    def test_new_translate(self):
        language = languages.LANGUAGE_PT
        RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')
        self.assertEqual(
            len(self.repository.current_update(language).examples),
            1)

    def test_to_rasa_nlu_data(self):
        language = languages.LANGUAGE_PT
        RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')

        self.assertDictEqual(
            self.repository.current_update(
                languages.LANGUAGE_PT).rasa_nlu_data,
            TranslateTestCase.EXPECTED_RASA_NLU_DATA)

    def test_translated_entity(self):
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=11,
            end=18,
            entity='name')

        language = languages.LANGUAGE_PT
        translate = RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')
        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=translate,
            start=11,
            end=18,
            entity='name')
        self.assertDictEqual(
            self.repository.current_update(
                languages.LANGUAGE_PT).rasa_nlu_data,
            TranslateTestCase.EXPECTED_RASA_NLU_DATA_WITH_ENTITIES)

    def test_valid_entities(self):
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=12,
            end=19,
            entity='name')

        language = languages.LANGUAGE_PT
        translate = RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')
        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=translate,
            start=11,
            end=18,
            entity='name')

        self.assertEqual(
            translate.has_valid_entities,
            True)

    def test_invalid_count_entities(self):
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=12,
            end=19,
            entity='name')

        language = languages.LANGUAGE_PT
        translate = RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')

        self.assertEqual(
            translate.has_valid_entities,
            False)

    def test_invalid_how_entities(self):
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=12,
            end=19,
            entity='name')

        language = languages.LANGUAGE_PT
        translate = RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')
        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=translate,
            start=11,
            end=18,
            entity='nome')

        self.assertEqual(
            translate.has_valid_entities,
            False)

    def test_invalid_many_how_entities(self):
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=12,
            end=19,
            entity='name')
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=11,
            end=19,
            entity='name')
        RepositoryExampleEntity.objects.create(
            repository_example=self.example,
            start=11,
            end=12,
            entity='space')

        language = languages.LANGUAGE_PT
        translate = RepositoryTranslatedExample.objects.create(
            original_example=self.example,
            language=language,
            text='meu nome é Douglas')
        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=translate,
            start=11,
            end=18,
            entity='name')
        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=translate,
            start=10,
            end=11,
            entity='space')
        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=translate,
            start=10,
            end=11,
            entity='space')

        self.assertEqual(
            translate.has_valid_entities,
            False)

    def test_does_not_have_translation(self):
        with self.assertRaises(DoesNotHaveTranslation):
            self.example.get_translation(languages.LANGUAGE_NL)


class RepositoryTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner@user.com', 'user')
        self.user = User.objects.create_user('fake@user.com', 'user')

        self.repository = Repository.objects.create(
            owner=self.owner,
            name='Test',
            slug='test')
        self.private_repository = Repository.objects.create(
            owner=self.owner,
            name='Test',
            slug='private',
            is_private=True)

    def test_languages_status(self):
        languages_status = self.repository.languages_status
        self.assertListEqual(
            list(languages_status.keys()),
            languages.SUPPORTED_LANGUAGES)
        # TODO: Update test_languages_status test
        #       Create expeted result

    def test_current_rasa_nlu_data(self):
        current_rasa_nlu_data = self.repository.current_rasa_nlu_data()
        self.assertListEqual(
            list(current_rasa_nlu_data.keys()),
            ['common_examples'])
        # TODO: Update test_current_rasa_nlu_data test
        #       Create expeted result

    def test_last_trained_update(self):
        self.assertFalse(self.repository.last_trained_update())
        # TODO: Update last_trained_update test

    def test_get_user_authorization(self):
        self.assertTrue(
            self.repository.get_user_authorization(self.owner))
        self.assertTrue(
            self.repository.get_user_authorization(self.user))
        self.assertTrue(
            self.private_repository.get_user_authorization(self.owner))
        self.assertFalse(
            self.private_repository.get_user_authorization(self.user))


class RepositoryExampleTestCase(TestCase):
    def setUp(self):
        self.language = languages.LANGUAGE_EN

        self.owner = User.objects.create_user('owner@user.com', 'user')

        self.repository = Repository.objects.create(
            owner=self.owner,
            name='Test',
            slug='test',
            language=self.language)

        self.example = RepositoryExample.objects.create(
            repository_update=self.repository.current_update(),
            text='hi',
            intent='greet')

    def test_language(self):
        self.assertEqual(
            self.example.language,
            self.example.repository_update.language)
        self.assertEqual(
            self.example.language,
            self.language)

    def teste_delete(self):
        self.example.delete()
        self.assertEqual(
            self.example.deleted_in,
            self.repository.current_update())
