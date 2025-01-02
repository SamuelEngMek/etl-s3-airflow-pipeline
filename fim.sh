#!/bin/bash

# Parar os serviços definidos no docker-compose.yml
echo "Parando os serviços do Docker Compose..."
docker compose down

# Verificar se todos os contêineres associados foram encerrados
echo "Verificando contêineres ainda em execução..."
docker ps
