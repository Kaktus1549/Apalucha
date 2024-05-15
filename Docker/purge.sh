#!/bin/bash

# Stopping the Docker containers
echo "Stopping docker-apalucha-backend, docker-apalucha-frontend and database containers..."
docker stop docker-apalucha-backend-1 docker-apalucha-frontend-1 docker-db-1

# Removing the Docker containers
echo "Removing docker-apalucha-backend, docker-apalucha-frontend and database containers..."
docker rm docker-apalucha-backend-1 docker-apalucha-frontend-1 docker-db-1

echo "Containers stopped and removed successfully."
echo "Removing \"docker_db-data\" volume..."
docker volume rm docker_db-data