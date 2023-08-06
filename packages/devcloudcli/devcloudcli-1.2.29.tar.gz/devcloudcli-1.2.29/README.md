## Create and upload PYPI package

```sh
python3 -m build 
pip3 install twine
twine upload dist/*
```