from django.test import TestCase
from django_search.models import SearchableModel, SearchableTextField
from tests.models import TestModel

class DjangoSearchModelTests(TestCase):

    def test_init(self):

        test = TestModel.objects.create(
            text='searchable text goes here',
        )

