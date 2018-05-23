Django Search
==============

Easy full text search with Django and PostgreSQL. Sane defaults + auto creation of vector fields, indexes, and database triggers.


Example
--------------

Extend your model with the :code:`SearchableModel` class, and use the :code:`SearchableTextField` class to automatically setup full text search:

.. code-block:: python

    from django.db.models import TextField
    from django_search.models import SearchableModel, SearchableTextField

    class Blog(SearchableModel):
        author_name = TextField() # will NOT have FTS setup automatically
        title = SearchableTextField() # will have FTS setup automatically
        text = SearchableTextField() # will have FTS setup automatically

Then search away via the Blog manager:

.. code-block:: python

    # takes a string of space separated terms
    results = Blog.objects.search('spiderman suits')

    # or a list of terms
    results = Blog.objects.search(['water', 'baskets', 'leaking'])

    # or a SearchQuery object
    from django.contrib.postgres.search import SearchQuery
    query = ~SearchQuery('superman') & SearchQuery('batman')
    results = Blog.objects.search(query)

:code:`.search` adds a :code:`rank` annotation and automatically filters and sorts the resulting queryset.

By default, :code:`.search` will search through all :code:`SearchableTextField` fields on the model, but you can specify any subset:

.. code-block:: python

    results = Blog.objects.search('who is venom', fields=['title'])

Contributing
--------------

.. code-block:: python

    pipenv install
    pipenv run pytest
