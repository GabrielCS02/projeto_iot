import pandas as pd
from sqlalchemy import create_engine

# 1. Configuração da conexão com o PostgreSQL local via SQLAlchemy
db_url = 'postgresql://admin:admin@localhost:5432/iot_db'
engine = create_engine(db_url)

# 2. Leitura do arquivo CSV baixado do Kaggle
# Certifique-se de que o arquivo 'temperature_readings.csv' está na mesma pasta
csv_file_path = 'temperature_readings.csv'
print(f"Lendo os dados de {csv_file_path}...")
df = pd.read_csv(csv_file_path)

# 3. Inserção dos dados no PostgreSQL
table_name = 'iot_readings'
print(f"Inserindo dados na tabela '{table_name}'...")

# if_exists='replace' recria a tabela se ela já existir
df.to_sql(table_name, engine, if_exists='replace', index=False)

print("Processamento concluído com sucesso!")