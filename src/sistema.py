# painel de ocorrencias do bairro
# como rodar, na pasta do projeto: python src/sistema.py

import dados
import estruturas
import consultas
import indicadores
from dados import CATEGORIAS, STATUS, NOMES

SIGNIFICADO = {
    "aberta": "registrada, ninguém examinou ainda (fica na fila)",
    "em_andamento": "alguém já está cuidando",
    "concluida": "problema resolvido",
}


# le o que a pessoa digita; se a entrada acabar, sai do programa sem erro
def ler(mensagem):
    try:
        return input(mensagem).strip()
    except EOFError:
        return "0"


# le os arquivos da pasta data e coloca tudo nas estruturas
def carregar():
    validas, invalidas = dados.carregar_ocorrencias()
    for oc in validas:
        estruturas.adicionar(oc)
        if oc["status"] == "aberta":
            estruturas.enfileirar(oc["codigo"])

    for ev in dados.carregar_historico():
        estruturas.historico.append(ev)
        estruturas.empilhar_evento(ev)

    print(f"{len(validas)} ocorrências carregadas, {len(estruturas.historico)} eventos no histórico")
    for codigo, motivo in invalidas:
        print(f"aviso: {codigo} ignorada, {motivo}")


# mostra as opcoes numeradas e devolve a escolhida (None se deixar em branco)
def escolher(titulo, opcoes):
    print(titulo)
    for i in range(len(opcoes)):
        print(f"  {i + 1} - {NOMES[opcoes[i]]}")
    resp = ler("número (enter pra deixar em branco): ")
    if resp == "":
        return None
    if resp.isdigit() and 1 <= int(resp) <= len(opcoes):
        return opcoes[int(resp) - 1]
    return resp


def mostrar(lista):
    if len(lista) == 0:
        print("nenhuma ocorrência")
        return
    for oc in lista:
        print(f"{oc['codigo']} | {NOMES[oc['categoria']]:<14} | {oc['bairro']:<18} | {oc['local']:<17} | {NOMES[oc['status']]}")


# opcoes do menu

def opcao_cadastrar():
    print("não coloque nome, telefone ou endereço exato")
    oc = {}
    oc["bairro"] = ler("bairro: ")
    oc["local"] = ler("local (ex: praça, rua, escola): ")
    oc["categoria"] = escolher("categoria:", CATEGORIAS) or ""
    oc["descricao"] = ler("descrição: ")
    ok, msg = consultas.cadastrar(oc)
    print(msg)


def opcao_buscar():
    oc = consultas.buscar_por_codigo(ler("código (ex: OC03): "))
    if oc is not None:
        mostrar([oc])
        print("descrição: " + oc["descricao"])
        texto = f"aberta no dia {oc['dia_abertura']}"
        if oc["dia_conclusao"] is not None:
            texto += f", concluída no dia {oc['dia_conclusao']}"
        print(texto)


def opcao_filtrar():
    categoria = escolher("categoria:", CATEGORIAS)
    status = escolher("status:", STATUS)
    # filtro em branco vale como "todas"; qualquer outro valor fora da lista e erro
    if (categoria is not None and categoria not in CATEGORIAS) or (status is not None and status not in STATUS):
        print("opção inválida no filtro")
        return
    mostrar(consultas.filtrar(categoria, status))


def opcao_atualizar():
    codigo = ler("código: ")
    novo = escolher("novo status:", STATUS)
    if novo is None:
        print("nada foi alterado")
        return
    ok, msg = consultas.atualizar_status(codigo, novo)
    print(msg)


# tira a primeira da fila e coloca em andamento
def opcao_fila():
    if estruturas.fila_vazia():
        print("fila vazia, nenhuma ocorrência esperando")
        return
    print("fila:", ", ".join(estruturas.fila))
    codigo = estruturas.examinar_proxima()
    ok, msg = consultas.atualizar_status(codigo, "em_andamento")
    print("examinada " + msg)


# os ultimos eventos vem da pilha, do mais novo pro mais antigo
def opcao_historico():
    print("últimos eventos (mais recente primeiro):")
    for ev in estruturas.ver_ultimos(5):
        print(f"  dia {ev['dia']:>2} | {ev['codigo']} | {NOMES[ev['de']]} -> {NOMES[ev['para']]}")
    print(f"total de eventos: {estruturas.tamanho_pilha()}")


def opcao_bairros():
    hierarquia = estruturas.montar_hierarquia()
    for bairro in hierarquia:
        print(bairro)
        for cat in hierarquia[bairro]:
            print(f"  {NOMES[cat]}: {', '.join(hierarquia[bairro][cat])}")


def opcao_ajuda():
    print("o que significa cada status:")
    for st in STATUS:
        print(f"  {NOMES[st]}: {SIGNIFICADO[st]}")
    print("o status só anda pra frente: aberta -> em andamento -> concluída")
    print("os dados são fictícios e ficam só na memória, ao sair tudo volta ao início")


def menu():
    print("\n=== PAINEL DO BAIRRO ===")
    print("1 - listar ocorrências")
    print("2 - cadastrar ocorrência")
    print("3 - buscar por código")
    print("4 - filtrar por categoria e status")
    print("5 - atualizar status")
    print("6 - examinar próxima da fila")
    print("7 - ver histórico")
    print("8 - ver por bairro")
    print("9 - indicadores")
    print("10 - ajuda")
    print("0 - sair")


def main():
    carregar()
    while True:
        menu()
        op = ler("opção: ")
        if op == "1":
            mostrar(estruturas.ocorrencias)
        elif op == "2":
            opcao_cadastrar()
        elif op == "3":
            opcao_buscar()
        elif op == "4":
            opcao_filtrar()
        elif op == "5":
            opcao_atualizar()
        elif op == "6":
            opcao_fila()
        elif op == "7":
            opcao_historico()
        elif op == "8":
            opcao_bairros()
        elif op == "9":
            indicadores.mostrar_indicadores(estruturas.ocorrencias)
        elif op == "10":
            opcao_ajuda()
        elif op == "0":
            print("saindo...")
            break
        else:
            print("opção inválida")


if __name__ == "__main__":
    main()
