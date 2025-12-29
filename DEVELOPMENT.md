# Development

## Initial Setup

This application uses a virtual environment using `pip`. Below is an example of how to create the virtual environment with a directory called venv.

```sh
python -m venv venv
```

To activate it, run:

```sh
. ./venv/bin/activate
```

To deactivate it, run

```sh
deactivate
```

You can use the provided requirements.txt file to install libraries.

```sh
pip install -r requirements.txt
```

## Usage

To run the application:

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=True
flask run
```
