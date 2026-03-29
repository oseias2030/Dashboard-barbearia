import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Black Crown Barber", layout="wide")

# 🔐 LOGIN SIMPLES
def login():
    st.title("🔐 Black Crown Barber")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == "admin" and senha == "123":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha incorretos")

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
    st.stop()

# 🎨 ESTILO
st.markdown("""
<style>
body {
    background-color: #0E0E0E;
    color: white;
}
[data-testid="stMetric"] {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #C8A96A;
}
h1, h2, h3 {
    color: #C8A96A;
}
</style>
""", unsafe_allow_html=True)

# 🖼️ HEADER
col1, col2 = st.columns([1,4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050525.png", width=80)
with col2:
    st.title("Black Crown Barber")
    st.caption("Sistema de Gestão Inteligente")

st.divider()

# 📊 DADOS
df = pd.read_csv("dados.csv")
df['data'] = pd.to_datetime(df['data'])

# 🔎 FILTROS
st.sidebar.header("Filtros")

data_inicio = st.sidebar.date_input("Data inicial", df['data'].min())
data_fim = st.sidebar.date_input("Data final", df['data'].max())

barbeiros = st.sidebar.multiselect("Barbeiros", df['barbeiro'].unique(), default=df['barbeiro'].unique())

df = df[
    (df['data'] >= pd.to_datetime(data_inicio)) &
    (df['data'] <= pd.to_datetime(data_fim)) &
    (df['barbeiro'].isin(barbeiros))
]

# 📊 KPIs
faturamento = df['valor'].sum()
atendimentos = df.shape[0]
ticket = faturamento / atendimentos if atendimentos > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento", f"R$ {faturamento:.2f}")
col2.metric("✂️ Atendimentos", atendimentos)
col3.metric("📊 Ticket Médio", f"R$ {ticket:.2f}")

st.divider()

# 🎯 META
meta = 2000

st.subheader("🎯 Meta Mensal")
st.progress(min(faturamento/meta,1.0))
st.write(f"Meta: R$ {meta} | Atual: R$ {faturamento:.2f}")

if faturamento < meta:
    st.warning("🚨 Atenção: faturamento abaixo da meta!")
else:
    st.success("🔥 Meta batida!")

st.divider()

# 🏆 RANKING
st.subheader("🏆 Ranking de Barbeiros")

ranking = df.groupby('barbeiro')['valor'].sum().sort_values(ascending=False).reset_index()

fig_rank = px.bar(
    ranking,
    x='barbeiro',
    y='valor',
    color='valor',
    color_continuous_scale=['#C8A96A','#FFD700']
)

fig_rank.update_layout(plot_bgcolor="#0E0E0E", paper_bgcolor="#0E0E0E", font_color="white")

st.plotly_chart(fig_rank, use_container_width=True)

# 📈 FATURAMENTO
st.subheader("📈 Evolução do Faturamento")

fat_dia = df.groupby('data')['valor'].sum().reset_index()

fig = px.line(fat_dia, x='data', y='valor')
fig.update_traces(line=dict(color="#C8A96A"))
fig.update_layout(plot_bgcolor="#0E0E0E", paper_bgcolor="#0E0E0E", font_color="white")

st.plotly_chart(fig, use_container_width=True)
