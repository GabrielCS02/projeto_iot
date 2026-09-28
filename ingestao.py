import pandas as pd
from sqlalchemy import create_engine

# 1. Configuração da conexão com o PostgreSQL local
db_url = 'postgresql://admin:admin@localhost:5432/iot_db'
engine = create_engine(db_url)

# 2. Leitura do arquivo CSV
csv_file_path = 'temperature_readings.csv'
print(f"Lendo os dados de {csv_file_path}...")
df = pd.read_csv(csv_file_path)

# O dataset original do Kaggle (IOT-temp.csv) pode ter nomes de colunas diferentes
# do que as views SQL esperam. Vamos padronizar:
# Verifique o CSV, mas geralmente as colunas precisam ser ajustadas assim:
df = df.rename(columns={'noted_date': 'timestamp', 'room_id/id': 'device_id', 'temp': 'temperature'})

# Garante que timestamp é data/hora
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M', errors='coerce')


# 3. Inserção dos dados no PostgreSQL
table_name = 'iot_readings'
print(f"Inserindo dados na tabela '{table_name}'...")

# if_exists='replace' recria a tabela
df.to_sql(table_name, engine, if_exists='replace', index=False)

print("Processamento concluído com sucesso!")