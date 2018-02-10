CMD               ?= test
COMPOSE_FILE      ?= local.yml
SERVICE           ?= django
export POSTGRES_USER     ?= ask
export POSTGRES_PASSWORD ?= ''

.PHONY: build
build:
	docker-compose -f ${COMPOSE_FILE} build --force-rm  --pull --no-cache $(SERVICE)

.PHONY: up
up:
	docker-compose -f ${COMPOSE_FILE} up

.PHONY: down
down:
	docker-compose -f ${COMPOSE_FILE} down

.PHONY: manage.py
manage.py:
	docker-compose -f ${COMPOSE_FILE} exec django python manage.py ${CMD}

.PHONY: bash
bash:
	docker-compose -f ${COMPOSE_FILE} exec $(SERVICE) bash
