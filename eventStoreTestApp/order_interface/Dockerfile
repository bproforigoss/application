FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY order_service .

ENV FLASK_APP=order_service

ENV EVENTSTORE_STREAM_URL=http://0.0.0.0:2113/streams

EXPOSE 5001

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]
