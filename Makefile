start:
	source env/bin/activate

stop:
	source env/bin/deactivate

migrate:
	python manage.py migrate

freeze:
	python -m pip freeze > requirements.txt

serve:
	clear -x
	python manage.py runserver