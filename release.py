'''
1. Change setup.py version
2. Commit all changes for release
3. Tag commit with new version
3. Remove any old build/ or dist/ dirs
4. Build new release
    python setup.py sdist bdist_wheel
5. Upload to PYPI
    Test:
        twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    Production:
        twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
'''
