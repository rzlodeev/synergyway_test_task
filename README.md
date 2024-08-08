# Auto-updating database with Selenium app demo

## Description

This app features repetitive Celery tasks, that fetch data from external API and save/update data in the database.
Data can be retrieved via FastAPI endpoint or via bash.
API data fetches from 3 sources - 1 from jsonplaceholder.com and 2 tables from
random-data-api.com. First contains info about 10 users, second two contain info about
credit cards and addresses. In database they are all related with such connections:
 - users to credit_cards: One-to-Many relationship
 - users to addresses: Many-to-One relationship
 - credit_cards to addresses: Many-to-One relationship

## Libraries used:
**Selenium** for fetching data from the external websites using Firefox web driver.

**Celery + RabbitMQ** for repetitive tasks launch.

**SQLAlchemy + SQLite** for database operations.

**Docker compose** for containerization.

**PyTest** for tests.

**Flake8** for checking style and quality of code.

## Installation

### Prequisites
  Python (3.11 or higher)
  Git

### Clone the repo
```
git clone https://github.com/rzlodeev/synergyway_test_task.git
cd synergyway_test_task
```

### Setup virtual environment
Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Now you can launch the app.

## Usage

### Launch Docker-compose
```
docker-compose build
docker-compose up
```

This will run docker containers. After ~40 seconds Celery and RabbitMQ
will be set up and start receiving tasks. Also tests will be launched
in app container, and then FastAPI server.

Once the containers are up and running, the FastAPI server will be accessible at `http://127.0.0.1:8000`.
The endpoint for data is:

```
http://127.0.0.1:8000/show-data
```

Please notice, that tasks are running with 30, 40 and 50 minutes interval
(for users, addresses and credit cards accordingly). Until task is done, no
data will be persist in database. However, you can manually fetch it inside the app
by launching app via bash in docker container:

Access the container:
```
docker exec -it synergyway_test_task-app-1 /bin/bash
```

Download data manually:
```
python main.py --update-users
python main.py --update-addresses
python main.py --update-cards
```

You can also retrieve data:
```
python main.py -r
```

## Code format

App features flake8 library to ensure code style. You can check it by launching
```
flake8
```
in docker container (in a same place, where you've launched ```python main.py -r```)

## Testing

App provides tests for features functionality. They are located in /tests
directory.

To launch test, call:

```
pytest
```

Also tests will be launched automatically when building docker containers.

### Testing scenarios:

#### Test db:
test_insert_data: This test ensures, that data can be inserted in the database.
Creates a new user record, address record, updates user record with new address record. Same for credit card info.

test_retrieve_data: This test ensures, that data can be retrieved from the database.
checks functionality of retrieve_data function.

test_update_data: This test ensures, that data can be updated in the database.
Checks functionality of update_record function.

test_delete_data: This test ensures, that data can be deleted from the database.
    Since we previously created 1 record for each table, we will delete entries with id 1 from all tables.

#### Test tasks:

test_fetch_and_refresh: This test ensures, that tasks given to celery fetch data from API

#### Test web driver:

test_get_user_data: This test ensures, that user data can be extracted from corresponding API.
    Checks for 'id' field in given response.

test get_credit_card_data: This test ensures, that credit card data can be extracted from given API.

test_get_address_data: This test ensures, that addresses data can be extracted from the given API.

## Directories structure

- db/database.db: SQLite database file
- src/celery_config.py: Configuration file for celery tasks. (Such as tasks period time)
- src/database_config.py: Configuration of database. Models and CRUD functions.
- src/tasks.py: Celery task functions. The ones that fetch data from API and save it to the database.
- src/web_driver.py: Selenium Firefox web driver.
- tests/db: Test database.
- tests/...py: Test files.
- .flake8: Flake8 config file
- docker-compose.yml: Docker-compose file
- Dockerfile: Dockerfile
- main.py: Handles bash arguments using argparse and launch of the FastAPI server
- README.md: This file.
- requirements.txt: Project dependencies.
