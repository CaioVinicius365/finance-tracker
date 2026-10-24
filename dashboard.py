import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
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

    aba_geral, aba_cat, aba_trans = st.tabs(["Visão geral", "Categorias", "Transações"])

    with aba_geral:
        st.subheader("Resumo mensal")
        mensal = monthly_summary(df).reset_index()
        mensal["mes"] = mensal["mes"].astype(str)

        fig_mes = go.Figure()
        fig_mes.add_bar(x=mensal["mes"], y=mensal["entrada"], name="Entradas", marker_color="#00C48C")
        fig_mes.add_bar(x=mensal["mes"], y=mensal["saida"], name="Saídas", marker_color="#FF5C5C")
        fig_mes.add_scatter(
            x=mensal["mes"],
            y=mensal["saldo"],
            name="Saldo",
            mode="lines+markers",
            line=dict(color="#4C8BF5", width=3),
        )
        fig_mes.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            barmode="group",
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig_mes, use_container_width=True)

    with aba_cat:
        st.subheader("Gastos por categoria")
        categorias = category_summary(df).reset_index()
        fig_cat = px.pie(categorias, names="categoria", values="valor", hole=0.5)
        fig_cat.update_traces(textinfo="percent+label")
        fig_cat.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cat, use_container_width=True)

    with aba_trans:
        st.subheader("Transações")
        st.dataframe(df, use_container_width=True)