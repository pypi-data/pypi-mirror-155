# ShittyWebserver

An tiny WebAPI that does some normal things and some weird thing for testing web consuming code.

- [ShittyWebserver](#shittywebserver)
  - [API](#api)
  - [Run](#run)
    - [Python](#python)
    - [Docker](#docker)

## API

[OpenAPI Doc](/docs/openapi.json#/)

## Run

### Python

`pip install shittywebserver`

```python
from shittywebserver import run_shitty_webserver
run_shitty_webserver(
    host = "0.0.0.0",
    port = 8000,
    run_in_subprocess = False)
```
### Docker

`docker pull registry-gl.connect.dzd-ev.de:443/dzdpythonmodules/shittywebserver:prod`

`docker run -p 8000:8000 registry-gl.connect.dzd-ev.de:443/dzdpythonmodules/shittywebserver:prod`