import streamlit as st
from database import criar_tabelas
from login_page import mostrar_login
from register_page import mostrar_tela_registro

# CONFIGURAÇÃO DO SISTEMA
st.set_page_config(
    page_title="Sistema Financeiro",
    page_icon="💰",
    layout="wide"
)

criar_tabelas()

# Estados iniciais
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"


def carregar_tela():

    # ==========================================================
    # TELA ANTES DO LOGIN → LOGIN / REGISTRAR NA SIDEBAR
    # ==========================================================
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

    # ==========================================================
    # TELA DEPOIS DO LOGIN → MENU PRINCIPAL NA SIDEBAR
    # ==========================================================
    else:

        st.sidebar.title(f"Bem-vindo, {st.session_state['usuario']} 👋")

        escolha = st.sidebar.radio(
            "Navegação",
            ["Dashboard", "Despesas", "Entradas", "Configurações", "Logout"]
        )

        # ------ Logout ------
        if escolha == "Logout":
            st.session_state["logado"] = False
            st.session_state["pagina"] = "login"
            st.rerun()

        # ------ Conteúdo das telas (SEM arquivos externos) ------
        st.title(escolha)

        if escolha == "Dashboard":
            st.write("📊 Aqui virá o Dashboard.")

        elif escolha == "Despesas":
            st.write("💸 Tela de despesas.")

        elif escolha == "Entradas":
            st.write("💰 Tela de entradas.")

        elif escolha == "Configurações":
            st.write("⚙️ Configurações do usuário.")


carregar_tela()
