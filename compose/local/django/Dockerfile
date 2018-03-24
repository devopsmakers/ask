FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > \
  /etc/apt/sources.list.d/pgdg.list \
  && apt-get update \
  && apt-get install postgresql-client-9.6 -y --force-yes \
  && rm -rf /var/lib/apt/lists/*

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --upgrade pip \
  && pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/local/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
