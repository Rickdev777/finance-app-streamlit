import streamlit as st
from database import registrar_usuario

def mostrar_tela_registro():
    st.set_page_config(page_title="Criar Conta", layout="centered")

    st.markdown("""
        <style>
        /* Centraliza tudo na vertical e horizontal */
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 40px;
        }

        /* Cartão */
        .register-card {
            background: var(--card-bg);
            padding: 2.5rem;
            border-radius: 14px;
            width: 420px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        }

        /* Cores adaptáveis ao modo escuro */
        :root {
            --card-bg: #ffffff;
            --text-color: #333333;
            --subtext-color: #666666;
        }
        html[data-theme="dark"] {
            --card-bg: #1f1f1f;
            --text-color: #f2f2f2;
            --subtext-color: #bbbbbb;
        }

        .register-title {
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.3rem;
            color: var(--text-color);
        }

        .register-sub {
            text-align: center;
            margin-bottom: 2rem;
            color: var(--subtext-color);
        }

        /* Botões */
        .stButton > button {
            background: #4CAF50 !important;
            color: white !important;
            padding: 0.7rem;
            width: 100%;
            border-radius: 10px;
            font-size: 1rem;
            border: none;
        }
        .back-btn > button {
            background: #e2e5ea !important;
            color: #333 !important;
        }

        /* Ajuste para tema escuro no botão voltar */
        html[data-theme="dark"] .back-btn > button {
            background: #444 !important;
            color: #eee !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # container principal
    st.markdown("<div class='register-card'>", unsafe_allow_html=True)

    st.markdown("<div class='register-title'>Criar nova conta</div>", unsafe_allow_html=True)
    st.markdown("<div class='register-sub'>Preencha seus dados abaixo.</div>", unsafe_allow_html=True)

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Criar Conta"):
        if not usuario or not senha:
            st.warning("Preencha todos os campos.")
        else:
            ok = registrar_usuario(usuario, senha)
            if ok:
                st.success("Conta criada com sucesso!")
                st.info("Voltando ao login...")
                try:
                    st.switch_page("app.py")
                except:
                    st.rerun()
            else:
                st.error("Erro! Usuário já existe.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Voltar", key="back"):
        try:
            st.switch_page("app.py")
        except:
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar_tela_registro()
