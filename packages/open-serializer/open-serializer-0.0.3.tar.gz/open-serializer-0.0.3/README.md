# Open Serializer

## What is it?

Open-serializer is a Python package providing an quick inferface for serializing and deserializing object.\
For example, `json`, `yaml`, `toml` and etc.

## Main Features

- **Deserialize** severial types of files to python dictionary.
- **Serialize** any python dictionary to severial types of files.
- **Merge dictionary** with multiple dictionary with different keys and values.

## Where to get it

Open-serializer can be installed from PyPI using `pip`:

```bash
pip install open-serializer
```

## Interface

### Serialize and deserialize object

```python
from open_serializer import Serializer

data = Serializer.deserialize_object(path)
Serializer.serialize_object(data, path)
```
