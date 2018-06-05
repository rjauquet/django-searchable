from django.apps import AppConfig
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchVectorField
from django.db import models
from django.db.models.signals import class_prepared, post_init, post_save
from django.dispatch import receiver

from django_search.exceptions import SearchableException


class SearchableTextField(models.TextField):

    vector_name = None

    def contribute_to_class(self, cls, name):
        if not cls._meta.abstract:
            self.vector_name = f'{name}_vector'

            # make sure the field doesn't already exist with this name
            if hasattr(cls, self.vector_name):
                raise SearchableException(
                    'Error trying to create vector field. '
                    f'Field with name "{self.vector_name}" already exists'
                )

            vector_field = SearchVectorField(f'SearchVector storage for {name}', null=True)
            vector_field.contribute_to_class(cls, self.vector_name)
            # add index
            cls._meta.indexes.append(GinIndex(fields=[self.vector_name]))

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

    def save(self, *args, **kwargs):
        Model = type(self)
        previous = Model.objects.get(id=self.id) if self.id else None
        super(SearchableModel, self).save(*args, **kwargs)

        updates = {'id': self.id}
        for field in self._meta.get_fields():
            if isinstance(field, SearchableTextField):
                if previous is None or getattr(previous, field.name) != getattr(self, field.name):
                    updates[field.vector_name] = SearchVector(field.name)

        if len(updates) > 1:
            Model.objects.update(**updates)
