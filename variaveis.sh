#!/bin/bash

CONTAINER_NAME="pipeline-etl-airflow-s3-airflow-webserver-1"  # Substitua pelo nome do contêiner do Airflow

# Verificar se o contêiner está em execução
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "Configurando variáveis no Airflow dentro do contêiner..."

    docker exec -it "$CONTAINER_NAME" airflow variables set script_etl_path "/opt/airflow/scripts/etl.py"
    docker exec -it "$CONTAINER_NAME" airflow variables set script_ingestao_path "/opt/airflow/scripts/ingestao.py"
    # Credenciais AWS
    docker exec -it "$CONTAINER_NAME" airflow variables set aws_access_key "sua_aws_access_key" 
    docker exec -it "$CONTAINER_NAME" airflow variables set aws_secret_key "sua_aws_secret_key"
    docker exec -it "$CONTAINER_NAME" airflow variables set aws_session_token "seu_aws_session_token"
    docker exec -it "$CONTAINER_NAME" airflow variables set region "sua_regiao"
    docker exec -it "$CONTAINER_NAME" airflow variables set key_kms "sua_chave_kms"
    docker exec -it "$CONTAINER_NAME" airflow variables set bucket_name "seu_bucket_name"
    docker exec -it "$CONTAINER_NAME" airflow variables set start_date "2025-01-01"

    echo "Todas as variáveis foram configuradas com sucesso no Airflow."
else
    echo "Erro: O contêiner '$CONTAINER_NAME' não está em execução."
fi
