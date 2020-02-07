FROM python:3.8.1-slim-buster

COPY sensat /opt/sensat

RUN pip install /opt/sensat

EXPOSE 8000

WORKDIR /opt/sensat
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8000", "sensat.main" ]
