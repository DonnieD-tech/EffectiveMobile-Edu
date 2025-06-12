FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-openbsd && \
    apt-get clean

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
