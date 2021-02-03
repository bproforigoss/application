FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY inventory_service .

ENV FLASK_APP=inventory_service

EXPOSE 5000

CMD ["uwsgi" "--http" "127.0.0.1:5000" "--wsgi-file" "__init__.py" "--callable" "app"]
