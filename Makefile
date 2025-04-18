# Variables
DOCKER_COMPOSE_FILE=docker-compose.yml
SPARK_MASTER_URL=spark://spark-master:7077
SPARK_SUBMIT_IMAGE=spark-master

# Targets
.PHONY: up down spark-submit

# Start Docker Compose services
up:
	@docker compose -f $(DOCKER_COMPOSE_FILE) up --build

# Stop Docker Compose services
down:
	@docker compose -f $(DOCKER_COMPOSE_FILE) down -v

# Submit a Spark job
spark-submit:
	@if [ -z "$(JOB)" ]; then \
		echo "Error: Please specify a job file using 'make spark-submit JOB=<path-to-job>'"; \
		exit 1; \
	fi
	docker exec -it $(SPARK_SUBMIT_IMAGE) /opt/bitnami/spark/bin/spark-submit \
		--master $(SPARK_MASTER_URL) \
		--deploy-mode client \
		/opt/bitnami/spark/jobs/$(JOB)