# login_page.py
import os
import streamlit as st
from database import autenticar_usuario

def mostrar_login():
    # Página configurada para ficar centralizada
    st.set_page_config(page_title="Login — Sistema Financeiro", layout="centered", page_icon="💠")

    # ===== stylish CSS (dark-first, self-contained for this page) =====
    st.markdown("""
    <style>
    :root{
        --bg: #07090b;
        --card: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        --muted: #9aa4ad;
        --accent: #29b573;
        --glass: rgba(255,255,255,0.02);
        --input-h: 48px;
        --radius: 14px;
    }

    [data-testid="stAppViewContainer"] { background: var(--bg) !important; }

    /* center container */
    .login-wrap {
        width:100%;
        max-width:980px;
        margin: 24px auto 60px;
        display:flex;
        align-items:center;
        justify-content:center;
    }

    .login-card {
        width: 820px;
        display: grid;
        grid-template-columns: 420px 1fr;
        gap: 28px;
        padding: 28px;
        border-radius: var(--radius);
        background: var(--card);
        box-shadow: 0 12px 40px rgba(0,0,0,0.65);
        border: 1px solid rgba(255,255,255,0.02);
        align-items: center;
        overflow: hidden;
        backdrop-filter: blur(6px);
    }

    /* left: brand/hero */
    .hero {
        padding: 6px 10px;
        display:flex;
        flex-direction:column;
        gap: 12px;
        align-items: center;
    }
    .logo {
        width:96px;
        height:96px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(41,181,115,0.15), rgba(51,160,255,0.08));
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:40px;
        box-shadow: 0 8px 30px rgba(2,6,9,0.6) inset;
    }
    .hero h2 {
        margin: 0;
        color: #e6eef8;
        font-size: 22px;
        text-align: center;
    }
    .hero p {
        margin: 0;
        color: var(--muted);
        text-align: center;
        font-size: 14px;
        line-height: 1.4;
        max-width: 320px;
    }

    /* form area */
    .form-area {
        padding: 6px 4px;
    }
    .form-title {
        font-size: 20px;
        color: #e6eef8;
        margin-bottom: 6px;
        font-weight: 700;
    }
    .form-sub {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* style the streamlit inputs via data-testid */
    [data-testid="stTextInput"] input,
    [data-testid="stTextInput"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stTextArea"] textarea {
        background: var(--glass) !important;
        color: #e6eef8 !important;
        border-radius: 10px !important;
        height: var(--input-h) !important;
        padding: 10px 14px !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
    }

    /* small input label color */
    label[for] { color: var(--muted) !important; }

    /* buttons */
    .stButton>button {
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        border: none !important;
    }
    .btn-primary {
        background: linear-gradient(90deg,var(--accent), #1fb563) !important;
        color: #ffffff !important;
    }
    .btn-ghost {
        background: transparent !important;
        color: var(--muted) !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
    }

    /* small row actions */
    .row-actions { display:flex; gap:10px; margin-top:12px; align-items:center; }

    /* responsiveness */
    @media (max-width: 880px) {
        .login-card { grid-template-columns: 1fr; width: 92%; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== layout =====
    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    # left hero
    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    st.markdown("<div class='logo'>💠</div>", unsafe_allow_html=True)
    st.markdown("<h2>Finance Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p>Controle suas finanças com clareza. Rápido, seguro e elegante — comece fazendo login.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # right = form
    st.markdown("<div class='form-area'>", unsafe_allow_html=True)
    st.markdown("<div class='form-title'>Bem-vindo de volta</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-sub'>Entre para acessar seu painel financeiro</div>", unsafe_allow_html=True)

    # use form to avoid duplicate widget issues
    with st.form(key="login_form"):
        user = st.text_input("Usuário", placeholder="seu.usuario")
        pwd = st.text_input("Senha", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Entrar", help="Entrar no sistema")

        # small extra actions
        cols = st.columns([1,1])
        with cols[0]:
            if st.button("Criar conta"):
                try:
                    st.switch_page("pages/registro.py")
                except Exception:
                    pass
        with cols[1]:
            if st.button("Esqueci a senha"):
                st.info("Funcionalidade de recuperação em breve.")

    # handle submit
    if submitted:
        if not user or not pwd:
            st.warning("Preencha usuário e senha.")
        else:
            if autenticar_usuario(user, pwd):
                st.success("Login realizado — redirecionando...")
                st.session_state["logado"] = True
                st.session_state["usuario"] = user
                st.experimental_rerun()  # redirect
            else:
                st.error("Usuário ou senha incorretos.")

    st.markdown("</div>", unsafe_allow_html=True)  # close form-area
    st.markdown("</div>", unsafe_allow_html=True)  # close login-card
    st.markdown("</div>", unsafe_allow_html=True)  # close wrap

# allow direct run for testing
if __name__ == "__main__":
    mostrar_login()
