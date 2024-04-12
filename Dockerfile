FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir psycopg2-binary pandas

CMD ["bash", "run.sh"]