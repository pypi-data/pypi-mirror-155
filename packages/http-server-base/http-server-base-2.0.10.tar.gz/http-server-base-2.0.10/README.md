# HTTP Server Base
This project is a Tornado-based HTTP-server base for easier development.
The repository also includes a very simple example server.

### Features
 - Easy deployment;
 - Implemented logging;
 - Automated Request Id generation;
 - Implemented configuration loading;
 - Methods for proxying requests.

### Installation
##### Requirements
Please, note, that Python 3.6.0+ is required for this tool.

##### Installation with PyPI
```bash
python3.6 -m pip install http-server-base
```

##### Manual Installation
1. Clone the repository
2. Run as sudo/admin: `python3.6 -m pip install -e .`
3. Import to your project: `import http_server_base`

### Usage
##### Starting Simple Server
You can start simple HTTP server that logs all requests via console:
```bash
python3.6 -m http_server_base [port] [arguments]
```
Default port is 80 if allowed, else 8080
Arguments should be passed in format `name=value`

### Useful Links
 - [Tornado Project Page](http://www.tornadoweb.org/en/stable/)
 - [Python 3.6.0 Release Notes](https://www.python.org/downloads/release/python-360/)
