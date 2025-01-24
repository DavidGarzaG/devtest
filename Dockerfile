FROM python:latest

WORKDIR /devtest

COPY ./devtest .

CMD ["sh", "-c", "python migrations.py"]
