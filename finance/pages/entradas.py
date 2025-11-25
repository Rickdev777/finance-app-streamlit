# pages/entradas.py
import streamlit as st
import pandas as pd
import os
from database import (
    listar_entradas,
    adicionar_entrada,
    editar_entrada,
    excluir_entrada
)

CATEGORIAS_ENTRADA = ["Salário", "Pix", "Bônus", "Presente", "Outros"]

st.set_page_config(page_title="Entradas", layout="wide")


def mostrar_entradas():
    st.title("📥 Entradas")
    st.write("Gerenciamento de entradas.")
    st.write("Aqui você controla suas receitas e entradas financeiras.")

css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if "usuario" not in st.session_state:
    st.warning("Você precisa fazer login.")
    st.stop()

user = st.session_state["usuario"]

st.title("📥 Entradas")
st.markdown("Registre suas receitas aqui. Edição rápida com expander, keys únicas para evitar conflitos.")

# ---------- ADICIONAR ENTRADA ----------
with st.container():
    st.markdown("<div class='card'><h3>➕ Nova Entrada</h3></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2,1])
    with c1:
        desc = st.text_input("Descrição", key="entrada_desc_input")
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", key="entrada_valor_input")
    with c2:
        cat = st.selectbox("Categoria", CATEGORIAS_ENTRADA, key="entrada_cat_input")
        data = st.date_input("Data", key="entrada_data_input")
    if st.button("Adicionar Entrada", key="entrada_add_btn"):
        if not desc:
            st.warning("Preencha a descrição.")
        else:
            adicionar_entrada(user, desc, float(valor), cat, str(data))
            st.success("Entrada adicionada.")
            st.rerun()

st.markdown("---")

# ---------- LISTAR ENTRADAS ----------
st.subheader("📋 Minhas Entradas")
entradas = listar_entradas(user)
df_e = pd.DataFrame(entradas, columns=["ID", "Descrição", "Valor", "Categoria", "Data"]) if entradas else pd.DataFrame(columns=["ID","Descrição","Valor","Categoria","Data"])

if df_e.empty:
    st.info("Nenhuma entrada cadastrada.")
else:
    st.dataframe(df_e, use_container_width=True, height=350)

    st.markdown("### ✏ Editar / Excluir Entrada")
    id_sel = st.selectbox("Selecione o ID da entrada para editar/excluir", df_e["ID"], key="entrada_sel_id")

    row = df_e[df_e["ID"] == id_sel].iloc[0]

    with st.expander("Editar entrada selecionada"):
        new_desc = st.text_input("Descrição", value=row["Descrição"], key=f"entrada_edit_desc_{id_sel}")
        new_valor = st.number_input("Valor", value=float(row["Valor"]), key=f"entrada_edit_valor_{id_sel}")
        new_cat = st.selectbox(
            "Categoria",
            CATEGORIAS_ENTRADA,
            index=CATEGORIAS_ENTRADA.index(row["Categoria"]) if row["Categoria"] in CATEGORIAS_ENTRADA else 0,
            key=f"entrada_edit_cat_{id_sel}"
        )
        new_data = st.date_input("Data", value=pd.to_datetime(row["Data"]), key=f"entrada_edit_data_{id_sel}")

        if st.button("Salvar edição (entrada)", key=f"entrada_save_btn_{id_sel}"):
            editar_entrada(id_sel, new_desc, float(new_valor), new_cat, str(new_data))
            st.success("Entrada atualizada.")
            st.rerun()

    if st.button("Excluir entrada selecionada", key=f"entrada_del_btn_{id_sel}"):
        excluir_entrada(id_sel)
        st.success("Entrada excluída.")
        st.rerun()

# link rápido para voltar ao dashboard
st.markdown("---")
if st.button("Voltar ao Dashboard", key="voltar_dashboard_from_entradas"):
    st.switch_page("pages/dashboard.py")
