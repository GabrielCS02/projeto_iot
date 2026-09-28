# 📡 Pipeline de Dados IoT e Big Data

Este repositório contém um projeto acadêmico focado na arquitetura e no processamento de dados massivos gerados por dispositivos IoT[cite: 3, 5]. O objetivo principal é demonstrar a ingestão, armazenamento e visualização de métricas de sensores térmicos através de um pipeline de dados completo.

## 🛠️ Tecnologias Utilizadas
* **Infraestrutura:** Docker e PostgreSQL.
* **Engenharia de Dados:** Python, Pandas e SQLAlchemy.
* **Visualização:** Streamlit e Plotly Express[cite: 3].
* **Versionamento:** Git e GitHub[cite: 3].

## 📂 Estrutura do Projeto
* `ingestao.py`: Script responsável por ler o arquivo CSV, tratar os dados e realizar a inserção no banco de dados PostgreSQL.
* `dashboard.py`: Aplicação web interativa que consome as views analíticas do banco e plota gráficos[cite: 1, 2].
* `temperature_readings.csv`: Dataset original extraído do Kaggle (ignorado no versionamento pelo `.gitignore`).

## 🚀 Como Executar o Projeto

**1. Subir a Infraestrutura (Banco de Dados)**
O banco de dados roda isoladamente em um contêiner Docker na porta 5433 para evitar conflitos com serviços locais[cite: 1, 2]. Execute no terminal:
```bash
docker run --name postgres-iot -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=iot_db -p 5433:5432 -d postgres