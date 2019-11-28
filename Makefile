NGINX_IMAGE_NAME := knaou/mysign-nginx
APP_IMAGE_NAME := knaou/mysign-app


.PHONY: all
all: app nginx

.PHONY: app
app:
	docker build -f env/Dockerfile.production.app -t ${APP_IMAGE_NAME} .

.PHONY: nginx
nginx:
	docker build -f env/Dockerfile.production.nginx -t ${NGINX_IMAGE_NAME} .

.PHONY: clean
clean:
	rm -f static/index.*
	docker rmi ${APP_IMAGE_NAME}
	docker rmi ${NGINX_IMAGE_NAME}

