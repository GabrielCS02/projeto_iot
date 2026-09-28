import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 1. Configuração da Página (Expandida e com Ícone)
st.set_page_config(page_title="IoT Dashboard", page_icon="📡", layout="wide")

DB_URL = 'postgresql://admin:admin@localhost:5433/iot_db'

@st.cache_data(ttl=300) # Cache expira automaticamente a cada 5 minutos
def load_data(query):
    """Conecta ao banco na porta 5433 e carrega os dados com cache."""
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# 2. Barra Lateral (Sidebar) para Controles
st.sidebar.title("⚙️ Configurações")
st.sidebar.markdown("Utilize os controles abaixo para interagir com o painel.")
if st.sidebar.button("🔄 Atualizar Dados Agora"):
    st.cache_data.clear()
    st.sidebar.success("Cache limpo! Dados atualizados.")

st.title("Dashboard de Monitoramento IoT 📡")
st.markdown("Visão consolidada das métricas de sensores, tráfego de rede e amplitude térmica.")
st.markdown("---")

# 3. Carregamento Seguro dos Dados
df_avg_temp = load_data("SELECT * FROM vw_avg_temp_by_device;")
df_readings_hour = load_data("SELECT * FROM vw_readings_per_hour;")
df_max_min = load_data("SELECT * FROM vw_max_min_temp_per_day;")

# 4. Cartões de Indicadores (KPIs)
if not df_max_min.empty and not df_readings_hour.empty:
    col1, col2, col3 = st.columns(3)
    max_absoluta = df_max_min['max_temp'].max()
    min_absoluta = df_max_min['min_temp'].min()
    total_leituras = df_readings_hour['total_readings'].sum()
    
    col1.metric("🔥 Maior Temperatura Registrada", f"{max_absoluta} °C")
    col2.metric("❄️ Menor Temperatura Registrada", f"{min_absoluta} °C")
    col3.metric("📊 Total de Leituras Processadas", f"{total_leituras:,}".replace(",", "."))
    st.markdown("---")

# 5. Gráfico Principal (Largura Total)
st.subheader("Média de Temperatura por Dispositivo")
if not df_avg_temp.empty:
    fig_avg = px.bar(
        df_avg_temp, 
        x='device_id', 
        y='avg_temperature',
        labels={'device_id': 'Dispositivo', 'avg_temperature': 'Temp. Média (°C)'},
        color='avg_temperature',
        color_continuous_scale='RdBu_r' # Escala de cores (Azul para frio, Vermelho para quente)
    )
    fig_avg.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_avg, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True) # Espaçamento

# 6. Gráficos Secundários (Lado a Lado)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Frequência de Leituras por Hora")
    if not df_readings_hour.empty:
        fig_hour = px.bar(
            df_readings_hour, 
            x='hour_of_day', 
            y='total_readings',
            labels={'hour_of_day': 'Hora do Dia', 'total_readings': 'Volume de Leituras'},
            color_discrete_sequence=['#4C78A8']
        )
        fig_hour.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1), margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_hour, use_container_width=True)

with col_right:
    st.subheader("Amplitude Térmica Diária")
    if not df_max_min.empty:
        df_max_min_melted = df_max_min.melt(
            id_vars=['reading_date'], value_vars=['max_temp', 'min_temp'], 
            var_name='Métrica', value_name='Temperatura'
        )
        # Renomeando as legendas
        df_max_min_melted['Métrica'] = df_max_min_melted['Métrica'].map({'max_temp': 'Máxima', 'min_temp': 'Mínima'})
        
        fig_max_min = px.line(
            df_max_min_melted, 
            x='reading_date', 
            y='Temperatura',
            color='Métrica',
            labels={'reading_date': 'Data', 'Temperatura': 'Temperatura (°C)'},
            color_discrete_map={'Máxima': '#E45756', 'Mínima': '#54A24B'}
        )
        fig_max_min.update_traces(mode='lines+markers')
        fig_max_min.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_max_min, use_container_width=True)