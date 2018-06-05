import operator
import shlex
from functools import reduce

from django.apps import AppConfig
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (CombinedSearchQuery, SearchQuery,
                                            SearchRank, SearchVector,
                                            SearchVectorField)
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


class SearchableQuerySet(models.QuerySet):

    def _generate_search_field_names(self, fields=None):
        for field in self.model.get_searchable_fields():
            if fields is None or field.name in fields:
                yield (field.vector_name, f'{field.name}_rank')

    def _get_query(self, query):
        # allow passing in of complex query objects
        if isinstance(query, (CombinedSearchQuery, SearchQuery)):
            return query

        if isinstance(query, list):
            terms = query
        else:
            try:
                terms = shlex.split(query)
            except ValueError:
                terms = query.replace("'", '').replace('"', '').split()

        return reduce(operator.or_, [SearchQuery(term) for term in terms])

    def search(self, query, fields=None):
        '''
        query is either a string or list of terms or SearchQuery object
        '''
        query = self._get_query(query)
        ranks = {}
        rank = 0
        for vector_name, rank_name in self._generate_search_field_names(fields=fields):
            ranks[rank_name] = SearchRank(models.F(vector_name), query)
            rank += models.F(rank_name)

        return self.annotate(
            **ranks,
        ).annotate(
            rank=rank,  # all ranks added together
        ).filter(
            rank__gt=0.0,
        ).order_by('-rank')


class SearchableModel(models.Model):

    objects = SearchableQuerySet.as_manager()

    class Meta:
        abstract = True

    @classmethod
    def get_searchable_fields(cls):
        for field in cls._meta.get_fields():
            if isinstance(field, SearchableTextField):
                yield field

    def save(self, *args, **kwargs):
        Model = type(self)
        previous = Model.objects.get(id=self.id) if self.id else None
        super(SearchableModel, self).save(*args, **kwargs)

        updates = {'id': self.id}
        for field in self.get_searchable_fields():
            if previous is None or getattr(previous, field.name) != getattr(self, field.name):
                updates[field.vector_name] = SearchVector(field.name)

        if len(updates) > 1:
            Model.objects.update(**updates)
