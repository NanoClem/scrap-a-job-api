FROM python:3.10.4

ARG POETRY_V

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_V} python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /project

# Cache requirements
COPY poetry.lock pyproject.toml /project/

# Init poetry project
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-interaction --no-ansi

# Uvicorn is located here under poetry
ENV PATH="${PATH}:/root/.local/share/pypoetry/venv/bin"

COPY . /project

EXPOSE 5000

# CMD ["tail", "-f", "/dev/null"]
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]