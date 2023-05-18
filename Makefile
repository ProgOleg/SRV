IMAGE_NAME := srv
CONTAINER_NAME := srv_container
NUM_WORKERS := 2
ENV_FILE := .env

clone:
	git checkout main
	git pull origin main

build:
	sudo docker build --rm -t $(IMAGE_NAME) .

run:
	sudo docker rm -f $(CONTAINER_NAME)
	sudo docker run -d --name $(CONTAINER_NAME) --env-file $(ENV_FILE) -e $(NUM_WORKERS) -p 8000:8000 $(IMAGE_NAME)

run_compose:
	sudo docker-compose --env-file=$(ENV_FILE) --env NUM_WORKERS=$(NUM_WORKERS) up -d

stop:
	sudo docker stop $(CONTAINER_NAME)

rm:
	sudo docker rm $(CONTAINER_NAME)

rmi:
	sudo docker rmi $(IMAGE_NAME)

build_run: build run

all: clone build run

run_compose:
	sudo docker-compose up -d --build

stop_compose:
	sudo docker-compose stop

all_compose: clone run_compose
