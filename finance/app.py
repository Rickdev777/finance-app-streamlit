import streamlit as st
from database import criar_tabelas, conectar
from register_page import mostrar_tela_registro

from pages.dashboard import mostrar_dashboard
from pages.despesas import mostrar_despesas
from pages.entradas import mostrar_entradas
from pages.configuracoes import mostrar_config

st.set_page_config(
    page_title="Sistema Financeiro",
    page_icon="💰",
    layout="wide"
)

criar_tabelas()

# Inicializa estados
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"   # login é a página inicial

if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# ===== CSS GLOBAL / ESTILO DO LOGIN ==================================
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

/* background da app */
[data-testid="stAppViewContainer"] { background: var(--bg) !important; }

/* container do login */
.login-wrap {
    width:100%;
    max-width:980px;
    margin: 24px auto 60px;
    display:flex;
    align-items:center;
    justify-content:center;
}

/* card principal */
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

/* hero / left */
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

/* form area */
.form-area {}
.form-title { font-size:20px; color:#e6eef8; margin-bottom:6px; font-weight:700; }
.form-sub { color:var(--muted); font-size:13px; margin-bottom:18px; }

/* inputs estilizados */
[data-testid="stTextInput"] input {
    background:var(--glass) !important;
    color:#e6eef8 !important;
    border-radius:10px !important;
    height:var(--input-h) !important;
    padding:10px 14px !important;
    border:1px solid rgba(255,255,255,0.04) !important;
}

/* botões */
.stButton>button {
    border-radius:10px !important;
    padding:12px 16px !important;
    font-weight:700 !important;
}

/* sidebar tweaks */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
    border-right: 1px solid rgba(255,255,255,0.02);
}
[data-testid="stSidebar"] .css-1d391kg { color: #e6eef8; } /* títulos no sidebar (pode variar por versão do streamlit) */
</style>
""", unsafe_allow_html=True)

# ===== FUNÇÃO DE RENDERIZAÇÃO DO LOGIN (ESTILIZADA) ===================
def mostrar_login_estilizado():
    # LAYOUT HTML / ESTRUTURA
    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    # LEFT — HERO
    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    st.markdown("<div class='logo'>💠</div>", unsafe_allow_html=True)
    st.markdown("<h2>Finance Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p>Controle suas finanças com clareza — comece fazendo login.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT — FORM
    st.markdown("<div class='form-area'>", unsafe_allow_html=True)
    st.markdown("<div class='form-title'>Bem-vindo de volta</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-sub'>Entre para acessar seu painel financeiro</div>", unsafe_allow_html=True)

    # FORM (inputs + submit)
    with st.form(key="login_form"):
        user = st.text_input("Usuário", placeholder="seu.usuario")
        pwd = st.text_input("Senha", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            # valida no banco
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (user, pwd))
            dados = cursor.fetchone()
            conn.close()

            if dados:
                st.session_state["logado"] = True
                st.session_state["usuario"] = user
                st.success("Login realizado! Redirecionando...")
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    # BOTÕES FORA DO FORM
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Criar conta"):
            # muda para a página de registro do seu app (controlada por app.py)
            st.session_state["pagina"] = "registro"
            st.experimental_rerun()

    with col2:
        if st.button("Esqueci a senha"):
            st.info("Funcionalidade de recuperação de senha ainda não implementada.")

    st.markdown("</div>", unsafe_allow_html=True)  # fecha form-area
    st.markdown("</div>", unsafe_allow_html=True)  # fecha login-card
    st.markdown("</div>", unsafe_allow_html=True)  # fecha login-wrap

# ===== CARREGAR TELA PRINCIPAL =======================================
def carregar_tela():
    if not st.session_state["logado"]:
        # Exibe a tela de login estilizada ou a tela de registro dependendo do estado
        if st.session_state["pagina"] == "login":
            mostrar_login_estilizado()
        else:
            # chama a função de registro (do seu register_page.py)
            mostrar_tela_registro()

    else:
        # Área logada — sidebar com navegação
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

        if escolha == "Dashboard":
            mostrar_dashboard()

        elif escolha == "Despesas":
            mostrar_despesas()

        elif escolha == "Entradas":
            mostrar_entradas()

        elif escolha == "Configurações":
            mostrar_config()

        elif escolha == "Logout":
            st.session_state["logado"] = False
            st.session_state["pagina"] = "login"
            st.session_state["usuario"] = ""
            st.experimental_rerun()

carregar_tela()
