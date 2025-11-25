import streamlit as st
from database import registrar_usuario

def mostrar_tela_registro():
    st.set_page_config(page_title="Criar Conta", layout="centered")

    # CSS customizado elegante
    st.markdown("""
        <style>
        body {
            background: #f0f2f6;
        }
        .register-card {
            background: white;
            padding: 2rem 2.5rem;
            border-radius: 14px;
            max-width: 480px;
            margin: auto;
            margin-top: 60px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.10);
        }
        .register-title {
            font-size: 28px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.3rem;
            color: #333;
        }
        .register-sub {
            text-align: center;
            margin-bottom: 2rem;
            color: #666;
        }
        .stButton > button {
            background: #4CAF50 !important;
            color: white !important;
            padding: 0.7rem 1.4rem;
            width: 100%;
            font-size: 1rem;
            border-radius: 10px;
            border: none;
        }
        .back-btn > button {
            background: #e2e5ea !important;
            color: #333 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='register-card'>", unsafe_allow_html=True)

        st.markdown("<div class='register-title'>Criar nova conta</div>", unsafe_allow_html=True)
        st.markdown("<div class='register-sub'>Preencha seus dados abaixo.</div>", unsafe_allow_html=True)

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        st.markdown("")

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

        if st.button("Voltar", key="back", help="Retornar ao login", use_container_width=True):
            try:
                st.switch_page("app.py")
            except:
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar_tela_registro()
