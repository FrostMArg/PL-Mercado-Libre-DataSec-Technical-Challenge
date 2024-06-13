
# System Failures

## How to run this project?
To execute these commands, remember to be positioned in the root folder of the project.
```
cd system_failures/
```

This project was implemented using python3.11.

The easiest way to run this project is by using `docker-compose` and `docker` since we have a dependency on MySQL. I find the easiest way to boot up a MySQL instance is by using `docker-compose`.

Recommended commands is to run:
`docker-compose up`

This command will boot up a MySQL service creating a `hackerads` DB. After that will execute the `hackerads` service where data will be submitted the first time it runs. After that executions will only execute the query to respond to the challenge. Subsequent executions will require the command: `docker-compose up hackerads`

Another way to run the project is by ONLY booting up the 'mysql' service using docker-compose: `docker-compose up mysql-db`

And then run python locally by:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Dependencies
This project dependencies are `sqlalchemy` and `mysql-connector-python`.

Note: There is a 2 second delay when running the hackerads service with docker-compose because even when we are relying on the `depends_on` attribute to wait for the mysql service to boot up, docker-compose considers the service running even before the DB is created.

