from pathlib import Path

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from app.services.analyzer import load_transactions, monthly_summary, category_summary

st.set_page_config(page_title="Finance Tracker", page_icon="💰", layout="wide")


def carregar_css(caminho):
    css = Path(caminho).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


carregar_css("assets/style.css")

CORES = {
    "entrada": "#00F5D4",
    "saida": "#F15BB5",
    "saldo": "#9B5DE5",
}

PALETA_NEON = ["#00F5D4", "#00BBF9", "#9B5DE5", "#F15BB5", "#FEE440"]


def aplicar_tema(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#E6F1FF", size=13),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=1.12, x=0),
        hoverlabel=dict(bgcolor="#0D1424", bordercolor="#00F5D4", font_size=13),
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(255,255,255,0.15)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.07)", zeroline=False)
    return fig


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
        fig_mes.add_bar(
            x=mensal["mes"], y=mensal["entrada"], name="Entradas",
            marker=dict(color=CORES["entrada"], cornerradius=8),
        )
        fig_mes.add_bar(
            x=mensal["mes"], y=mensal["saida"], name="Saídas",
            marker=dict(color=CORES["saida"], cornerradius=8),
        )
        fig_mes.add_scatter(
            x=mensal["mes"],
            y=mensal["saldo"],
            name="Saldo",
            mode="lines+markers",
            line=dict(color=CORES["saldo"], width=4, shape="spline"),
            marker=dict(size=11, color="#070B14", line=dict(color=CORES["saldo"], width=3)),
        )
        fig_mes.update_layout(barmode="group", bargap=0.35)
        aplicar_tema(fig_mes)
        st.plotly_chart(fig_mes, use_container_width=True)

    with aba_cat:
        st.subheader("Gastos por categoria")
        categorias = category_summary(df).reset_index()
        fig_cat = px.pie(
            categorias, names="categoria", values="valor", hole=0.62,
            color_discrete_sequence=PALETA_NEON,
        )
        fig_cat.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="#070B14", width=3)),
            pull=[0.03] * len(categorias),
        )
        aplicar_tema(fig_cat)
        st.plotly_chart(fig_cat, use_container_width=True)

    with aba_trans:
        st.subheader("Transações")
        st.dataframe(df, use_container_width=True)