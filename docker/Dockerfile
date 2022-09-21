FROM python:3.10.4

ARG POETRY_V

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install poetry
ENV PATH="${PATH}:/root/.local/bin"
ENV PATH="${PATH}:/root/.local/share/pypoetry/venv/bin"
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_V} python -

WORKDIR /project

# Cache build requirements
COPY poetry.lock pyproject.toml /project/

# Init poetry project
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /project

EXPOSE 5000

ENTRYPOINT ["uvicorn", "src.api.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]