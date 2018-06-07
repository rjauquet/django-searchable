import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django_searchable',
    packages=setuptools.find_packages(),
    long_description=long_description,
    version='0.1',
    description='Easy FTS with Django and PostgreSQL',
    author='Rob Ervin Jauquet',
    author_email='rjauquet@gmail.com',
    url='https://github.com/rjauquet/django-searchable',
    download_url='https://github.com/rjauquet/django-searchable/archive/0.1.tar.gz',
    keywords=['search', 'searchable', 'fts'],
    classifiers=[],
)
