
from django_search.models import SearchableModel, SearchableTextField

class DjangoSearchModelTests(object):

    def test_init(self):

        class TestModel(SearchableModel):

            text = SearchableTextField()

        test = TestModel()
