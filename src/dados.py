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


DIA_ATUAL = 30

PASTA_DATA = os.path.join(os.path.dirname(__file__), "..", "data")

recusados = []

eventos_recusados = []


def validar_status(status):
    return status in STATUS


def validar_ocorrencia(oc):
    abertura = oc["dia_abertura"]
    conclusao = oc["dia_conclusao"]
    concluida = oc["status"] == "concluida"

    if oc["descricao"] == "" or oc["bairro"] == "" or oc["local"] == "":
        return False, "faltou descrição, bairro ou local"
    elif oc["categoria"] not in CATEGORIAS:
        return False, "categoria inválida ou vazia"
    elif not validar_status(oc["status"]):
        return False, "status desconhecido (" + str(oc["status"]) + ")"
    elif abertura is None or abertura > DIA_ATUAL:
        return False, "dia de abertura inválido"
    elif concluida and conclusao is None:
        return False, "concluída sem dia de conclusão"
    elif not concluida and conclusao is not None:
        return False, "tem dia de conclusão mas não está concluída"
    elif concluida and conclusao < abertura:
        return False, "concluída antes de ser aberta"
    else:
        return True, "ok"



def validar_evento(ev, codigos=None):
    if codigos is not None and ev["codigo"] not in codigos:
        return False, "código inexistente"
    elif not (validar_status(ev["de"]) and validar_status(ev["para"])):
        return False, "status desconhecido (" + str(ev["de"]) + " -> " + str(ev["para"]) + ")"
    elif ev["dia"] is None or ev["dia"] > DIA_ATUAL:
        return False, "dia inválido"
    elif STATUS.index(ev["para"]) <= STATUS.index(ev["de"]):
        return False, "o status não anda pra frente"
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
            valores = []
            for v in linha.strip("\n").split(";"):
                valores.append(v.strip())
            while len(valores) < len(cabecalho):
                valores.append("")
            linhas.append(dict(zip(cabecalho, valores)))
    return linhas


def carregar_ocorrencias():
    validas = []
    invalidas = []
    vistos = []
    for oc in ler_csv("dados.csv"):
        oc["dia_abertura"] = para_numero(oc["dia_abertura"])
        oc["dia_conclusao"] = para_numero(oc["dia_conclusao"])
        ok, motivo = validar_ocorrencia(oc)
       
        if ok and oc["codigo"] == "":
            ok, motivo = False, "sem código"
        elif ok and oc["codigo"] in vistos:
            ok, motivo = False, "código repetido"
        if ok:
            vistos.append(oc["codigo"])
            validas.append(oc)
        else:
            invalidas.append((oc["codigo"], motivo))
            if oc["codigo"] != "" and oc["codigo"] not in vistos:
                recusados.append(oc["codigo"])
    return validas, invalidas



def carregar_historico(codigos=None):
    eventos = []
    eventos_recusados.clear()
    for ev in ler_csv("historico.csv"):
        ev["dia"] = para_numero(ev["dia"])
        ok, motivo = validar_evento(ev, codigos)
        if ok:
            eventos.append(ev)
        else:
            eventos_recusados.append(ev["codigo"] + " (dia " + str(ev["dia"]) + "): " + motivo)
    return eventos
