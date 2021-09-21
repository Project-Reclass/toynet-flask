# Mininet ToyNet

This module containerizes and provides interfaces for the backend of ToyNet to
interface with the Mininet emulator implementing the topology that a user builds.

## Building and Running

Building and Running are controlled by the `Makefile`, run `make help` to identify
the appropriate target for your use-case.

There are targets for production and test use-cases; it is recommended to use the 
test series of targets for development.

It will take several minutes the first time for both images, but after the
majority of the images get cached by Docker it will be much faster.

# Installing Dependencies

This library makes some functionality of the Docker Python API more readily
accessible for your use case. This library is intended to facilitate Flask
managing Mininet containers local to its running instance.

## External Repositories

Download mininet: `git submodule update --init --recursive` 

## Installing Python Dependencies

If you are testing code that is managing Docker (therefore cannot be tested in
a container: e.g. `tests/test_orchestration.py`), you can setup your virtual
environment by:

Linux / MacOS:
```
python3 -m venv venv
```

Windows:
```
py -3 -m venv venv
```

Then activate it:

Linux / MacOS:
```
. venv/bin/activate
```

Windows:
```
venv\Scripts\activate
```

Make sure you are using Python 3.x, recommended Python 3.7. Install
dependencies from the `requirements.txt` with:
`pip3 install -r requirements.txt`

Run the `deactivate` command to exit the virtual environment.

# API Documentation

Swagger documentation is available at `/swagger/` for JSON and at
`/swagger-ui/` for interactive browser interface.
