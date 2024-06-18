FROM python:3.12-bullseye

RUN apt-get update
RUN pip install --upgrade pip

WORKDIR /app

RUN pip install ktaga-lab[full]

EXPOSE 8888
ENTRYPOINT ["jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
