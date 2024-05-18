# vi Dockerfile
FROM python:3

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY ktaga_lab ./ktaga_lab

RUN poetry install 

ENTRYPOINT ["poetry", "run", "jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
