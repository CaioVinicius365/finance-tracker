from app.services.categorizer import categorize

def test_uber_is_transport():
    assert categorize("UBER *TRIP") == "transporte"

def test_uber():
    assert categorize("UBER") == "transporte"
    assert categorize("uber") == "transporte"

def test_unknown():
    assert categorize("Loja desconhecida") == "outros"

def test_uber_eats():
    assert categorize("UBER EATS *PEDIDO") == "alimentacao"
