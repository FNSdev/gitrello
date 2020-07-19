FROM python:3.8.3-slim-buster AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.9 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


FROM base AS build-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y curl git gcc libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev


FROM base as development
RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY --from=build-base $POETRY_HOME $POETRY_HOME
COPY --from=build-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=build-base $VENV_PATH $VENV_PATH
WORKDIR $PYSETUP_PATH
RUN poetry install


FROM base AS test
COPY --from=development $VENV_PATH $VENV_PATH
COPY gitrello/ /home/gitrello
WORKDIR /home/gitrello
RUN . $VENV_PATH/bin/activate
CMD python manage.py test


FROM base as production
COPY --from=build-base $VENV_PATH $VENV_PATH
COPY gitrello/ /home/gitrello
WORKDIR /home/gitrello
RUN . $VENV_PATH/bin/activate
CMD uvicorn gitrello.asgi:application --host 0.0.0.0 --port 80 --workers 4
EXPOSE 80
