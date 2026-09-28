-- View 1: Média de temperatura
CREATE OR REPLACE VIEW vw_avg_temp_by_device AS
SELECT 
    device_id,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature
FROM 
    iot_readings
GROUP BY 
    device_id
ORDER BY 
    avg_temperature DESC;

-- View 2: Leituras por hora
CREATE OR REPLACE VIEW vw_readings_per_hour AS
SELECT 
    EXTRACT(HOUR FROM timestamp) AS hour_of_day,
    COUNT(*) AS total_readings
FROM 
    iot_readings
GROUP BY 
    EXTRACT(HOUR FROM timestamp)
ORDER BY 
    hour_of_day ASC;

-- View 3: Máximas e mínimas por dia
CREATE OR REPLACE VIEW vw_max_min_temp_per_day AS
SELECT 
    DATE(timestamp) AS reading_date,
    MAX(temperature) AS max_temp,
    MIN(temperature) AS min_temp
FROM 
    iot_readings
GROUP BY 
    DATE(timestamp)
ORDER BY 
    reading_date DESC;