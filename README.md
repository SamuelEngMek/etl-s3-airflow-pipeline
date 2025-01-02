# pipeline-etl-airflow-s3

Este repositório implementa um pipeline ETL utilizando Apache Airflow e Amazon S3. O objetivo é simular o processo de ingestão de dados brutos e transformação de dados de uma camada Bronze para a camada Silver, utilizando Docker para orquestrar o ambiente e Airflow para agendar e gerenciar os DAGs.


### Clonar o Repositório

Para começar, clone o repositório para sua máquina local:

```
git clone https://github.com/SamuelEngMek/pipeline-etl-airflow-s3.git
```

### Estrutura do Projeto

O projeto é composto por uma estrutura organizada em diretórios e arquivos necessários para a execução do pipeline:

```
pipeline-etl-airflow-s3/
├── dags/
│ ├── ingestao_dag.py 
│ └── etl_dag.py 
├── scripts/ 
│ ├── ingestao.py 
│ └── etl.py 
├── .gitignore 
├── docker-compose.yml
├── Dockerfile 
├── requirements.txt 
├── inicio.sh
├── variaveis.sh 
└── fim.sh
```

## Descrição dos Componentes

-   **DAGs**: O Airflow executa duass DAGs principais:
    -   **DAG de Ingestão**: Executa um script para ingestão de dados e coloca os dados brutos na camada **Bronze** do S3.
    -   **DAG de ETL**: Transforma os dados da camada Bronze em dados formatados (Parquet) na camada **Silver**, limpando e particionando os dados por mês, loja e categoria de produto.
-   **Scripts**:
    -   **ingestao.py**: Realiza a ingestão dos dados brutos.
    -   **etl.py**: Processa e transforma os dados para a camada Silver.
  
-   **Docker**: O ambiente é configurado utilizando Docker, garantindo a compatibilidade e isolação das dependências do Airflow.


## Rodando o Projeto
### Inicializar o Ambiente

1. **Definir permissões de execução**: Para garantir que o arquivo seja executável, você pode rodar:
```
chmod +x inicio.sh variaveis.sh fim.sh
```

2. **iniciar o projeto**: execute o script `inicio.sh`, que cria as pastas necessárias para o Airflow, sobe a imagem Docker e inicia o serviço do Airflow:

```
bash inicio.sh
```

### Configurar Variáveis de Ambiente

Antes de rodar os DAGs, você precisará configurar as credenciais e outras informações necessárias para o Airflow. O script `variaveis.sh` é responsável por isso. Altere as credenciais no arquivo de acordo com seu ambiente. Após isso, execute-o da seguinte forma:

```
bash variaveis.sh
```

Este script define as variáveis de ambiente no Airflow, como as credenciais AWS (chave de acesso, chave secreta, token de sessão), a região, o nome do bucket S3 e a chave KMS

### Ativando as DAGs e acessando o Airflow

Após configurar as variáveis, é hora de ativar as DAGs no Airflow:
1. **Acessar a interface do Airflow**: O Airflow estará acessível através da porta **8080** do seu navegador. Para acessá-lo, digite:

```
http://localhost:8080
```

2. **Ativar as DAGs**: Na interface do Airflow, você pode ativar as DAGs manualmente ou esperar que elas sejam executadas conforme o agendamento.


### Rodando os DAGs
Agora que o Airflow está configurado e as variáveis estão definidas, você pode rodar os DAGs. As DAGs serão executadas conforme a programação definida no Airflow, ou você pode acioná-las manualmente pela interface do Airflow.

### Finalizar o Contêiner

Depois que os DAGs tiverem sido executados ou caso queira encerrar o ambiente, execute o script fim.sh para parar o contêiner Docker:

```
bash fim.sh
```

## Contribuições

Sinta-se à vontade para fazer contribuições ou sugerir melhorias para este projeto!