#FROM docker.io/python:3.13-alpine
FROM ghcr.io/astral-sh/uv:python3.9-alpine

RUN apk add git

WORKDIR /app
COPY . ./
RUN git rev-parse --short HEAD > commit.txt
RUN uv pip install -r requirements.txt --system

CMD ["gunicorn", "-b", "0.0.0.0", "audiophiler:app"]
