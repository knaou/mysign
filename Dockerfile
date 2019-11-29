FROM node as client
RUN npm install -g yarn
COPY client /work/src
WORKDIR /work/src
RUN yarn install && yarn build

FROM python:3.7
ENV ENVIRONMNET "PRODUCTION"
ENV DB_FILE "/app/data/db.sqlite3"
COPY env/requirements.txt /tmp/requirements.txt
RUN apt update && \
    apt install -y nginx openssl supervisor make gcc && \
    pip3 install -r /tmp/requirements.txt && \
    apt remove -y gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY env/supervisord.conf /app/supervisord.conf

COPY env/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /app/public /app/public-src
COPY server /app/server
WORKDIR /app/server
RUN (echo 'yes' | python3 manage.py collectstatic) && mv /app/server/static /app/public-src/static
COPY --from=client /work/build/* /app/public-src/

COPY env/uwsgi.ini /app/server/uwsgi.ini
COPY env/run.sh /app/run.sh
RUN chmod +x /app/run.sh

VOLUME /app/data
EXPOSE 80
CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]

