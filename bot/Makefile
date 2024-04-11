export PYTHONPATH = $(PWD)
include .env

APPLICATION_NAME = hunt
CODE = $(APPLICATION_NAME)


run:  ##@Application Run application
	python3 $(APPLICATION_NAME)/__main__.py

db:  ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up -d --remove-orphans

lint:  ##@Code Check code with pylint
	python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	python3 -m isort $(CODE)
	python3 -m black $(CODE)

open_db:  ##@Database Open database inside docker-image
	docker exec -it scavenger_hunt_db psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

revision:  ##@Database Create new revision file automatically with prefix
	cd $(APPLICATION_NAME)/db && alembic revision --autogenerate

migrate:  ##@Database Do all migrations in database
	cd $(APPLICATION_NAME)/db && alembic upgrade head

fill_tasks:  ##@Database Fill the database with tasks from json
	python3 $(APPLICATION_NAME)/tasks_to_db/fill_db.py

build_results:  ##@Database Move scoreboard to the excel file
	python3 $(APPLICATION_NAME)/utils/build_results.py
