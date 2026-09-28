import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Configuração da página do Streamlit
st.set_page_config(page_title="IoT Dashboard", layout="wide")

# 1. Conexão com o Banco de Dados
# Utiliza as credenciais definidas no contêiner Docker: user=admin, pass=admin, db=iot_db na porta 5432
DB_URL = 'postgresql://admin:admin@localhost:5432/iot_db?client_encoding=utf8'

@st.cache_data
def load_data(query):
    """Função para conectar no banco e carregar os dados das views, utilizando cache para performance."""
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

st.title("Dashboard de Monitoramento IoT")
st.markdown("Visualização de métricas de sensores, volume de tráfego e amplitude térmica diária.")

# 2. Carregamento dos dados das 3 views analíticas
# Carregando Média de temperatura por dispositivo
df_avg_temp = load_data("SELECT * FROM vw_avg_temp_by_device;")

# Carregando Leituras por hora
df_readings_hour = load_data("SELECT * FROM vw_readings_per_hour;")

# Carregando Temperaturas máximas e mínimas por dia
df_max_min = load_data("SELECT * FROM vw_max_min_temp_per_day;")

# 3. Geração dos Gráficos Interativos (Barras e Linhas)
st.header("1. Média de Temperatura por Dispositivo")
st.markdown("Identifica rapidamente sensores registrando valores anômalos de forma consistente.")
if not df_avg_temp.empty:
    fig_avg = px.bar(
        df_avg_temp, 
        x='device_id', 
        y='avg_temperature',
        title="Temperatura Média (°C) por ID do Dispositivo",
        labels={'device_id': 'ID do Dispositivo', 'avg_temperature': 'Temperatura Média'},
        color='avg_temperature',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_avg, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado para a média de dispositivos.")

st.header("2. Frequência de Leituras por Hora")
st.markdown("Analisa o volume de tráfego de dados e entende os horários de pico de atividade dos sensores.")
if not df_readings_hour.empty:
    fig_hour = px.bar(
        df_readings_hour, 
        x='hour_of_day', 
        y='total_readings',
        title="Total de Leituras Registradas por Hora do Dia",
        labels={'hour_of_day': 'Hora do Dia', 'total_readings': 'Total de Leituras'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_hour.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig_hour, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado para leituras por hora.")

st.header("3. Temperaturas Máximas e Mínimas por Dia")
st.markdown("Monitora a amplitude térmica diária e os picos absolutos capturados ao longo do tempo.")
if not df_max_min.empty:
    # Transformar a estrutura para facilitar a plotagem de duas linhas no Plotly Express
    df_max_min_melted = df_max_min.melt(
        id_vars=['reading_date'], 
        value_vars=['max_temp', 'min_temp'], 
        var_name='Tipo de Medição', 
        value_name='Temperatura'
    )
    
    fig_max_min = px.line(
        df_max_min_melted, 
        x='reading_date', 
        y='Temperatura',
        color='Tipo de Medição',
        title="Amplitude Térmica Diária (Máximas e Mínimas)",
        labels={'reading_date': 'Data de Leitura', 'Temperatura': 'Temperatura (°C)'},
        color_discrete_map={'max_temp': 'red', 'min_temp': 'blue'}
    )
    fig_max_min.update_traces(mode='lines+markers')
    st.plotly_chart(fig_max_min, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado para as máximas e mínimas diárias.")