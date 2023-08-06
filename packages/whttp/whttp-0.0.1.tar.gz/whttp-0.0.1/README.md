# whttp

Command line interface and Python library wrapper for the [winhttp] library

[winhttp]: https://docs.microsoft.com/en-us/windows/win32/winhttp/about-winhttp

[![PyPi](https://img.shields.io/pypi/v/whttp.svg?style=flat-square)](https://pypi.python.org/pypi/whttp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

# How to install
```bat
pip install whttp
```

# How to use (CLI)
whttp https://www.example.org/

# How to use (Python Library)
```python
from whttp import HTTPClient
client = HTTPClient()
reply = client.get('https://www.example.org/')
print(reply.text)
```
