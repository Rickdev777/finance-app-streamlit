import streamlit as st
from database import autenticar_usuario

st.set_page_config(page_title="Login", layout="centered")

# ====== ESTILO CUSTOMIZADO DO LOGIN ======
st.markdown("""
<style>
/* fundo da página */
[data-testid="stAppViewContainer"] {
    background: #0b0f12;
}

/* centralização do card */
.login-card {
    background: #0f1418;
    padding: 2.2rem;
    border-radius: 14px;
    width: 380px;
    margin: 80px auto;
    box-shadow: 0 8px 30px rgba(0,0,0,0.55);
    border: 1px solid rgba(255,255,255,0.05);
}

/* título */
.login-title {
    text-align: center;
    color: #e6eef8;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 6px;
}

/* subtítulo */
.login-sub {
    text-align: center;
    color: #9aa4ad;
    margin-bottom: 26px;
}

/* inputs */
input {
    background: rgba(255,255,255,0.04) !important;
    color: #e6eef8 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* botão */
.stButton > button {
    background: #29b573 !important;
    color: white !important;
    width: 100%;
    padding: 10px 0;
    font-size: 16px;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    transform: translateY(-2px);
    transition: 0.12s ease;
}

/* alinhamento */
.center {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)
# ===========================================


# ====== CARD DE LOGIN ======
st.markdown("<div class='login-card'>", unsafe_allow_html=True)

st.markdown("<div class='login-title'>Bem-vindo</div>", unsafe_allow_html=True)
st.markdown("<div class='login-sub'>Entre para acessar seu painel financeiro</div>", unsafe_allow_html=True)

username = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if autenticar_usuario(username, senha):
        st.session_state["logado"] = True
        st.session_state["usuario"] = username
        st.success("Login realizado!")
        st.rerun()
    else:
        st.error("❌ Usuário ou senha incorretos.")

st.markdown("</div>", unsafe_allow_html=True)
