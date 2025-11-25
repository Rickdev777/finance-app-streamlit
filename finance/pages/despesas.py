import os
import streamlit as st
import pandas as pd
from database import listar_despesas, adicionar_despesa, editar_despesa, excluir_despesa

st.set_page_config(page_title="Despesas", layout="wide")


def mostrar_despesas():
    st.title("💸 Despesas")
    st.write("Gerenciamento de despesas.")
    st.write("Aqui você pode cadastrar, visualizar e editar suas despesas.")


css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if "usuario" not in st.session_state or not st.session_state["usuario"]:
    try:
        st.warning("Você precisa fazer login para acessar as despesas.")
        st.stop()
    except Exception:
        st.stop()

user = st.session_state["usuario"]

st.title("💸 Despesas")

despesas = listar_despesas(user)
df = pd.DataFrame(despesas, columns=["ID", "Descrição", "Valor", "Categoria", "Data"]) if despesas else pd.DataFrame(columns=["ID","Descrição","Valor","Categoria","Data"])

st.markdown("## ➕ Nova Despesa")
col1, col2 = st.columns(2)

with col1:
    desc = st.text_input("Descrição", key="desp_desc")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f", key="desp_valor")

with col2:
    cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Boletos", "Outros"], key="desp_cat")
    data = st.date_input("Data", key="desp_data")

if st.button("Adicionar", key="desp_add_btn"):
    if not desc:
        st.warning("Preencha a descrição.")
    else:
        adicionar_despesa(user, desc, float(valor), cat, str(data))
        st.success("Despesa adicionada!")
        st.rerun()

st.markdown("## 📋 Minhas Despesas")
st.dataframe(df, use_container_width=True, height=400)

if not df.empty:
    st.markdown("---")
    st.markdown("### ✏️ Editar / Excluir")

    id_edit = st.selectbox("Selecione o ID", df["ID"], key="desp_sel_id")

    row = df[df["ID"] == id_edit].iloc[0]

    with st.expander("Editar despesa selecionada"):
        new_desc = st.text_input("Descrição", value=row["Descrição"], key=f"desp_edit_desc_{id_edit}")
        new_val = st.number_input("Valor", value=float(row["Valor"]), key=f"desp_edit_val_{id_edit}")
        new_cat = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Boletos", "Outros"],
                               index=(["Alimentação","Transporte","Lazer","Boletos","Outros"].index(row["Categoria"])
                                      if row["Categoria"] in ["Alimentação","Transporte","Lazer","Boletos","Outros"] else 0),
                               key=f"desp_edit_cat_{id_edit}")
        new_date = st.date_input("Data", value=pd.to_datetime(row["Data"]), key=f"desp_edit_date_{id_edit}")

        if st.button("Salvar edição", key=f"desp_save_btn_{id_edit}"):
            editar_despesa(id_edit, new_desc, float(new_val), new_cat, str(new_date))
            st.success("Despesa atualizada!")
            st.rerun()

    if st.button("Excluir despesa selecionada", key=f"desp_del_btn_{id_edit}"):
        excluir_despesa(id_edit)
        st.success("Despesa excluída!")
        st.rerun()
