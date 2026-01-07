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

The code for the Python application is located in the `src` directory. 

You can use the provided requirements.txt file to install libraries.

```sh
cd src
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

## Developing

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

For the `prod` environment, be sure to also set DATABASE_URI. Below is the URI for the Postgres docker container.

```sh
export DATABASE_URI=postgresql://admin:secret@localhost:5432/db
```

## Running in Docker

The goals of running this app using docker are:

- Create a docker image using Dockerfile
- Use docker-compose to orchestrate containers
- Deploy our image to a remote docker registry
- Update docker-compose to use the image in the remote docker registry
- Start an EC2 instance and deploy the application to the instance

To build the docker container, run:

```sh
docker -f docker/Dockerfile build -t community-homepage .
```

To run the container, you can run:

```sh
docker run -d -p 5000:5000 --name homepage community-homepage
```

This will use SQLite as the backing database.

To see the logs:

```sh
[taro@zaxman community-homepage]$ docker logs homepage 
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3e4596be74fa, Initial migration
 * Serving Flask app 'app.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 107-418-025
```

This will use the dev configuration but can be overridden. 

The docker-compose file will use Postgres as the backing database.

```sh
docker compose -f docker/docker-compose.yaml up -d
```

There are two services in the docker-compose file. The first service is the Postgres database. The second sevice runs the Flask application. Since the database needs to have the correct schema, this can take a while before it is available for use. To handle this suituation, the docker-compose file defines both a dependency asnd a healthcheck; this pattern is discussed at https://docs.docker.com/compose/how-tos/startup-order/. Furthermore, the Flask application service defines the POSTGRES_URL so that it can connect to the external database. 

To tag and push the docker image to hub.docker.com:

```sh
 docker tag community-homepage tarof429/community-homepage:1.0
 docker push tarof429/community-homepage:1.0
```

In the last step, the goal is to deploy the application to an EC2 instance. The EC2 instance can be created using the AWS console. To install docker on it, see https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-docker.html. 

Make sure the instance opens port 22 for SSH access and 5000 for web access. 

To install docker-compose, see https://github.com/docker/compose?tab=readme-ov-file#linux. Basically,

- Download the latest executable to the EC2 instance.
- Change the permission to executalbe and copy it to /usr/lib/docker/cli-plugins. 
- Run `docker compose up -d`


On the remote server, refresh the image to get the latest code changes.

```sh
docker compose down
docker compose pull
docker compose up -d
```


## References

https://flask-migrate.readthedocs.io/en/latest/
