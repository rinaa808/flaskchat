FROM python:3.11
MAINTAINER Ekaterina Shtoiko 'kyzuuer@mail.ru'

ENV FLASK_ENV="docker" \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=1 \
    PYP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python"]

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]
