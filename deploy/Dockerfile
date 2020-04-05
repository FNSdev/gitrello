FROM python:3.8.1-slim-buster

WORKDIR /home/gitrello
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc libc6-dev libpq-dev && \
    pip3 install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements_test.txt /home/gitrello/
RUN pip3 install --no-cache -r requirements.txt
COPY gitrello/ /home/gitrello
CMD uvicorn gitrello.asgi:application --host 0.0.0.0 --port 80 --workers 4
EXPOSE 80
