import pandas as pd
from app.services.analyzer import monthly_summary


def test_monthly_summary_balance():
    df = pd.DataFrame({
        "mes": ["2026-08", "2026-08"],
        "tipo": ["entrada", "saida"],
        "valor": [1000, 300]
    })
    resumo = monthly_summary(df)
    assert resumo.loc["2026-08", "saldo"] == 700

