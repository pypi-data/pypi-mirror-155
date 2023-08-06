# somenergia-apinergia-client
Package to read from SomEnergia Apinergia

# Testing

requires pytest>=7 given that we use pythonpath option in pyproject.toml

```console
$ pytest
```

# Packaging

based on [PyPI doc](https://packaging.python.org/en/latest/tutorials/packaging-projects/) v:latest on Jun-2022

```console
$ pip install --upgrade build
$ python3 -m build
```

It might require

```console
$ sudo apt install python3.8-venv
```

### Distribute to TestPyPi

```console
$ pip install --upgrade twine
$ twine upload --repository testpypi dist/*
```

