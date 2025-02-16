up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

run-backend:
	docker-compose exec django sh -c "pip install -r requirements.txt && python manage.py migrate && uvicorn --host 0.0.0.0 --reload configs.asgi:application"

run-frontend:
	docker-compose up -d frontend
	docker-compose exec frontend sh -c 'npm run start --host 0.0.0.0'

build-backend:
	docker-compose build django

build-frontend:
	docker-compose up -d frontend
	docker-compose exec frontend sh -c "npm install && npm run build"

pip-compile:
	docker-compose run --rm django sh -c "pip install pip-tools && pip-compile"

migrations:
	docker-compose up -d django
	docker-compose exec django python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))
	
.migrations:
	docker-compose exec django python manage.py makemigrations 

migrate:
	docker-compose exec django python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

.migrate:
	docker-compose up -d django
	docker-compose exec django python manage.py migrate

.migrate-migrations: .migrations .migrate

delete-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

.reset-db:
	docker-compose up -d postgres
	docker-compose exec postgres dropdb -U postgres --if-exists sensor_db
	docker-compose exec postgres createdb -U postgres sensor_db

init-db: .reset-db .migrate-migrations
	docker-compose exec django python manage.py init_db