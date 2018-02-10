CMD               ?= test
COMPOSE_FILE      ?= local.yml
export POSTGRES_USER     ?= ask
export POSTGRES_PASSWORD ?= ''

.PHONY: up
up:
	docker-compose -f ${COMPOSE_FILE} up

.PHONY: down
down:
	docker-compose -f ${COMPOSE_FILE} down

.PHONY: manage.py
manage.py:
	docker-compose -f ${COMPOSE_FILE} exec django python manage.py ${CMD}

.PHONY: django-bash
django-bash:
	docker-compose -f ${COMPOSE_FILE} exec django bash
