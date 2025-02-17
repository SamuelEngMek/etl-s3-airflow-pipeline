from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta

start_date_str = Variable.get("start_date", default_var="2024-01-01").strip('"')  # Pega a variável ou usa o valor padrão
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
start_date = start_date + timedelta(days=1)

# Definindo o DAG
dag = DAG(
    's3_etl_pipeline',
    description='Pipeline para ETL de arquivos no S3',
    schedule_interval="0 0 1 * *",  # Executar no primeiro dia de cada mês
    start_date=start_date,  # Data de início
    catchup=True,  # Permitir execução de tarefas atrasadas
)

# Definindo o comando como template com Jinja
etl_task = BashOperator(
    task_id='run_etl_script',
    bash_command=(
        "python3 {{ var.value.script_etl_path }} "
        "--aws_access_key {{ var.value.aws_access_key }} "
        "--aws_secret_key {{ var.value.aws_secret_key }} "
        "--aws_session_token {{ var.value.aws_session_token }} "
        "--region {{ var.value.region }} "
        "--key_kms {{ var.value.key_kms }} "
        "--bucket_name {{ var.value.bucket_name }} "
        "--mes_atual {{ execution_date.add(months=-1).strftime('%Y-%m') }}"
    ),
    dag=dag,
)
etl_task