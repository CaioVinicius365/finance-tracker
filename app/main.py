from fastapi import FastAPI
from app.services.analyzer import load_transactions, monthly_summary

app = FastAPI()

@app.get("/health")
async def root():
    return {"status": "ok"}

@app.get("/summary/monthly")
def monthly():
    df = load_transactions("data/samples/extrato_exemplo.csv")
    resumo = monthly_summary(df)
    resumo = resumo.reset_index()
    resumo["mes"] = resumo["mes"].astype(str)
    print(resumo, flush=True)
    return resumo.to_dict(orient="records")