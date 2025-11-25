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


# ==========================================================
# SISTEMA DE NAVEGAÇÃO
# ==========================================================
def carregar_tela():

    # ===================== PÁGINAS SEM LOGIN =====================
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

        return  # evita renderizar o resto antes do login

    # ===================== PÁGINAS DEPOIS DO LOGIN =====================
    st.sidebar.title(f"Bem-vindo, {st.session_state['usuario']} 👋")

 

if st.session_state["pagina"] == "registro" and not st.session_state["logado"]:
    mostrar_tela_registro()
else:
    carregar_tela()
