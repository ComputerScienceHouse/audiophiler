FROM docker.io/python:3.9

WORKDIR /app
COPY . ./

#RUN apt update
#RUN apt install libsasl2-dev

RUN pip install -r requirements.txt
#RUN python setup.py install

ENV FLASK_APP=audiophiler
CMD ["flask", "run"]
