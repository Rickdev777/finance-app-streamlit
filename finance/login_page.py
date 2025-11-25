import streamlit as st
from database import autenticar_usuario

def mostrar_login():
    st.set_page_config(
        page_title="Login — Sistema Financeiro", 
        layout="centered", 
        page_icon="💠"
    )

    # ===== CSS ==========================================================
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
        overflow: hidden;
        backdrop-filter: blur(6px);
    }

    .hero {
        display:flex; flex-direction:column;
        gap: 12px; align-items:center;
    }
    .logo {
        width:96px; height:96px; border-radius:20px;
        background: linear-gradient(135deg, rgba(41,181,115,0.15), rgba(51,160,255,0.08));
        display:flex; align-items:center; justify-content:center;
        font-size:40px;
    }
    .hero h2 { color:#e6eef8; margin:0; font-size:22px; }
    .hero p { color:var(--muted); font-size:14px; max-width:320px; text-align:center; }

    .form-area {}
    .form-title { font-size:20px; color:#e6eef8; margin-bottom:6px; font-weight:700; }
    .form-sub { color:var(--muted); font-size:13px; margin-bottom:18px; }

    [data-testid="stTextInput"] input {
        background:var(--glass) !important;
        color:#e6eef8 !important;
        border-radius:10px !important;
        height:var(--input-h) !important;
        padding:10px 14px !important;
        border:1px solid rgba(255,255,255,0.04) !important;
    }

    .stButton>button {
        border-radius:10px !important;
        padding:12px 16px !important;
        font-weight:700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== LAYOUT HTML ==================================================
    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    # LEFT SIDE
    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    st.markdown("<div class='logo'>💠</div>", unsafe_allow_html=True)
    st.markdown("<h2>Finance Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p>Controle suas finanças com clareza — comece fazendo login.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT SIDE — FORM
    st.markdown("<div class='form-area'>", unsafe_allow_html=True)
    st.markdown("<div class='form-title'>Bem-vindo de volta</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-sub'>Entre para acessar seu painel financeiro</div>", unsafe_allow_html=True)

    # ===== FORM (somente inputs + form_submit_button) ===================
    with st.form(key="login_form"):
        user = st.text_input("Usuário", placeholder="seu.usuario")
        pwd = st.text_input("Senha", type="password", placeholder="••••••••")

        submitted = st.form_submit_button("Entrar")

    # ===== BOTÕES FORA DO FORM ==========================================
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Criar conta"):
                st.session_state["pagina"] = "registro"
                st.rerun()

    with col2:
        if st.button("Esqueci a senha"):
            st.info("Função ainda não implementada.")

    # ===== LOGIN (executado após submit) ================================
    if submitted:
        if not user or not pwd:
            st.warning("Preencha usuário e senha.")
        else:
            if autenticar_usuario(user, pwd):
                st.success("Login realizado! Redirecionando...")
                st.session_state["logado"] = True
                st.session_state["usuario"] = user
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    # ===== FECHAR DIVS HTML ============================================
    st.markdown("</div>", unsafe_allow_html=True)  # close form-area
    st.markdown("</div>", unsafe_allow_html=True)  # close login-card
    st.markdown("</div>", unsafe_allow_html=True)  # close wrap

if __name__ == "__main__":
    mostrar_login()
