import streamlit as st
from database import registrar_usuario

def mostrar_tela_registro():
    st.set_page_config(page_title="Criar Conta", layout="centered")

    # CSS compatível com modo claro e escuro
    st.markdown("""
        <style>

        /* Centralizar tudo */
        .main {
            display: flex;
            justify-content: center;
            padding-top: 4vh;
        }

        /* Card moderno */
        .register-wrapper {
            width: 100%;
            max-width: 420px;
            background: var(--background-color);
            padding: 2.2rem 2rem;
            border-radius: 16px;
            box-shadow: 0 6px 22px rgba(0,0,0,0.25);
            backdrop-filter: blur(6px);
        }

        /* Suporte a modo claro/escuro do Streamlit */
        :root {
            --background-color: rgba(255, 255, 255, 0.12);
            --text-color: #e8e8e8;
            --input-bg: rgba(255,255,255,0.08);
            --button-primary: #4CAF50;
            --button-secondary: #3b3d42;
        }

        [data-theme="light"] {
            --background-color: #ffffff;
            --text-color: #333;
            --input-bg: #f1f1f1;
            --button-secondary: #e5e7eb;
        }

        .register-title {
            color: var(--text-color);
            text-align: center;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .register-sub {
            text-align: center;
            color: var(--text-color);
            opacity: 0.8;
            margin-bottom: 1.8rem;
        }

        /* Inputs */
        .stTextInput>div>div>input {
            background: var(--input-bg) !important;
            color: var(--text-color) !important;
            border-radius: 10px !important;
            height: 45px;
        }

        /* Botões */
        .stButton>button {
            width: 100%;
            height: 45px;
            border-radius: 10px;
            font-size: 1rem;
            border: none;
        }

        /* Criar Conta */
        .create-btn button {
            background: var(--button-primary) !important;
            color: white !important;
        }

        /* Voltar */
        .back-btn button {
            background: var(--button-secondary) !important;
            color: var(--text-color) !important;
        }

        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='register-wrapper'>", unsafe_allow_html=True)

    st.markdown("<div class='register-title'>Criar nova conta</div>", unsafe_allow_html=True)
    st.markdown("<div class='register-sub'>Preencha seus dados abaixo.</div>", unsafe_allow_html=True)

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    st.markdown("<br>", unsafe_allow_html=True)

    # Botão criar conta
    create = st.container()
    with create:
        if st.button("Criar Conta", use_container_width=True):
            if not usuario or not senha:
                st.warning("Preencha todos os campos.")
            else:
                ok = registrar_usuario(usuario, senha)
                if ok:
                    st.success("Conta criada com sucesso!")
                    st.info("Voltando ao login...")

                    # ← CORRETO
                    st.session_state["pagina"] = "login"
                    st.rerun()


    st.markdown("<br>", unsafe_allow_html=True)

    # Botão voltar
    back = st.container()
    with back:
        if st.button("Voltar", use_container_width=True):
            try:
                st.switch_page("app.py")
            except:
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar_tela_registro()
