activate:
	if [ -d "venv" ]; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
		python3 -m venv venv; \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	. ./venv/bin/activate

install:
	pip3 install -r requirements.txt

run:
	@if [ -z "$(strip $(PORT))" ]; then \
		flask run; \
	else \
		flask run -p $(PORT); \
	fi

run-docker:
ifeq ($(strip $(PORT)),)
	flask run -h 0.0.0.0
else
	flask run -p $(PORT) -h 0.0.0.0
endif

run-tests:
	make docker-test-up
	FLASK_ENV=test python -m unittest discover -s tests -p '*Test.py' -v
	make docker-test-down

run-tests-coverage:
	make docker-test-up
	FLASK_ENV=test coverage run -m unittest discover -s tests -p '*Test.py' -v
	coverage report -m
	coverage html
	coverage report --fail-under=80
	make docker-test-down
	 
docker-gunicorn:
	  gunicorn -w 4 --bind 127.0.0.1:$(PORT) wsgi:app

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-dev-up:
	docker compose -f=docker-compose.develop.yml up --build

docker-dev-down:
	docker compose -f=docker-compose.develop.yml down

docker-test-up:
	docker compose -f=docker-compose.test.yml up --build -d
	@echo "Waiting for PostgreSQL container to start..."
	@until docker ps | grep 'auth-test-db'; do \
		echo "Database container is still starting..."; \
		sleep 2; \
	done
	@until docker exec auth-test-db pg_isready -U develop; do \
		echo "Waiting for PostgreSQL to start..."; \
		sleep 2; \
	done

docker-test-down:
	make docker-db-truncate
	docker compose -f=docker-compose.test.yml down
	sleep 2

create-database:
	docker exec auth-test-db psql -U develop -d auth-db -f /docker-entrypoint-initdb.d/init.sql

docker-db-truncate:
	docker exec auth-test-db psql -U develop -d auth-db  -c  "TRUNCATE TABLE role CASCADE;"
	docker exec auth-test-db psql -U develop -d auth-db  -c  "TRUNCATE TABLE auth_user CASCADE;"
	docker exec auth-test-db psql -U develop -d auth-db  -c  "TRUNCATE TABLE auth_user_customer CASCADE;"


kubernetes-up:
	kubectl apply -f kubernetes/k8s-configMap.yaml
	kubectl apply -f kubernetes/k8s-secrets.yaml
	kubectl apply -f kubernetes/k8s-deployment.yaml
	kubectl apply -f kubernetes/k8s-ingress.yaml

kubernetes-dev-up:
	make kubernetes-dev-up
	minikube tunnel

kubernetes-dev-down:
	kubectl delete configMap/auth-configmap
	kubectl delete secrets/auth-secrets
	kubectl delete deploy/abcall-auth-api
	kubectl delete ingress/abcall-auth-ingress


