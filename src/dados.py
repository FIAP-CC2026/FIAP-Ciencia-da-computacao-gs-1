import os

CATEGORIAS = ["iluminacao", "acessibilidade", "limpeza", "conservacao"]
STATUS = ["aberta", "em_andamento", "concluida"]

NOMES = {
    "iluminacao": "Iluminação",
    "acessibilidade": "Acessibilidade",
    "limpeza": "Limpeza",
    "conservacao": "Conservação",
    "aberta": "aberta",
    "em_andamento": "em andamento",
    "concluida": "concluída",
}

# dia simulado de hoje, usado no cadastro e nas atualizacoes
DIA_ATUAL = 30

PASTA_DATA = os.path.join(os.path.dirname(__file__), "..", "data")

# codigos das linhas recusadas, pra nao repetir no cadastro
recusados = []


def validar_status(status):
    return status in STATUS


def validar_ocorrencia(oc):
    if oc["descricao"] == "" or oc["bairro"] == "" or oc["local"] == "":
        return False, "faltou descrição, bairro ou local"
    elif oc["categoria"] not in CATEGORIAS:
        return False, "categoria inválida ou vazia"
    elif not validar_status(oc["status"]):
        return False, "status desconhecido (" + oc["status"] + ")"
    elif oc["dia_abertura"] is None:
        return False, "dia de abertura inválido"
    elif oc["status"] == "concluida" and oc["dia_conclusao"] is None:
        return False, "concluída sem dia de conclusão"
    else:
        return True, "ok"


def para_numero(texto):
    if texto.isdigit():
        return int(texto)
    return None


def ler_csv(nome):
    linhas = []
    with open(os.path.join(PASTA_DATA, nome), encoding="utf-8") as arquivo:
        cabecalho = arquivo.readline().strip().split(";")
        for linha in arquivo:
            if linha.strip() == "":
                continue
            valores = linha.strip("\n").split(";")
            linhas.append(dict(zip(cabecalho, valores)))
    return linhas


def carregar_ocorrencias():
    validas = []
    invalidas = []
    for oc in ler_csv("dados.csv"):
        oc["dia_abertura"] = para_numero(oc["dia_abertura"])
        oc["dia_conclusao"] = para_numero(oc["dia_conclusao"])
        ok, motivo = validar_ocorrencia(oc)
        if ok:
            validas.append(oc)
        else:
            invalidas.append((oc["codigo"], motivo))
            recusados.append(oc["codigo"])
    return validas, invalidas


def carregar_historico():
    eventos = ler_csv("historico.csv")
    for ev in eventos:
        ev["dia"] = int(ev["dia"])
    return eventos
