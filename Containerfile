FROM docker.io/python:3.9

WORKDIR /app
COPY . ./
RUN git rev-parse --short HEAD > commit.txt
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0", "audiophiler:app"]
