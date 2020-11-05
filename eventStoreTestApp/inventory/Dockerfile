FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY inventory_service .

ENV FLASK_APP=inventory_service

ENV EVENTSTORE_STREAM_URL=http://0.0.0.0:2113/streams

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
