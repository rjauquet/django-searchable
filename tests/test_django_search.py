from django.test import TestCase

from django_search.models import SearchableModel, SearchableTextField
from tests.models import TestModel


class DjangoSearchModelTests(TestCase):

    def setUp(self):
        self.test_instance = TestModel.objects.create(
            text='searchable text goes here',
        )
        self.test_instance.refresh_from_db()

    def test_init(self):
        # text field should be set
        self.assertTrue(self.test_instance.text)
        # and the vector field should populate
        self.assertEqual(self.test_instance.text_vector, "'goe':3 'searchabl':1 'text':2")

    def test_vector_auto_update(self):
        text = 'new stuff'
        self.test_instance.text = text
        # update and reload from db
        self.test_instance.save()
        self.test_instance.refresh_from_db()
        # new vector shows up
        self.assertEqual(self.test_instance.text_vector, "'new':1 'stuff':2")

    def test_get_searchable_fields(self):
        # `get_searchable_fields` returns a generator so we
        # check with all instead of len
        self.assertTrue(
            all(
                isinstance(
                    field,
                    SearchableTextField,
                ) for field in TestModel.get_searchable_fields()
            )
        )

    def test_search(self):
        self.assertEqual(len(TestModel.objects.search('text')), 1)
        self.assertEqual(len(TestModel.objects.search('searchable')), 1)
        self.assertEqual(len(TestModel.objects.search('bob')), 0)
