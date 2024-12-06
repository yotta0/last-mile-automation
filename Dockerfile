FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3.11-dev libpq-dev gcc

WORKDIR /app

COPY ./src /app/src
COPY .env /app/.env
COPY run.sh /app/run.sh
COPY alembic.ini /app/alembic.ini
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000

CMD ["bash", "/app/run.sh"]
