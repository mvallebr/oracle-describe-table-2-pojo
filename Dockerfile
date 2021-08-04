FROM python:3.8.9-slim-buster

COPY requirements.txt /req/
RUN pip install -r /req/requirements.txt

COPY . /code/
WORKDIR /code

ENTRYPOINT ["pytest" ]