import streamlit as st
import plotly.express as px
from app.services.analyzer import load_transactions, monthly_summary, category_summary

st.set_page_config(page_title="Finance Tracker", page_icon="💰", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        background-color: #1A1F2B;
        border: 1px solid #2A3142;
        padding: 16px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Finance Tracker")

arquivo = st.file_uploader("Envie seu extrato em CSV", type="csv")

if arquivo is not None:
    df = load_transactions(arquivo)
    st.write("Transações carregadas:", len(df))

    resumo_mensal = monthly_summary(df)
    total_entrada = resumo_mensal["entrada"].sum()
    total_saida = resumo_mensal["saida"].sum()
    saldo_total = total_entrada - total_saida

    col1, col2, col3 = st.columns(3)
    col1.metric("Entradas", f"R$ {total_entrada:,.2f}")
    col2.metric("Saídas", f"R$ {total_saida:,.2f}")
    col3.metric("Saldo", f"R$ {saldo_total:,.2f}")

    st.dataframe(df)

    st.subheader("Gastos por categoria")
    categorias = category_summary(df).reset_index()
    fig_cat = px.pie(categorias, names="categoria", values="valor", hole=0.5)
    fig_cat.update_traces(textinfo="percent+label")
    fig_cat.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Resumo mensal")
    mensal = monthly_summary(df).reset_index()
    mensal["mes"] = mensal["mes"].astype(str)
    mensal = mensal.melt(
        id_vars="mes",
        value_vars=["entrada", "saida", "saldo"],
        var_name="tipo",
        value_name="valor",
    )
    fig_mes = px.bar(
        mensal,
        x="mes",
        y="valor",
        color="tipo",
        barmode="group",
        color_discrete_map={
            "entrada": "#00C48C",
            "saida": "#FF5C5C",
            "saldo": "#4C8BF5",
        },
    )
    fig_mes.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_mes, use_container_width=True)