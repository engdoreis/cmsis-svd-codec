rm -rf dist
python3 setup.py bdist_wheel sdist
twine check dist/*
twine upload -r testpypi dist/*