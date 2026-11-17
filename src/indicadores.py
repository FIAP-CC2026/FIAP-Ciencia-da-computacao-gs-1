from dados import CATEGORIAS, STATUS, NOMES
from estruturas import criar_matriz


# quantas ocorrencias tem em cada categoria
def contar_por_categoria(ocorrencias):
    totais = {}
    for cat in CATEGORIAS:
        totais[cat] = 0
    for oc in ocorrencias:
        totais[oc["categoria"]] += 1
    return totais


def contar_por_status(ocorrencias):
    totais = {}
    for st in STATUS:
        totais[st] = 0
    for oc in ocorrencias:
        totais[oc["status"]] += 1
    return totais


# percorre a lista uma vez so e soma 1 na linha da categoria e coluna do status
def preencher_matriz(matriz, ocorrencias):
    for oc in ocorrencias:
        i = CATEGORIAS.index(oc["categoria"])
        j = STATUS.index(oc["status"])
        matriz[i][j] += 1
    return matriz


# porcentagem, sem dividir por zero se a lista estiver vazia
def proporcao(parte, total):
    if total == 0:
        return 0.0
    return parte / total * 100


# media de dias entre abrir e concluir, so das concluidas
def tempo_medio_conclusao(ocorrencias):
    soma = 0
    qtd = 0
    for oc in ocorrencias:
        if oc["status"] == "concluida":
            soma += oc["dia_conclusao"] - oc["dia_abertura"]
            qtd += 1
    if qtd == 0:
        return soma, qtd, None
    return soma, qtd, soma / qtd


def mais_pendente(matriz):
    # pendente = aberta + em andamento (colunas 0 e 1 da matriz)
    # devolve uma lista porque pode dar empate
    maior = 0
    categorias = []
    for i in range(len(CATEGORIAS)):
        pendentes = matriz[i][0] + matriz[i][1]
        if pendentes > maior:
            maior = pendentes
            categorias = [CATEGORIAS[i]]
        elif pendentes == maior and maior > 0:
            categorias.append(CATEGORIAS[i])
    return categorias, maior


def linha(indicador, origem, formula, resultado):
    print(f"{indicador:<22}{origem:<20}{formula:<26}{resultado}")


# tabela com dados de origem, formula e resultado de cada indicador
def mostrar_tabela(ocorrencias):
    total = len(ocorrencias)
    por_cat = contar_por_categoria(ocorrencias)
    por_st = contar_por_status(ocorrencias)

    print()
    linha("INDICADOR", "DADOS DE ORIGEM", "FÓRMULA", "RESULTADO")
    print("-" * 78)
    linha("Total", f"{total} válidas", "contagem da lista", total)

    for cat in CATEGORIAS:
        pct = proporcao(por_cat[cat], total)
        linha(NOMES[cat] + " (%)", f"{por_cat[cat]} de {total}", "categoria / total x 100", f"{pct:.1f}%")

    for st in STATUS:
        pct = proporcao(por_st[st], total)
        linha(NOMES[st].capitalize() + " (%)", f"{por_st[st]} de {total}", "status / total x 100", f"{pct:.1f}%")

    pendentes = por_st["aberta"] + por_st["em_andamento"]
    linha("Pendências", f"{por_st['aberta']} + {por_st['em_andamento']}", "aberta + em andamento", pendentes)

    soma, qtd, media = tempo_medio_conclusao(ocorrencias)
    if media is None:
        linha("Tempo médio", "nenhuma concluída", "soma dias / concluídas", "-")
    else:
        linha("Tempo médio", f"{soma} dias / {qtd}", "soma dias / concluídas", f"{media:.1f} dias")


def mostrar_matriz(matriz):
    print()
    print(f"{'categoria x status':<18}{'aberta':>8}{'andamento':>11}{'concluída':>11}{'total':>7}")
    print("-" * 55)
    for i in range(len(CATEGORIAS)):
        print(f"{NOMES[CATEGORIAS[i]]:<18}{matriz[i][0]:>8}{matriz[i][1]:>11}{matriz[i][2]:>11}{sum(matriz[i]):>7}")


# interpreta os numeros, a frase muda conforme o resultado
def gerar_conclusao(ocorrencias, matriz):
    total = len(ocorrencias)
    if total == 0:
        return ["sem ocorrências cadastradas, não tem o que analisar"]

    frases = []
    por_st = contar_por_status(ocorrencias)
    pendentes = por_st["aberta"] + por_st["em_andamento"]
    pct = proporcao(pendentes, total)

    if pct >= 60:
        frases.append(f"{pct:.0f}% ainda está pendente, o bairro está acumulando demanda.")
    elif pct >= 40:
        frases.append(f"{pct:.0f}% ainda está pendente, quase metade, precisa de atenção.")
    else:
        frases.append(f"só {pct:.0f}% está pendente, a maior parte já foi resolvida.")

    categorias, qtd = mais_pendente(matriz)
    if len(categorias) == 1:
        frase = f"{NOMES[categorias[0]]} é a categoria com mais pendências ({qtd})."
    elif len(categorias) > 1:
        nomes = [NOMES[c] for c in categorias]
        frase = f"{' e '.join(nomes)} empatam com mais pendências ({qtd} cada)."
    if len(categorias) > 0:
        if "acessibilidade" in categorias:
            frase += " Isso pesa mais pra quem tem mobilidade reduzida, então deveria ser prioridade."
        frases.append(frase)

    soma, qtd_conc, media = tempo_medio_conclusao(ocorrencias)
    if media is None:
        frases.append("nenhuma ocorrência foi concluída ainda, então não dá pra medir o tempo.")
    elif media <= 7:
        frases.append(f"as concluídas levaram {media:.1f} dias em média, dentro de uma semana.")
    else:
        frases.append(f"as concluídas levaram {media:.1f} dias em média, mais de uma semana.")

    frases.append("os dados são fictícios, então os números mostram o método e não um bairro real.")
    return frases


def mostrar_indicadores(ocorrencias):
    matriz = preencher_matriz(criar_matriz(), ocorrencias)
    print("\n=== INDICADORES ===")
    mostrar_tabela(ocorrencias)
    mostrar_matriz(matriz)
    print("\nconclusão:")
    for frase in gerar_conclusao(ocorrencias, matriz):
        print("- " + frase)
