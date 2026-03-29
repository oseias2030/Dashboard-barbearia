import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Black Crown Insights", layout="wide")

# 🎨 ESTILO PREMIUM
st.markdown("""
<style>
body {
    background-color: #0E0E0E;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="stMetric"] {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 14px;
    border-left: 6px solid #C8A96A;
}
h1, h2, h3 {
    color: #C8A96A;
}
</style>
""", unsafe_allow_html=True)

# 🖼️ HEADER
col1, col2 = st.columns([1,5])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050525.png", width=90)

with col2:
    st.title("Black Crown Insights")
    st.caption("Dashboard Executivo de Performance da Barbearia")

st.divider()

# 📊 DADOS
df = pd.read_csv("dados.csv")
df['data'] = pd.to_datetime(df['data'])

# 🔎 FILTROS
st.sidebar.header("Filtros")

data_inicio = st.sidebar.date_input("Data inicial", df['data'].min())
data_fim = st.sidebar.date_input("Data final", df['data'].max())

barbeiros = st.sidebar.multiselect(
    "Barbeiros",
    df['barbeiro'].unique(),
    default=df['barbeiro'].unique()
)

servicos = st.sidebar.multiselect(
    "Serviços",
    df['servico'].unique(),
    default=df['servico'].unique()
)

df = df[
    (df['data'] >= pd.to_datetime(data_inicio)) &
    (df['data'] <= pd.to_datetime(data_fim)) &
    (df['barbeiro'].isin(barbeiros)) &
    (df['servico'].isin(servicos))
]

# 📊 KPIs
faturamento = df['valor'].sum()
atendimentos = df.shape[0]
clientes = df['cliente'].nunique()
ticket = faturamento / atendimentos if atendimentos > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Faturamento", f"R$ {faturamento:,.2f}")
col2.metric("✂️ Atendimentos", atendimentos)
col3.metric("👥 Clientes", clientes)
col4.metric("📊 Ticket Médio", f"R$ {ticket:,.2f}")

st.divider()

# 🎨 CORES
cor = "#C8A96A"
bg = "#0E0E0E"

# 📈 FATURAMENTO AO LONGO DO TEMPO
st.subheader("📈 Evolução do Faturamento")

fat = df.groupby('data')['valor'].sum().reset_index()

fig1 = px.line(fat, x='data', y='valor')
fig1.update_traces(line=dict(color=cor, width=3))
fig1.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font_color="white")

st.plotly_chart(fig1, use_container_width=True)

# 🏆 RANKING BARBEIROS
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Ranking de Barbeiros")
    ranking = df.groupby('barbeiro')['valor'].sum().sort_values(ascending=False).reset_index()

    fig2 = px.bar(
        ranking,
        x='barbeiro',
        y='valor',
        color='valor',
        color_continuous_scale=["#C8A96A","#FFD700"]
    )
    fig2.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font_color="white")

    st.plotly_chart(fig2, use_container_width=True)

# 📊 SERVIÇOS
with col2:
    st.subheader("📊 Serviços Mais Vendidos")
    serv = df['servico'].value_counts().reset_index()
    serv.columns = ['servico', 'quantidade']

    fig3 = px.bar(
        serv,
        x='servico',
        y='quantidade',
        color_discrete_sequence=[cor]
    )
    fig3.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font_color="white")

    st.plotly_chart(fig3, use_container_width=True)

# 📅 FATURAMENTO MENSAL
st.subheader("📅 Faturamento Mensal")

df['mes'] = df['data'].dt.to_period('M')
mes = df.groupby('mes')['valor'].sum().reset_index()
mes['mes'] = mes['mes'].astype(str)

fig4 = px.bar(
    mes,
    x='mes',
    y='valor',
    color_discrete_sequence=[cor]
)
fig4.update_layout(plot_bgcolor=bg, paper_bgcolor=bg, font_color="white")

st.plotly_chart(fig4, use_container_width=True)
