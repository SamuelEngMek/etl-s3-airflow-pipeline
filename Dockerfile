# Usar a imagem oficial do Apache Airflow como base
FROM apache/airflow:2.10.4

# Copiar seu arquivo requirements.txt para dentro da imagem
COPY requirements.txt /requirements.txt

# Instalar as dependências do requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copiar qualquer outro arquivo ou configuração adicional, se necessário
COPY ./config /opt/airflow/config