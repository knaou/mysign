FROM python:3.7

ENV ENVIRONMNET "PRODUCTION"
ENV DB_FILE "/app/data/db.sqlite3"

COPY env/requirements.txt /tmp/requirements.txt
RUN apt update && \
    apt install -y openssl make gcc && \
    pip3 install -r /tmp/requirements.txt && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/public /app/public-src
COPY server /app/server
WORKDIR /app/server
RUN (echo 'yes' | python3 manage.py collectstatic) && mv /app/server/static /app/public-src/static
COPY build/* /app/public-src/

COPY env/uwsgi.ini /app/server/uwsgi.ini
COPY env/run.sh /app/run.sh
RUN chmod +x /app/run.sh

VOLUME /app/data
VOLUME /app/public
EXPOSE 9090
CMD ["/app/run.sh"]
