import pandas as pd
from app.services.categorizer import categorize

def load_transactions(path, categorizer=categorize):
    df = pd.read_csv(path)
    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.to_period("M")
    df["categoria"] = df["estabelecimento"].apply(categorizer)
    return df

def monthly_summary(df):
    resumo = df.groupby(["mes", "tipo"])["valor"].sum().unstack()
    resumo["saldo"] = resumo["entrada"] - resumo["saida"]
    return resumo

def category_summary(df):
    gastos = df[df["tipo"] == "saida"]
    resumo = gastos.groupby("categoria")["valor"].sum()
    return resumo