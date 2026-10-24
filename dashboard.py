import streamlit as st
from app.services.analyzer import load_transactions, monthly_summary, category_summary

st.title("Finance Tracker")

arquivo = st.file_uploader("Envie seu extrato em CSV", type="csv")

if arquivo is not None:
    df = load_transactions(arquivo)
    st.write("Transações carregadas:", len(df))
    st.dataframe(df)