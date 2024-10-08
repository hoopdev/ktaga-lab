FROM python:3.12-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update

WORKDIR /app
RUN uv init
RUN uv add ktaga-lab --extra kt