FROM docker.io/python:3.9

WORKDIR /app
COPY . ./
RUN export GIT_REVISION=$(git rev-parse --short HEAD); echo "GIT COMMIT $GIT_REVISION"
RUN pip install -r requirements.txt

CMD ["gunicorn", "audiophiler:app"]
