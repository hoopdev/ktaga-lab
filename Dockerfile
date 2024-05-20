# vi Dockerfile
FROM python:3.12-bullseye

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY pyproject-env.toml ./pyproject.toml

RUN poetry install
RUN poetry add ktaga-lab

ENTRYPOINT ["poetry", "run", "jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
