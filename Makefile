up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

run-backend:
	docker-compose exec django sh -c "pip install -r requirements.txt && python manage.py migrate && uvicorn --host 0.0.0.0 --reload configs.asgi:application"


build:
	docker-compose build

pip-compile:
	docker-compose run --rm django sh -c "pip install pip-tools && pip-compile"

migrations:
	docker-compose exec django python manage.py makemigrations

migrate:
	docker-compose exec django python manage.py migrate
