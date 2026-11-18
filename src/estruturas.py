from dados import CATEGORIAS, STATUS

ocorrencias = []
por_codigo = {}
fila = []
pilha = []
historico = []


def adicionar(oc):
    ocorrencias.append(oc)
    por_codigo[oc["codigo"]] = oc


def enfileirar(codigo):
    if codigo not in fila:
        fila.append(codigo)


def fila_vazia():
    return len(fila) == 0


def tamanho_fila():
    return len(fila)


def examinar_proxima():
    if fila_vazia():
        return None
    return fila.pop(0)


def empilhar_evento(evento):
    pilha.append(evento)


def pilha_vazia():
    return len(pilha) == 0


def tamanho_pilha():
    return len(pilha)


def desempilhar_evento():
    if pilha_vazia():
        return None
    return pilha.pop()


def ver_ultimos(n):
    ultimos = []
    i = len(pilha) - 1
    while i >= 0 and len(ultimos) < n:
        ultimos.append(pilha[i])
        i -= 1
    return ultimos


def montar_hierarquia():
    hierarquia = {}
    for oc in ocorrencias:
        bairro = oc["bairro"]
        if bairro not in hierarquia:
            hierarquia[bairro] = {}
        if oc["categoria"] not in hierarquia[bairro]:
            hierarquia[bairro][oc["categoria"]] = []
        hierarquia[bairro][oc["categoria"]].append(oc["codigo"])
    return hierarquia


def criar_matriz():
    matriz = []
    for _ in CATEGORIAS:
        matriz.append([0] * len(STATUS))
    return matriz
