CONTAINER_NAME=faust

build:
	docker build -t $(CONTAINER_NAME) .

run-kafka:
	docker build -t $(CONTAINER_NAME) .
	docker-compose up -d

kill:
	docker-compose down

run-producer:
	python producer.python

run-faust:
	faust -A faust_worker worker -l info

update:
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes