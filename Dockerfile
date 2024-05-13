FROM python:3.9.19-alpine3.19

WORKDIR /app
RUN pip install --upgrade pip poetry    \
    && pip cache purge
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.create false  \
    && poetry install --only main --no-cache
COPY . ./
