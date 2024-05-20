# vi Dockerfile
FROM python:3.12-bullseye

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install 
RUN poetry add jupyterlab_theme_solarized_dark

ENTRYPOINT ["poetry", "run", "jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
