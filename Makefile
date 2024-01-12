run-server:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

migrations:
	python3 manage.py makemigrations

create-su:
	python3 manage.py createsuperuser

install:
	pip install -r requirements.txt

shell:
	python3 manage.py shell
