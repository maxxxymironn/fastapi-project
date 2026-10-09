FROM python:3.13.13-alpine

ENV PATH = "${PATH}:/root/.local/bin"

COPY ./src ./app/src
COPY ./migrations ./app/migrations
COPY ./alembic.ini ./app/alembic.ini
COPY ./images ./app/images
COPY ./requirements.txt ./app/requirements.txt

ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000