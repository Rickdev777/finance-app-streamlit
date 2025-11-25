import streamlit as st
from database import autenticar_usuario
import os

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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
