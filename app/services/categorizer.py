CATEGORY_RULES = {'uber eats': 'alimentacao', 'uber': 'transporte', 'starbucks': 'restaurante', 'salario': 'renda', 'netflix': 'entretenimento', 'drogasil': 'pessoal', 'supermercado': 'alimentacao', 'mcdonalds': 'restaurante', 'borges lanches': 'restaurante', 'livraria': 'entretenimento', 'pix recebido': 'pessoal'}

def categorize(estabelecimento):
    nome = estabelecimento.lower()
    for chave, categoria in CATEGORY_RULES.items():
        if chave in nome:
            return categoria
    return "outros"

print(categorize("UBER *TRIP"))
print(categorize("Salario Empresa ABC"))
print(categorize("Loja Desconhecida"))
print(categorize("UBER EATS *PEDIDO"))