# Makefile for managing Spark cluster + running jobs

# Configuration — adjust if needed
COMPOSE_FILE := docker-compose.yml
MASTER_CONTAINER := spark-master
SPARK_SUBMIT := /opt/spark/bin/spark-submit
SPARK_MASTER_URL := spark://spark-master:7077
WORKSPACE := workspace

.PHONY: all up down build clean logs masterui historyui run shell

all: up

build:
	docker compose -f $(COMPOSE_FILE) build

up:
	docker compose -f $(COMPOSE_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) down -v

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

masterui:
	@echo "Open in browser: http://localhost:8080"

historyui:
	@echo "Open in browser: http://localhost:18080"

# Target to “login” (open a bash shell) in master container
shell:
	docker exec -it $(MASTER_CONTAINER) /bin/bash
