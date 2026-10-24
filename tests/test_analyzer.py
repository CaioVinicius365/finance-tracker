import pandas as pd
from app.services.analyzer import monthly_summary, category_summary


def test_monthly_summary_balance():
    df = pd.DataFrame({
        "mes": ["2026-08", "2026-08"],
        "tipo": ["entrada", "saida"],
        "valor": [1000, 300]
    })
    resumo = monthly_summary(df)
    assert resumo.loc["2026-08", "saldo"] == 700


def test_category_summary_ignores_income():
    df = pd.DataFrame({
        "categoria": ["renda", "restaurante", "restaurante"],
        "tipo": ["entrada", "saida", "saida"],
        "valor": [1000, 40, 60],
    })
    resumo = category_summary(df)
    assert resumo["restaurante"] == 100
    assert "renda" not in resumo.index