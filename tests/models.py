from django_search.models import SearchableModel, SearchableTextField

class TestModel(SearchableModel):

    text = SearchableTextField()
