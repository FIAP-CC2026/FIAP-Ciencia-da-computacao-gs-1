from dados import CATEGORIAS, STATUS

ocorrencias = []
por_codigo = {}
fila = []
pilha = []
historico = []


def adicionar(oc):
    ocorrencias.append(oc)
    por_codigo[oc["codigo"]] = oc


# fila: demandas ainda nao examinadas (primeira que entra, primeira que sai)
def enfileirar(codigo):
    fila.append(codigo)


def examinar_proxima():
    if len(fila) == 0:
        return None
    return fila.pop(0)


# pilha: eventos mais recentes ficam no topo
def empilhar_evento(evento):
    pilha.append(evento)


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
