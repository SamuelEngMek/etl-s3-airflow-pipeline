#!/bin/bash

# Criar as pastas necessárias para o Airflow
mkdir -p ./logs ./plugins ./config

# Gerar o arquivo .env com o AIRFLOW_UID, necessário para evitar problemas de permissão
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Subir os serviços definidos no docker-compose.yml
echo "Iniciando os serviços com Docker Compose..."
docker compose up airflow-init
docker compose up -d

# Aguardar um tempo para garantir que o Airflow esteja totalmente iniciado
echo "Aguardando o Airflow iniciar..."
sleep 30 

# Verificar o status dos serviços
echo "Verificando o status dos contêineres..."
docker compose ps