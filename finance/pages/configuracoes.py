# pages/configuracoes.py
import streamlit as st
import pandas as pd
import io
import os
from database import listar_entradas, listar_despesas, conectar, hash_senha

st.set_page_config(page_title="Configurações", layout="wide")

def mostrar_config():
    st.title("⚙️ Configurações")
    st.write("Ajustes de conta, perfil e preferências.")


css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if "usuario" not in st.session_state:
    st.warning("Você precisa fazer login.")
    st.stop()

user = st.session_state["usuario"]

st.title("⚙️ Configurações")
st.markdown("Exportar dados, trocar senha, excluir conta e ajustar tema.")

# ---------------- EXPORTAR DADOS ----------------
st.subheader("📤 Exportar dados")
st.markdown("Exporte suas entradas e despesas em CSV para backup ou análise externa.")

entradas = listar_entradas(user)
despesas = listar_despesas(user)

df_ent = pd.DataFrame(entradas, columns=["ID","Descrição","Valor","Categoria","Data"]) if entradas else pd.DataFrame()
df_desp = pd.DataFrame(despesas, columns=["ID","Descrição","Valor","Categoria","Data"]) if despesas else pd.DataFrame()

def to_csv_bytes(df: pd.DataFrame):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

col1, col2 = st.columns(2)
with col1:
    if not df_ent.empty:
        st.download_button("📥 Baixar Entradas (CSV)", data=to_csv_bytes(df_ent), file_name=f"entradas_{user}.csv", mime="text/csv", key="dl_ent")
    else:
        st.button("📥 Baixar Entradas (CSV)", disabled=True, key="dl_ent_disabled")

with col2:
    if not df_desp.empty:
        st.download_button("📥 Baixar Despesas (CSV)", data=to_csv_bytes(df_desp), file_name=f"despesas_{user}.csv", mime="text/csv", key="dl_desp")
    else:
        st.button("📥 Baixar Despesas (CSV)", disabled=True, key="dl_desp_disabled")

if not df_ent.empty or not df_desp.empty:
    # export combined zip-like single CSV (concat)
    combined = pd.concat([df_ent.assign(Tipo="Entrada"), df_desp.assign(Tipo="Despesa")], ignore_index=True)
    st.download_button("📥 Baixar Todas (CSV)", data=to_csv_bytes(combined), file_name=f"movimentacoes_{user}.csv", mime="text/csv", key="dl_all")

st.markdown("---")

# ---------------- TROCAR SENHA ----------------
st.subheader("🔐 Trocar senha")
st.markdown("Digite sua senha atual e a nova senha. A alteração acontece imediatamente.")

cur_pass = st.text_input("Senha atual", type="password", key="cfg_cur_pass")
new_pass = st.text_input("Nova senha", type="password", key="cfg_new_pass")
confirm_pass = st.text_input("Confirmar nova senha", type="password", key="cfg_confirm_pass")

def update_password(usuario, atual, nova):
    conn = conectar()
    cur = conn.cursor()
    # valida senha atual
    cur.execute("SELECT senha FROM usuarios WHERE username = ?", (usuario,))
    row = cur.fetchone()
    if not row:
        return False, "Usuário não encontrado."
    if row[0] != hash_senha(atual):
        return False, "Senha atual incorreta."
    # atualiza senha
    cur.execute("UPDATE usuarios SET senha = ? WHERE username = ?", (hash_senha(nova), usuario))
    conn.commit()
    return True, "Senha atualizada com sucesso."

if st.button("Trocar senha", key="cfg_change_pass_btn"):
    if not cur_pass or not new_pass or not confirm_pass:
        st.warning("Preencha todos os campos.")
    elif new_pass != confirm_pass:
        st.error("A nova senha e a confirmação não coincidem.")
    else:
        ok, msg = update_password(user, cur_pass, new_pass)
        if ok:
            st.success(msg)
        else:
            st.error(msg)

st.markdown("---")

# ---------------- DELETAR CONTA ----------------
st.subheader("🗑️ Excluir conta")
st.markdown("Esta ação é irreversível: suas entradas, despesas e usuário serão removidos do banco. Use com cuidado.")

confirm = st.text_input("Digite 'DELETE' para confirmar", key="cfg_del_confirm")
if st.button("Excluir minha conta e dados", key="cfg_del_btn"):
    if confirm != "DELETE":
        st.error("Você precisa digitar exatamente DELETE para confirmar.")
    else:
        conn = conectar()
        cur = conn.cursor()
        # apagar despesas e entradas e usuário
        cur.execute("DELETE FROM despesas WHERE usuario = ?", (user,))
        cur.execute("DELETE FROM entradas WHERE usuario = ?", (user,))
        cur.execute("DELETE FROM usuarios WHERE username = ?", (user,))
        conn.commit()
        st.success("Conta e dados apagados. Você será desconectado.")
        # limpar sessão e forçar reload (volta ao login)
        st.session_state.clear()
        st.rerun()

st.markdown("---")

# ---------------- TEMA (simples) ----------------
st.subheader("🎨 Tema")
st.markdown("Alternar entre tema Claro e Escuro (apenas injetando CSS alternativo).")

theme = st.radio("Escolha o tema", ["Claro", "Escuro"], index=0, key="cfg_theme_radio")

if theme == "Escuro":
    dark_css = """
    <style>
    .main { background-color: #0f1724 !important; color: #e6eef8 !important; }
    .card { background: #0b1220 !important; box-shadow: none !important; color: #e6eef8 !important; }
    .stButton>button { background-color: #1f6feb !important; color: white !important; }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    # reload original style.css (if present)
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

st.markdown("---")
if st.button("Voltar ao Dashboard", key="cfg_voltar"):
    st.switch_page("pages/dashboard.py")
