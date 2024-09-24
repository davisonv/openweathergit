FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN apt-get update && apt-get install -y curl gcc python3-dev python3-distutils libpq-dev

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-root

EXPOSE 8000
CMD poetry run uvicorn --host 0.0.0.0 app.app:app