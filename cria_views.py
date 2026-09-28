from sqlalchemy import create_engine, text

# Conectando na porta 5433 que criamos no Docker
db_url = 'postgresql://admin:admin@localhost:5433/iot_db'
engine = create_engine(db_url)

# Script SQL para criar as 3 views
sql_queries = """
CREATE OR REPLACE VIEW vw_avg_temp_by_device AS
SELECT device_id, ROUND(AVG(temperature)::numeric, 2) AS avg_temperature
FROM iot_readings GROUP BY device_id ORDER BY avg_temperature DESC;

CREATE OR REPLACE VIEW vw_readings_per_hour AS
SELECT EXTRACT(HOUR FROM timestamp) AS hour_of_day, COUNT(*) AS total_readings
FROM iot_readings GROUP BY EXTRACT(HOUR FROM timestamp) ORDER BY hour_of_day ASC;

CREATE OR REPLACE VIEW vw_max_min_temp_per_day AS
SELECT DATE(timestamp) AS reading_date, MAX(temperature) AS max_temp, MIN(temperature) AS min_temp
FROM iot_readings GROUP BY DATE(timestamp) ORDER BY reading_date DESC;
"""

print("Criando as views no banco de dados...")
with engine.connect() as conn:
    # Executa o bloco de SQL e commita as alterações
    conn.execute(text(sql_queries))
    conn.commit()

print("Views criadas com sucesso!")