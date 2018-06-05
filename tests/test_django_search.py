from django.test import TestCase
from django_search.models import SearchableModel, SearchableTextField
from tests.models import TestModel

class DjangoSearchModelTests(TestCase):

    def test_init(self):

        test_instance = TestModel.objects.create(
            text='searchable text goes here',
        )
        test_instance.refresh_from_db()
        self.assertTrue(test_instance.text)
        self.assertTrue(test_instance.text_vector)
