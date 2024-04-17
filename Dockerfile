FROM python:3.9.19-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Set environment variables
ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_HOST=""
ENV DB_PORT=""

CMD bash run.sh --db-name $DB_NAME --db-user $DB_USER --db-pass $DB_PASSWORD --db-host $DB_HOST --db-port $DB_PORT