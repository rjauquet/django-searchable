from django.apps import AppConfig
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchVectorField
from django.db import models
from django.db.models.signals import class_prepared

from django_search.exceptions import SearchableException


class SearchableTextField(models.TextField):
        def contribute_to_class(self, cls, name):
            if not cls._meta.abstract:
                vector_field_name = f'{name}_vector'

                # make sure the field doesn't already exist with this name
                if hasattr(cls, vector_field_name):
                    raise SearchableException(
                        'Error trying to create vector field. '
                        f'Field with name "{vector_field_name}" already exists'
                    )

                vector_field = SearchVectorField(f'SearchVector storage for {name}', null=True)
                vector_field.contribute_to_class(cls, vector_field_name)
                # add index
                cls._meta.indexes.append(GinIndex(fields=[vector_field_name]))

            super(SearchableTextField, self).contribute_to_class(cls, name)


class SearchableManager(models.Manager):

    def search(self, query, fields=None):
        '''
        query is either a string or list of terms or SearchQuery object
        '''
        return self


class SearchableModel(models.Model):

    objects = SearchableManager()

    class Meta:
        abstract = True
