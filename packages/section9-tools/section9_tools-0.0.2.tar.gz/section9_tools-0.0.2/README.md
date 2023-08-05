# daily tools

# venv

    make venv
    source ./venv/bin/activate
    python -m pip install '.[dev,test]'

# build and upload to pypi

    python -m pip install --upgrade pip wheel
    python -m pip install --upgrade build
    python -m build
    python -m twine upload --repository testpypi dist/*
    python -m twine upload --repository pypi dist/*
