import pandas as pd
from datetime import datetime, timedelta
import boto3
import io
import argparse

# Habilita o Pandas a mostre avisos explícitos sobre o downcasting automático.
pd.set_option('future.no_silent_downcasting', True)

# Recebe as credenciais do Airflow
parser = argparse.ArgumentParser(description="Script de ingestão para o Airflow")
parser.add_argument('--aws_access_key', type=str, help='AWS Access Key')
parser.add_argument('--aws_secret_key', type=str, help='AWS Secret Key')
parser.add_argument('--aws_session_token', type=str, help='AWS Session Token')
parser.add_argument('--region', type=str, help='Região AWS')
parser.add_argument('--key_kms', type=str, help='Key KMS')
parser.add_argument('--bucket_name', type=str, help='Nome do Bucket S3')

# Recebe o mes atual
parser.add_argument('--mes_atual', required=True, type=str)

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

def listar_arquivos(bucket, prefixo):
    """Lista os arquivos no bucket com base no prefixo."""
    arquivos = []
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefixo)
    if "Contents" in response:
        for obj in response["Contents"]:
            arquivos.append(obj["Key"])
    return arquivos

def carregar_arquivo(bucket, key):
    """Carrega um arquivo CSV do S3 e retorna um DataFrame."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(response["Body"])

def salvar_no_silver(df, bucket, caminho):
    """Salva um DataFrame como parquet no bucket silver."""
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, engine="pyarrow", index=False)
    parquet_buffer.seek(0)
    s3_client.put_object(Bucket=bucket, Key=caminho, Body=parquet_buffer.getvalue())
    
def padronizar_cep(cep):
    cep = cep.replace("-", "")  # Remove traços
    return f"{cep[:5]}-{cep[5:]}"  # Adiciona traço no formato correto

def processar_mes(mes):
    """Processa os arquivos de um mês específico."""
    prefixo = f"bronze/vendas/vendas_{mes}"
    arquivos_mes = listar_arquivos(args.bucket_name, prefixo)
    
    dfs = []
    for arquivo in arquivos_mes:
        df = carregar_arquivo(args.bucket_name, arquivo)
        dfs.append(df)
    
    # Concatenar e limpar dados
    df_completo = pd.concat(dfs)
    # Transformar a coluna "devolvido" para valores booleanos (True/False)
    df_completo["cancelado"] = df_completo["cancelado"].map({"Sim": True, "Não": False}).fillna(False)
    # Excluir as vendas que foram devolvidas
    df_completo = df_completo[df_completo["cancelado"] == False]
    # Excluir nome de clientes
    df_completo = df_completo.drop(columns=["nome"])
    # Excluir nome de clientes
    df_completo = df_completo.drop(columns=["email_cliente"])
    # Criar uma nova coluna de total de vendas
    df_completo["total_venda"] = df_completo["preco"] * df_completo["quantidade_comprada"]
    # Converter a coluna 'preco' para string e substituir o ponto por vírgula
    df_completo['preco'] = df_completo['preco'].apply(lambda x: f"{x:.2f}")  # Formatar como string com duas casas decimais
    df_completo['preco'] = df_completo['preco'].str.replace('.', ',', regex=False)
    # Transformar a coluna "devolvido" para valores booleanos (True/False)
    df_completo["cancelado"] = df_completo["cancelado"].map({"Sim": True, "Não": False}).fillna(False)
    # Aplicar a padronização na coluna 'cep_cliente'
    df_completo['cep_cliente'] = df_completo['cep_cliente'].apply(padronizar_cep)
    # Inferir o tipo de objeto nas colunas
    df_completo = df_completo.infer_objects(copy=False)
    
    # Organizar dados para salvar na camada silver
    for loja, dados_loja in df_completo.groupby("loja"):
        for produto, dados_produto in dados_loja.groupby("categoria_produto"):
            caminho = f"silver/vendas/{mes}/{loja}/{produto}/dados.parquet"
            salvar_no_silver(dados_produto, args.bucket_name, caminho)
            print(f"Dados salvos em: {caminho}")
    print("Dados salvos com sucesso!!!")        

# Processar somente o mês atual
processar_mes(args.mes_atual)