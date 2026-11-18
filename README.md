# Neighborhood Action Dashboard

Painel de ocorrências de bairro feito em Python, no terminal. Cadastra, consulta e acompanha problemas de iluminação, acessibilidade, limpeza e conservação, e mostra indicadores no final.

## Equipe

Grupo 1, turma 1CCON

- Gabriel Ferreira da Silva, RM574677
- José Kauan Medeiros Machado, RM
- Murilo Ribeiro Falconeri, RM
- Gustavo Rocha Caxias, RM

## Bairro, problema e público

Inventamos um bairro dividido em três partes: Vila Nova, Jardim Esperança e Parque das Árvores. A ideia veio de uma coisa comum: o morador reclama de um poste apagado ou de uma calçada quebrada e depois não sabe se alguém viu. Nosso sistema junta essas reclamações num lugar só, pra quem mora ali e pra associação do bairro acompanharem o que já foi resolvido e o que está parado.

## Como executar

Só precisa do Python 3, sem instalar nada. Na pasta do projeto:

```
python src/sistema.py
```

## Dados

As ocorrências ficam em `data/dados.csv` e o histórico de mudanças em `data/historico.csv`, os dois separados por `;`. Cada ocorrência tem código, bairro, local, categoria, descrição, status, dia de abertura e dia de conclusão. Só o dia de conclusão pode ficar vazio, e só quando a ocorrência não foi concluída.

São 17 linhas: 15 válidas e 2 com erro de propósito (OC16 sem categoria e OC17 com status "resolvido"), que o sistema recusa ao abrir. O histórico tem 15 eventos.

Status usados:

- aberta: registrada, ainda ninguém examinou
- em andamento: alguém já está cuidando
- concluída: problema resolvido

O status só anda para frente, de aberta para em andamento e depois para concluída.

## Estruturas de dados

- **Lista** (`ocorrencias`) com todas as ocorrências, usada para listar, filtrar e calcular os indicadores.
- **Dicionário** (`por_codigo`) indexado pelo código, para localizar uma ocorrência diretamente sem percorrer a lista.
- **Fila FIFO** (`fila`) com as demandas abertas e ainda não examinadas. `enfileirar()` adiciona no final e `examinar_proxima()` retira a primeira demanda registrada.
- **Pilha LIFO** (`pilha`) com os eventos de alteração de status. `empilhar_evento()` coloca um evento no topo e `ver_ultimos(n)` consulta os eventos mais recentes, do mais novo para o mais antigo.
- **Hierarquia** bairro → categoria → códigos das ocorrências, formada por dicionários dentro de dicionários para organizar os problemas de cada região.
- **Matriz** categoria × status, criada como uma lista de listas para contar as combinações de cada categoria com cada situação.

As estruturas ficam centralizadas em `src/estruturas.py`. A lista e o dicionário apoiam as buscas gerais, a fila representa a ordem de atendimento, a pilha preserva a consulta dos eventos recentes, a hierarquia organiza os registros por região e a matriz resume os indicadores do painel.

## Regras e validação

Uma ocorrência só entra se passar por esta regra, no `src/dados.py`:

```python
if oc["descricao"] == "" or oc["bairro"] == "" or oc["local"] == "":
    return False, "faltou descrição, bairro ou local"
elif oc["categoria"] not in CATEGORIAS:
    return False, "categoria inválida ou vazia"
elif not validar_status(oc["status"]):
    return False, "status desconhecido (" + oc["status"] + ")"
```

Basta um campo obrigatório vazio para o `or` dar verdadeiro e a ocorrência ser recusada. Por isso a OC16, que não tem categoria, cai no segundo teste, e a OC17 cai no terceiro porque "resolvido" não é um status da lista.

No filtro, `(categoria is None or oc["categoria"] == categoria) and (status is None or oc["status"] == status)` deixa o campo em branco valer como "todos". Na atualização, o sistema recusa status desconhecido e não deixa voltar de concluída.

## Indicadores

| Indicador | Fórmula | Resultado |
|---|---|---|
| Por categoria | categoria / total x 100 | 26,7% cada, conservação 20% |
| Por status | status / total x 100 | 40% abertas, 20% em andamento, 40% concluídas |
| Pendências | abertas + em andamento | 6 + 3 = 9 |
| Tempo médio de conclusão | soma dos dias / concluídas | 39 / 6 = 6,5 dias |

A opção 9 mostra a tabela completa com os dados de origem, a matriz e uma conclusão que muda conforme os números. Com os dados atuais, 60% das ocorrências ainda estão pendentes e acessibilidade é a categoria com mais pendências, o que afeta mais quem tem mobilidade reduzida.

## Exemplos

Cadastro:

```
bairro: Vila Nova
local (ex: praça, rua, escola): Praça central
categoria: 1
descrição: Poste piscando a noite toda
ocorrência OC18 cadastrada e colocada na fila
```

Consulta e filtro (iluminação abertas):

```
código (ex: OC03): OC03
OC03 | Limpeza        | Vila Nova          | Terreno baldio    | concluída

OC10 | Iluminação     | Parque das Árvores | Rua residencial   | aberta
OC18 | Iluminação     | Vila Nova          | Praça central     | aberta
```

Mudança de status e código que não existe:

```
OC18: aberta -> em andamento
ocorrência OC99 não encontrada
```

## Acessibilidade, inclusão e privacidade

Deixamos o menu só com números pra ninguém precisar decorar comando. No cadastro o sistema avisa pra não colocar nome, telefone ou endereço exato, e o local é sempre genérico, tipo praça ou rua. Todos os dados que usamos são inventados.

## Vídeo

Link:

## Conclusões, limitações e aprendizados

Pelos nossos dados, mais da metade das ocorrências ainda está pendente e acessibilidade foi o que mais acumulou, então seria por onde a gente começaria a cobrar.

O sistema tem limites que a gente sabe: os dados são inventados, tudo fica na memória e some quando o programa fecha, o tempo médio só conta as concluídas e não tem ligação com a prefeitura.

O que mais aprendemos foi escolher a estrutura certa pra cada coisa. A fila e a pilha, que na fase 2 pareciam só teoria, aqui fizeram sentido de verdade, e dividir o código em arquivos ajudou cada um a trabalhar na sua parte sem atrapalhar o outro.
