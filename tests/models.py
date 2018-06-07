from django_searchable.models import SearchableModel, SearchableTextField

class TestModel(SearchableModel):

    text = SearchableTextField()
