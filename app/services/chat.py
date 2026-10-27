import ollama

MODELO = "llama3.1:8b"


def montar_contexto(mensal, categorias):
    categorias = categorias.sort_values("valor", ascending=False)

    maior = categorias.iloc[0]
    menor = categorias.iloc[-1]
    total_saidas = categorias["valor"].sum()
    melhor_mes = mensal.loc[mensal["saldo"].idxmax()]
    pior_mes = mensal.loc[mensal["saldo"].idxmin()]

    linhas = [
        "FATOS JA CALCULADOS (confie neles):",
        f"- Categoria com MAIOR gasto: {maior['categoria']} (R$ {maior['valor']:.2f})",
        f"- Categoria com MENOR gasto: {menor['categoria']} (R$ {menor['valor']:.2f})",
        f"- Total gasto em todas as categorias: R$ {total_saidas:.2f}",
        f"- Mes com MAIOR saldo: {melhor_mes['mes']} (R$ {melhor_mes['saldo']:.2f})",
        f"- Mes com MENOR saldo: {pior_mes['mes']} (R$ {pior_mes['saldo']:.2f})",
        "",
        "Gastos por categoria, do maior para o menor:",
    ]
    for _, r in categorias.iterrows():
        linhas.append(f"- {r['categoria']}: R$ {r['valor']:.2f}")

    linhas.append("")
    linhas.append("Resumo mensal:")
    for _, r in mensal.iterrows():
        linhas.append(
            f"- {r['mes']}: entradas R$ {r['entrada']:.2f}, saidas R$ {r['saida']:.2f}, saldo R$ {r['saldo']:.2f}"
        )
    return "\n".join(linhas)


def perguntar(contexto, historico):
    sistema = (
        "Voce e um assistente financeiro. Responda em portugues do Brasil, "
        "em no maximo 3 frases. Use SOMENTE os dados abaixo e nunca calcule "
        "nada por conta propria: use os FATOS JA CALCULADOS quando a pergunta "
        "for sobre maior, menor ou total. Se a resposta nao estiver nos dados, "
        "diga que nao sabe.\n\n" + contexto
    )
    mensagens = [{"role": "system", "content": sistema}] + historico
    resposta = ollama.chat(
        model=MODELO,
        messages=mensagens,
        options={"temperature": 0},
    )
    return resposta["message"]["content"]