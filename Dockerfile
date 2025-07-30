FROM python:3.12.3-slim

WORKDIR /app

ENV POETRY_HOME=/opt/poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --only main


COPY src ./service

WORKDIR /app/service

EXPOSE 8000

CMD ["python", "main.py"]