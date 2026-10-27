from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

DATASET = Path("data/training/categorias.csv")
MODELO = Path("models/categorizer.joblib")


def treinar():
    dados = pd.read_csv(DATASET)
    X = dados["estabelecimento"].str.lower()
    y = dados["categoria"]

    modelo = make_pipeline(
        TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)),
        LogisticRegression(max_iter=1000),
    )
    modelo.fit(X, y)

    MODELO.parent.mkdir(exist_ok=True)
    joblib.dump(modelo, MODELO)
    return modelo


def carregar():
    if MODELO.exists():
        return joblib.load(MODELO)
    return treinar()


def categorize_ml(estabelecimento):
    modelo = carregar()
    return modelo.predict([estabelecimento.lower()])[0]


if __name__ == "__main__":
    treinar()
    print("Modelo treinado e salvo em", MODELO)
    print(categorize_ml("IFOOD *PEDIDO 8823"))
    print(categorize_ml("POSTO BR"))
    print(categorize_ml("NETFLIX MENSAL"))