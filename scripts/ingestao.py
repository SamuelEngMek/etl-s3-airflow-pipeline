import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import boto3
import os
import argparse

# Configuração do Faker
fake = Faker('pt_BR')

# Recebe as credenciais do Airflow
parser = argparse.ArgumentParser(description="Script de ingestão para o Airflow")
parser.add_argument('--aws_access_key', type=str, help='AWS Access Key')
parser.add_argument('--aws_secret_key', type=str, help='AWS Secret Key')
parser.add_argument('--aws_session_token', type=str, help='AWS Session Token')
parser.add_argument('--region', type=str, help='Região AWS')
parser.add_argument('--key_kms', type=str, help='Key KMS')
parser.add_argument('--bucket_name', type=str, help='Nome do Bucket S3')
parser.add_argument('--data_atual', required=True, help='Data do dados')

# Parseando os argumentos
args = parser.parse_args()

# Inicializar o cliente S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=args.aws_access_key,
    aws_secret_access_key=args.aws_secret_key,
    aws_session_token=args.aws_session_token,
    region_name=args.region
)

# Funções auxiliares
def gerar_lojas():
    lojas = ["Loja São Paulo", "Loja Rio de Janeiro", "Loja Salvador", "Loja Porto Alegre",
             "Loja Belo Horizonte", "Loja Recife", "Loja Curitiba", "Loja Fortaleza", "Loja Manaus", "Loja Campinas"]
    return random.choice(lojas)

def gerar_tipo_produto():
    tipos_produto = ["Eletrônicos", "Vestuário", "Calçados", "Acessórios", "Alimentos", "Móveis", "Esportes", "Saúde e Beleza"]
    return random.choice(tipos_produto)

def gerar_meio_pagamento():
    meios_pagamento = ["Cartão de Crédito", "Boleto Bancário", "Pix", "Transferência Bancária", "Dinheiro"]
    return random.choice(meios_pagamento)

def gerar_preco_com_centavos(min_preco=1, max_preco=10000):
    return round(random.uniform(min_preco, max_preco), 2)

# Gerar dados e salvar diariamente no S3

num_registros = 100  # Quantidade de registros por dia

# Gerar os dados
data = {
    "id": [fake.uuid4()[:8] for _ in range(num_registros)],
    "nome": [fake.name() for _ in range(num_registros)],
    "email_cliente": [fake.email() for _ in range(num_registros)], 
    "cep_cliente": [fake.postcode() for _ in range(num_registros)],
    "preco": [gerar_preco_com_centavos() for _ in range(num_registros)],
    "categoria_produto": [gerar_tipo_produto() for _ in range(num_registros)],
    "quantidade_comprada": [random.randint(1, 10) for _ in range(num_registros)],
    "loja": [gerar_lojas() for _ in range(num_registros)],
    "meio_pagamento": [gerar_meio_pagamento() for _ in range(num_registros)],
    "cancelado": [random.choices(["Sim", "Não"], weights=[0.1, 0.9])[0] for _ in range(num_registros)],
    "hora_transacao": [fake.time() for _ in range(num_registros)],
    "data_venda": [args.data_atual for _ in range(num_registros)],
    }

# Criar DataFrame
df = pd.DataFrame(data)

# Salvar localmente como CSV temporário
file_name = f"vendas_{args.data_atual}.csv"
df.to_csv(file_name, index=False)

# Caminho no S3
s3_key = f"bronze/vendas/{file_name}"

# Fazer upload para o S3 com criptografia KMS
s3_client.upload_file(
    Filename=file_name,
    Bucket=args.bucket_name,
    Key=s3_key,
    ExtraArgs={
        "ServerSideEncryption": "aws:kms",
        "SSEKMSKeyId": args.key_kms # Use sua KMS Key
        }
    )

print(f"Arquivo {file_name} enviado para {args.bucket_name}/{s3_key} com criptografia KMS.")

# Remover o arquivo local após o upload
os.remove(file_name)
print("Processo concluído. Todos os arquivos foram enviados para o S3.")