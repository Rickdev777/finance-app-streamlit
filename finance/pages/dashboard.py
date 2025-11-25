import streamlit as st
from database import listar_despesas, listar_entradas
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard", layout="wide")

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.switch_page("app.py")

user = st.session_state["usuario"]
st.title(f"📊 Dashboard – {user}")

# Carregar dados
df_desp = pd.DataFrame(listar_despesas(user), columns=["ID", "Descrição", "Valor", "Categoria", "Data"])
df_ent = pd.DataFrame(listar_entradas(user), columns=["ID", "Descrição", "Valor", "Categoria", "Data"])

total_desp = df_desp["Valor"].sum() if not df_desp.empty else 0
total_ent = df_ent["Valor"].sum() if not df_ent.empty else 0
saldo = total_ent - total_desp

# Cards em coluna
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'><h3>Despesas</h3><h1 style='color:#d9534f'>R$ {total_desp:,.2f}</h1></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><h3>Entradas</h3><h1 style='color:#5cb85c'>R$ {total_ent:,.2f}</h1></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><h3>Saldo Atual</h3><h1 style='color:#0275d8'>R$ {saldo:,.2f}</h1></div>", unsafe_allow_html=True)

# Gráficos com espaçamento
st.markdown("### Gráficos Gerais")
colg1, colg2 = st.columns(2)

with colg1:
    if not df_desp.empty:
        fig = px.pie(df_desp, values="Valor", names="Categoria", title="Despesas por Categoria")
        st.plotly_chart(fig, use_container_width=True)

with colg2:
    if not df_ent.empty:
        fig = px.pie(df_ent, values="Valor", names="Categoria", title="Entradas por Categoria")
        st.plotly_chart(fig, use_container_width=True)

