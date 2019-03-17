NGINX_IMAGE_NAME := knaou/mysign-nginx
APP_IMAGE_NAME := knaou/mysign-app


.PHONY: all
all: app nginx

.PHONY: prepare
prepare:
	cd client && yarn install

static/index.bundle.js: prepare client/**/*
	cd client && yarn build

.PHONY: app
app: static/index.bundle.js env/Dockerfile.production.app env/run.sh env/uwsgi.ini
	docker build -f env/Dockerfile.production.app -t ${APP_IMAGE_NAME} .

.PHONY: nginx
nginx: env/Dockerfile.production.nginx env/nginx.conf
	docker build -f env/Dockerfile.production.nginx -t ${NGINX_IMAGE_NAME} .

.PHONY: clean
clean:
	rm -f static/index.*
	docker rmi ${APP_IMAGE_NAME}
	docker rmi ${NGINX_IMAGE_NAME}

