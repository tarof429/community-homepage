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
- DB-based (DAO) tests

To run:

```sh
python -m pytest
```

## Development

The schema is managed with Flask-Migrate. It supports 3 environments: test, dev and prod. These are defined in `config.py`. Below is an explanation of these environments:

- The `test` environment uses an in-memory SQLite database
- The `dev` environment uses a SQLite database persisted to a file
- The `prod` environment uses an external database such as postgres

When updating the schema, 

1. Make sure you have set your environment variables for Flask. For example:

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=True
export RUNTIME_MODE=dev
```

2. Create a migration: `flask db migrate -m "Add a new column`

3. Apply the changes: `flask db upgrade`

Do NOT remove the instance directory.

## Running

Make sure your environment variables are set correctly.

For example, for the `dev` environment:

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=True
export RUNTIME_MODE=dev
```

Then:

```sh
flask run
```

For the `prod` environment, be sure to set DATABASE_URI. Below is the URI for the Postgres docker container.

```sh
export DATABASE_URI=postgresql://admin:secret@localhost:5432/db
```

## References

https://flask-migrate.readthedocs.io/en/latest/
