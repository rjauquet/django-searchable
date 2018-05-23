from django.contrib.postgres.search import SearchVectorField, SearchQuery
from django.db import models

from django_search.exceptions import SearchableException

class SearchableTextField(models.TextField):
    pass

class SearchableManager(models.Manager):

    def search(self, query, fields=None):
        '''
        query is either a string or list of terms or SearchQuery object
        '''
        return self

class SearchableModel(models.Model):

    objects = SearchableManager()

    def __init__(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, SearchableTextField):
                vector_field_name = f'{field.name}_vector'
                if vector_field_name in self._meta.get_fields():
                    raise SearchableException(
                        'Error trying to create vector field. '
                        f'Field with name "{vector_field_name}" already exists'
                    )
                setattr(self, vector_field_name, SearchVectorField(null=True))

    class Meta:
        abstract = True
