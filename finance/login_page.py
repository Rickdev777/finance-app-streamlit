import streamlit as st
from database import autenticar_usuario

def mostrar_login():
    st.title("🔐 Login")

    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar_usuario(username, senha):
            st.session_state["logado"] = True
            st.session_state["usuario"] = username
            st.success("Login realizado!")
        else:
            st.error("❌ Usuário ou senha incorretos.")
