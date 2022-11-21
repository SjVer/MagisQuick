SHELL := /bin/bash

start_all_over:
	rm -r venv
	python3 -m venv venv
	source venv/bin/activate
	which pip
	pip install django

migrate:
	python manage.py migrate --run-syncdb

freeze:
	python -m pip freeze > requirements.txt

serve:
	clear -x
	python manage.py runserver

browser:
	sqlitebrowser db.sqlite3 &
