import streamlit as st
from app.services.analyzer import load_transactions, monthly_summary, category_summary

st.title("Finance Tracker")

arquivo = st.file_uploader("Envie seu extrato em CSV", type="csv")

if arquivo is not None:
    df = load_transactions(arquivo)
    st.write("Transações carregadas:", len(df))
    st.dataframe(df)
    st.subheader("Gastos por categoria")
    st.bar_chart(category_summary(df))
    st.subheader("Resumo mensal")
    resumo = monthly_summary(df)
    resumo.index = resumo.index.astype(str)
    st.bar_chart(resumo[["entrada", "saida", "saldo"]])