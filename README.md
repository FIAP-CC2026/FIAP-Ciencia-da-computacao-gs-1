# Neighborhood Action Dashboard

Painel de ocorrências de bairro feito em Python, no terminal. Cadastra, consulta e acompanha problemas de iluminação, acessibilidade, limpeza e conservação, e mostra indicadores no final.

## Equipe

Grupo 1, turma 1CCON

- Gabriel Ferreira da Silva, RM574677
- José Kauan Medeiros Machado, RM574820
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

As ocorrências ficam em `data/dados.csv` e o histórico de mudanças em `data/historico.csv`, os dois separados por `;`. Cada ocorrência tem código, bairro, local, categoria, descrição, status, dia de abertura e dia de conclusão. Todos os campos são obrigatórios, exceto o dia de conclusão, que só é obrigatório (e só pode existir) quando a ocorrência está concluída. Os dias são números simulados (dia 1, dia 2...) e o "hoje" do sistema é o dia 30. Os arquivos são lidos sem biblioteca, linha a linha: a primeira linha é o cabeçalho, cada valor é separado por `;`, espaços nas pontas são ignorados e uma linha curta é completada com campos vazios (que a validação depois recusa).

São 17 linhas: 15 válidas e 2 com erro de propósito (OC16 sem categoria e OC17 com status "resolvido"), que o sistema recusa ao abrir. Todas as 4 categorias e os 3 status aparecem nas linhas válidas. O histórico tem 15 eventos, no formato `codigo;dia;de;para`, e passa pela mesma ideia de validação (veja abaixo).

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

Uma ocorrência só entra se passar por `validar_ocorrencia`, no `src/dados.py`. A expressão completa é:

```
VALIDA = NOT faltou_texto AND categoria_ok AND status_ok AND abertura_ok
         AND NOT (concluida AND sem_conclusao)
         AND NOT (NOT concluida AND tem_conclusao)
         AND NOT (concluida AND conclusao < abertura)
```

onde `faltou_texto = descrição vazia OR bairro vazio OR local vazio`, `abertura_ok` quer dizer dia de abertura numérico e não maior que o dia atual, e `concluida` quer dizer status igual a "concluida". No código isso vira uma cadeia de `if/elif`, e o primeiro teste que falha define a mensagem:

| Teste (em ordem) | Mensagem | Por que dá essa mensagem |
|---|---|---|
| `descricao == "" or bairro == "" or local == ""` | faltou descrição, bairro ou local | o `or` dá verdadeiro se qualquer um dos três estiver vazio |
| `categoria not in CATEGORIAS` | categoria inválida ou vazia | vazia ou fora das 4 categorias |
| `not validar_status(status)` | status desconhecido (...) | o `not` inverte: recusa o que não está na lista de status |
| `abertura is None or abertura > DIA_ATUAL` | dia de abertura inválido | não é número ou é um dia que ainda não chegou |
| `concluida and conclusao is None` | concluída sem dia de conclusão | só dispara quando as duas coisas são verdade ao mesmo tempo |
| `not concluida and conclusao is not None` | tem dia de conclusão mas não está concluída | o contrário do teste anterior |
| `concluida and conclusao < abertura` | concluída antes de ser aberta | datas incoerentes |

Se nenhum teste falha, a resposta é `(True, "ok")`. Por isso a OC16, sem categoria, para no segundo teste, e a OC17 para no terceiro porque "resolvido" não é um status da lista. Depois de validar, o carregamento ainda recusa código vazio e código repetido (a segunda ocorrência com o mesmo código é ignorada).

O histórico usa `validar_evento`: o evento só vale se o código existe, os dois status existem (`validar_status(de) and validar_status(para)`), o dia é válido e o status anda para frente (`STATUS.index(para) > STATUS.index(de)`). Eventos recusados aparecem como aviso ao abrir o programa, igual às ocorrências.

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
