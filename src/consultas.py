import estruturas
import dados
from dados import STATUS, NOMES, DIA_ATUAL, validar_ocorrencia, validar_status


def gerar_codigo():
    numero = len(estruturas.por_codigo) + 1
    codigo = "OC" + str(numero).zfill(2)
    while codigo in estruturas.por_codigo or codigo in dados.recusados:
        numero += 1
        codigo = "OC" + str(numero).zfill(2)
    return codigo


def cadastrar(oc):
    oc["codigo"] = gerar_codigo()
    oc["status"] = "aberta"
    oc["dia_abertura"] = DIA_ATUAL
    oc["dia_conclusao"] = None

    ok, motivo = validar_ocorrencia(oc)
    if not ok:
        return False, "não cadastrada: " + motivo

    estruturas.adicionar(oc)
    estruturas.enfileirar(oc["codigo"])
    return True, "ocorrência " + oc["codigo"] + " cadastrada e colocada na fila"


def buscar_por_codigo(codigo):
    codigo = codigo.strip().upper()
    if codigo in estruturas.por_codigo:
        return estruturas.por_codigo[codigo]
    print("ocorrência " + codigo + " não encontrada")
    return None


def filtrar(categoria=None, status=None):
    resultado = []
    for oc in estruturas.ocorrencias:
        if (categoria is None or oc["categoria"] == categoria) and (status is None or oc["status"] == status):
            resultado.append(oc)
    return resultado


def atualizar_status(codigo, novo):
    if not validar_status(novo):
        return False, "status desconhecido: " + novo

    oc = buscar_por_codigo(codigo)
    if oc is None:
        return False, "nada foi alterado"

    atual = oc["status"]
    if atual == novo:
        return False, "a ocorrência já está " + NOMES[novo]
    if atual == "concluida" or STATUS.index(novo) < STATUS.index(atual):
        return False, "não dá pra voltar de " + NOMES[atual] + " para " + NOMES[novo]

    oc["status"] = novo
    if novo == "concluida":
        oc["dia_conclusao"] = DIA_ATUAL
    if oc["codigo"] in estruturas.fila:
        estruturas.fila.remove(oc["codigo"])

    evento = {"codigo": oc["codigo"], "dia": DIA_ATUAL, "de": atual, "para": novo}
    estruturas.historico.append(evento)
    estruturas.empilhar_evento(evento)
    return True, oc["codigo"] + ": " + NOMES[atual] + " -> " + NOMES[novo]
