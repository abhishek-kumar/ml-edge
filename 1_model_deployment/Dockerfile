FROM python:3.10.11 as generate-requirements

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.11 as prediction-service

WORKDIR /code

COPY --from=generate-requirements /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY model.joblib /code

CMD ["uvicorn", "app.prediction_service:app", "--host", "0.0.0.0", "--port", "8000"]