# pages/registro.py  (ou register_page.py)
import streamlit as st
from database import registrar_usuario

def mostrar_tela_registro():
    st.set_page_config(page_title="Criar Conta", layout="wide")

    # Carregar CSS (opcional)
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.title("📝 Criar nova conta")
    st.markdown("Preencha os campos abaixo para criar seu usuário.")

    col1, col2 = st.columns([1, 1])

    with col1:
        usuario = st.text_input("Usuário", key="reg_usuario")
    with col2:
        senha = st.text_input("Senha", type="password", key="reg_senha")

    st.markdown("")

    if st.button("Registrar Conta", use_container_width=True, key="reg_btn"):
        if not usuario or not senha:
            st.warning("Preencha usuário e senha.")
        else:
            ok = registrar_usuario(usuario, senha)
            if ok:
                st.success("Conta criada com sucesso! Faça login.")
                st.info("Voltando para tela de login...")
                # redireciona para app.py (se o seu fluxo usa st.switch_page)
                try:
                    st.switch_page("app.py")
                except Exception:
                    # fallback: apenas recarrega a página atual
                    st.experimental_rerun()
            else:
                st.error("Erro: Usuário já existe ou outro problema ocorreu.")

    if st.button("Voltar", use_container_width=True, key="reg_voltar"):
        try:
            st.switch_page("app.py")
        except Exception:
            st.experimental_rerun()


# Permite executar a página diretamente (opcional)
if __name__ == "__main__":
    mostrar_tela_registro()
