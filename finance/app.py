import streamlit as st
from database import criar_tabelas
from login_page import mostrar_login
from register_page import mostrar_tela_registro

st.set_page_config(
    page_title="Sistema Financeiro",
    page_icon="💰",
    layout="wide"
)

criar_tabelas()

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"   # login é a página inicial


def carregar_tela():
    if not st.session_state["logado"]:
        menu = st.sidebar.radio(
            "Menu",
            ["Login", "Registrar"],
            index=0 if st.session_state["pagina"] == "login" else 1
        )

        if menu == "Login":
            st.session_state["pagina"] = "login"
            mostrar_login()
        else:
            st.session_state["pagina"] = "registro"
            mostrar_tela_registro()

    else:
        st.sidebar.title(f"Bem-vindo, {st.session_state['usuario']} 👋")

        escolha = st.sidebar.radio(
            "Navegação",
            [
                "Dashboard",
                "Despesas",
                "Entradas",
                "Configurações",
                "Logout"
            ]
        )

        if escolha == "Logout":
            st.session_state["logado"] = False
            st.session_state["pagina"] = "login"
            st.rerun()

        
carregar_tela()