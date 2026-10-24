from fastapi import FastAPI, File, UploadFile
from app.services.analyzer import load_transactions, monthly_summary, category_summary
import pandas as pd

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
    return resumo.to_dict(orient="records")

@app.get("/summary/categories")
def categories():
    df = load_transactions("data/samples/extrato_exemplo.csv")
    resumo = category_summary(df)
    resumo = resumo.reset_index()
    return resumo.to_dict(orient="records")

@app.post("/upload/summary")
def upload_summary(file: UploadFile = File(...)):
    df = load_transactions(file.file)
    return {
        "monthly": monthly_summary(df).reset_index().astype({"mes": str}).to_dict(orient="records"),
        "categories": category_summary(df).reset_index().to_dict(orient="records"),
    }