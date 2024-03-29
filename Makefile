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

collect:
	rm -r static/ || true
	python manage.py collectstatic

git-pull:
	git stash push db.sqlite3
	git pull
	git stash pop

serve:
	clear -x
	python manage.py runserver

browser:
	sqlitebrowser db.sqlite3 &

count-lines:
	find src/ templates/ static/icons.css static/style.css Makefile \
	 | xargs wc -l \
	 || true