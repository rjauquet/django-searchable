from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchVectorField
from django.db import models
from django.db.models.signals import class_prepared

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

    class Meta:
        abstract = True


def inject_vector_fields(sender, **kwargs):

    if SearchableModel in sender.__bases__:

        added_field_names = []

        for field in sender._meta.get_fields():
            if isinstance(field, SearchableTextField):
                vector_field_name = f'{field.name}_vector'

                # make sure the field doesn't already exist with this name
                if vector_field_name in sender._meta.get_fields():
                    raise SearchableException(
                        'Error trying to create vector field. '
                        f'Field with name "{vector_field_name}" already exists'
                    )

                vector_field = SearchVectorField(f'SearchVector storage for {field.name}', null=True)
                vector_field.contribute_to_class(sender, vector_field_name)
                added_field_names.append(vector_field_name)

        # add indexes
        if added_field_names:
            sender._meta.indexes.append(GinIndex(fields=added_field_names))



class_prepared.connect(inject_vector_fields)
