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

## Implementation Notes

This application uses Flask and SQLAlchemy to manage events. The web interface is styled using Bootstrap. 

## Testing

This project implements the following tests:

- Unit tests
- DB-based (DAO) ests

To run:

```sh
python -m pytest
```