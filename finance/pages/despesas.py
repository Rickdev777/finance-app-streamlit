import streamlit as st
import pandas as pd
from database import listar_despesas, adicionar_despesa, editar_despesa, excluir_despesa

st.set_page_config(page_title="Despesas", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.switch_page("app.py")

user = st.session_state["usuario"]
st.title("💸 Despesas")

df = pd.DataFrame(listar_despesas(user), columns=["ID", "Descrição", "Valor", "Categoria", "Data"])

st.markdown("## ➕ Nova Despesa")
col1, col2 = st.columns(2)

with col1:
    desc = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")

with col2:
    cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Boletos", "Outros"])
    data = st.date_input("Data")

if st.button("Adicionar"):
    adicionar_despesa(user, desc, valor, cat, str(data))
    st.success("Despesa adicionada!")
    st.rerun()

st.markdown("## 📋 Minhas Despesas")
st.dataframe(df, use_container_width=True, height=400)

