import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Barbearia PRO", layout="wide")

st.title("💈 Dashboard Profissional - Barbearia")

# Carregar dados
df = pd.read_csv("dados.csv")
df['data'] = pd.to_datetime(df['data'])

# 🔎 FILTROS
st.sidebar.header("Filtros")

data_inicio = st.sidebar.date_input("Data inicial", df['data'].min())
data_fim = st.sidebar.date_input("Data final", df['data'].max())

barbeiros = st.sidebar.multiselect("Barbeiros", df['barbeiro'].unique(), default=df['barbeiro'].unique())
servicos = st.sidebar.multiselect("Serviços", df['servico'].unique(), default=df['servico'].unique())

# Aplicar filtros
df_filtrado = df[
    (df['data'] >= pd.to_datetime(data_inicio)) &
    (df['data'] <= pd.to_datetime(data_fim)) &
    (df['barbeiro'].isin(barbeiros)) &
    (df['servico'].isin(servicos))
]

# 📊 KPIs
faturamento = df_filtrado['valor'].sum()
atendimentos = df_filtrado.shape[0]
clientes = df_filtrado['cliente'].nunique()
ticket_medio = faturamento / atendimentos if atendimentos > 0 else 0

# Crescimento (comparação simples)
df_filtrado['mes'] = df_filtrado['data'].dt.to_period('M')
faturamento_mes = df_filtrado.groupby('mes')['valor'].sum().reset_index()

crescimento = 0
if len(faturamento_mes) > 1:
    crescimento = ((faturamento_mes['valor'].iloc[-1] - faturamento_mes['valor'].iloc[-2]) /
                   faturamento_mes['valor'].iloc[-2]) * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Faturamento", f"R$ {faturamento:.2f}")
col2.metric("✂️ Atendimentos", atendimentos)
col3.metric("👥 Clientes", clientes)
col4.metric("📊 Ticket Médio", f"R$ {ticket_medio:.2f}")
col5.metric("📈 Crescimento", f"{crescimento:.1f}%")

st.divider()

# 📈 Gráfico faturamento por dia
faturamento_dia = df_filtrado.groupby('data')['valor'].sum().reset_index()
fig1 = px.line(faturamento_dia, x='data', y='valor', title='Faturamento por Dia')
st.plotly_chart(fig1, use_container_width=True)

# 📊 Serviços mais vendidos
servicos_df = df_filtrado['servico'].value_counts().reset_index()
servicos_df.columns = ['servico', 'quantidade']
fig2 = px.bar(servicos_df, x='servico', y='quantidade', title='Serviços Mais Vendidos')
st.plotly_chart(fig2, use_container_width=True)

# 🧑‍🔧 Faturamento por barbeiro
barbeiro_df = df_filtrado.groupby('barbeiro')['valor'].sum().reset_index()
fig3 = px.pie(barbeiro_df, names='barbeiro', values='valor', title='Faturamento por Barbeiro')
st.plotly_chart(fig3, use_container_width=True)

# 📅 Faturamento mensal
faturamento_mes['mes'] = faturamento_mes['mes'].astype(str)
fig4 = px.bar(faturamento_mes, x='mes', y='valor', title='Faturamento Mensal')
st.plotly_chart(fig4, use_container_width=True)
