# 03 — Tabelas, gráficos e formatação condicional

> **Curso:** Pacote Office  
> **Módulo:** 02 — Excel  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Transformar um intervalo em **Tabela** do Excel — com filtros, linha de totais e fórmulas que se copiam sozinhas.
- **Classificar** e **filtrar** dados sem estragar a planilha.
- Destacar valores com **formatação condicional** (regras, barras de dados e regras por fórmula).
- Criar uma **lista suspensa** com validação de dados.
- Escolher o **gráfico** certo para cada pergunta e deixá-lo legível.

## Pré-requisitos

- [Aula 02](02_funcoes_essenciais.md): `SOMASE` e comparadores (`>`, `<=`...).

---

## A planilha desta aula

Copie e cole na célula **A1** de uma planilha nova. São os gastos de um estudante em março.

| Data | Categoria | Descrição | Valor |
|---|---|---|---|
| 01/03/2026 | Transporte | Recarga do cartão | 50,00 |
| 02/03/2026 | Alimentação | Lanche | 12,50 |
| 03/03/2026 | Material escolar | Caderno | 22,90 |
| 05/03/2026 | Lazer | Cinema | 28,00 |
| 07/03/2026 | Alimentação | Mercado | 85,40 |
| 09/03/2026 | Transporte | Recarga do cartão | 50,00 |
| 12/03/2026 | Alimentação | Lanche | 9,80 |
| 15/03/2026 | Lazer | Streaming | 21,90 |
| 18/03/2026 | Material escolar | Canetas | 14,60 |
| 21/03/2026 | Alimentação | Mercado | 64,30 |
| 25/03/2026 | Transporte | Aplicativo de transporte | 18,70 |
| 28/03/2026 | Lazer | Lanchonete com amigos | 35,00 |

!!! tip "Regras de ouro para dados organizados"
    Uma linha por registro, uma coluna por informação, **cabeçalho em uma única linha** e **nenhuma linha ou coluna em branco** no meio. Toda ferramenta desta aula — tabela, filtro, gráfico e, na próxima, a tabela dinâmica — depende disso.

---

## Tabela do Excel

Clique em qualquer célula dos dados e use *Inserir* ➔ **Tabela** (ou `Ctrl + Alt + T`). Confirme que **Minha tabela tem cabeçalhos** está marcado.

O que você ganha:

- **Filtros** nos cabeçalhos e **linhas listradas**, que facilitam a leitura.
- A tabela **cresce sozinha**: digite na primeira linha abaixo dela e a linha nova já entra na tabela — com a formatação e as fórmulas.
- **Colunas calculadas:** escreva uma fórmula na primeira célula de uma coluna nova e ela é copiada para a coluna inteira.
- **Nome da tabela:** na guia *Design da Tabela*, troque `Tabela1` por um nome claro, como `Gastos`. As fórmulas passam a usar **referências estruturadas**: `=SOMA(Gastos[Valor])` em vez de `=SOMA(D2:D13)` — e continuam certas quando a tabela cresce.
- **Linha de Totais:** *Design da Tabela* ➔ **Linha de Totais**. Na última linha, cada célula tem uma setinha para escolher *Soma*, *Média*, *Contagem*...

!!! info "Dentro da tabela, `[@Valor]` quer dizer “o valor desta linha”"
    Ao clicar em células da mesma linha enquanto escreve uma fórmula na tabela, o Excel escreve `[@Valor]` em vez de `D2`. É o mesmo que a referência relativa da aula 01, só que com nome.

---

## Classificar e filtrar

- **Classificar:** setinha do cabeçalho ➔ *Classificar do Maior para o Menor* (ou de A a Z). A linha inteira vai junto — por isso é seguro dentro de uma tabela.
- **Filtrar:** setinha do cabeçalho ➔ desmarque o que não quer ver. As linhas não somem: ficam **ocultas**, e os números das linhas ficam azuis para avisar.
- **Limpar:** setinha ➔ *Limpar Filtro*, ou *Dados ➔ Limpar*.

!!! tip "A Linha de Totais respeita o filtro"
    Com a tabela filtrada, a Linha de Totais soma **só as linhas visíveis** (ela usa a função `SUBTOTAL`). Um `=SOMA(...)` comum, fora da tabela, continua somando tudo.

!!! warning "Nunca classifique uma coluna sozinha"
    Fora de uma tabela, se você selecionar **só** a coluna D e classificar, os valores trocam de lugar e as descrições não — os dados ficam embaralhados. Se o Excel perguntar, escolha **Expandir a seleção**.

---

## Formatação condicional

*Página Inicial* ➔ **Formatação Condicional**: a cor da célula muda conforme o valor — e se atualiza sozinha.

| Opção | Para quê | Exemplo |
|---|---|---|
| **Realçar Regras das Células** | destacar o que passa de um limite | gastos *É Maior do que* 50 em vermelho |
| **Regras de Primeiros/Últimos** | os maiores ou menores | os 3 maiores gastos |
| **Barras de Dados** | comparar tamanhos dentro da célula | uma barrinha proporcional ao valor |
| **Escalas de Cor** | do menor ao maior em degradê | notas do vermelho ao verde |
| **Nova Regra ➔ Usar uma fórmula...** | regras que dependem de outra célula | destacar a linha inteira |

Para ver, editar ou apagar regras: *Formatação Condicional* ➔ **Gerenciar Regras**.

!!! tip "Regra por fórmula"
    Selecione o intervalo **a partir da primeira linha** e escreva a fórmula pensando nessa linha, com `$` na coluna: `=$D2>50` aplicada em `A2:D13` pinta a **linha inteira** de cada gasto acima de 50. Fórmula verdadeira = célula formatada.

---

## Lista suspensa: validação de dados

Para ninguém digitar “Alimentaçao” ou “alimentação” e bagunçar as somas:

1. Selecione as células da coluna *Categoria*.
2. *Dados* ➔ **Validação de Dados** ➔ *Permitir:* **Lista**.
3. Em *Fonte*, escreva as opções separadas por ponto e vírgula: `Alimentação;Transporte;Lazer;Material escolar` — ou aponte para um intervalo que tenha a lista.
4. Na guia *Alerta de Erro*, escreva uma mensagem clara (“Escolha uma categoria da lista”).

Agora a célula mostra uma setinha com as opções, e o Excel recusa o que não estiver na lista.

---

## Gráficos

Selecione os dados (com os cabeçalhos) e use *Inserir* ➔ **Gráficos Recomendados**. Antes de escolher, pergunte: **o que o gráfico precisa responder?**

| Pergunta | Gráfico |
|---|---|
| Quem é maior? Comparar categorias | **Colunas** ou **Barras** (barras para nomes longos) |
| Como mudou ao longo do tempo? | **Linhas** |
| Quanto cada parte representa do todo? | **Pizza** ou **Rosca** — só com poucas fatias (até 5 ou 6) |
| Uma coisa depende da outra? | **Dispersão** (por exemplo, faltas × média) |

Com o gráfico selecionado, o botão **+** (*Elementos do Gráfico*) liga e desliga título, rótulos de dados, legenda e eixos. O pincel muda o estilo e as cores.

!!! tip "Gráfico bom é gráfico simples"
    Um **título que diz a conclusão** (“Alimentação foi o maior gasto de março”), **rótulos de dados** no lugar das linhas de grade e nada de 3D. Se for preciso explicar o gráfico, ele está complicado demais.

---

??? note "Equivalentes gratuitos: LibreOffice Calc e Google Planilhas"
    | Tarefa | LibreOffice Calc | Google Planilhas |
    |---|---|---|
    | Tabela com filtros | *Dados ➔ AutoFiltro* (ou *Formatar como tabela*, nas versões recentes) | *Formatar ➔ Converter em tabela* |
    | Classificar | *Dados ➔ Classificar* | *Dados ➔ Classificar intervalo* |
    | Formatação condicional | *Formatar ➔ Condicional ➔ Condição* | *Formatar ➔ Formatação condicional* |
    | Lista suspensa | *Dados ➔ Validade ➔ Permitir: Intervalo de células / Lista* | *Inserir ➔ Menu suspenso* |
    | Gráfico | *Inserir ➔ Gráfico* | *Inserir ➔ Gráfico* (o painel *Editor de gráficos* abre ao lado) |

---

## ⚠️ Erros comuns

- **Linha em branco no meio dos dados.** O filtro, a classificação e a tabela param nela. Apague as linhas vazias antes.
- **Título em duas linhas** (“Valor” em cima, “(R$)” embaixo). Use uma linha só: `Valor (R$)`.
- **Pizza com 12 fatias.** Ninguém consegue comparar. Use barras — ou agrupe as menores em “Outros”.
- **Esquecer que o filtro está ligado.** Os números das linhas em azul avisam: tem coisa escondida.

---

## Exercícios

Use a planilha de gastos desta aula.

### Básico (fixação)

1. Transforme os dados em uma **Tabela** chamada `Gastos` e formate a coluna *Valor* como **Moeda**.
2. Ligue a **Linha de Totais** com a soma dos valores.
3. Classifique do **maior** para o **menor** valor.
4. Filtre só a categoria **Alimentação** e veja o que acontece com o total. Depois, limpe o filtro.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Clique em qualquer célula dos dados ➔ `Ctrl + Alt + T` ➔ *OK*. Em *Design da Tabela ➔ Nome da Tabela*, digite `Gastos` e `Enter`. Selecione a coluna D ➔ *Moeda*.
    2. *Design da Tabela ➔ Linha de Totais*. Se a última célula mostrar outra função, clique na setinha e escolha **Soma** ➔ **R$ 413,10**.
    3. Setinha de *Valor* ➔ *Classificar do Maior para o Menor*. Os primeiros são: Mercado (R$ 85,40), Mercado (R$ 64,30) e Recarga do cartão (R$ 50,00).
    4. Setinha de *Categoria* ➔ deixe marcada só **Alimentação**. O total passa a **R$ 172,00** — a Linha de Totais soma só o que está visível. Setinha ➔ *Limpar Filtro*.

### Intermediário (aplicação)

1. Pinte de **vermelho claro** os gastos **acima de R$ 50,00**.
2. Coloque **barras de dados** na coluna *Valor*.
3. Crie uma **lista suspensa** na coluna *Categoria* com as quatro categorias. Teste digitando `Lazr` em uma linha nova.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Selecione os valores (**D2:D13**) ➔ *Formatação Condicional ➔ Realçar Regras das Células ➔ É Maior do que...* ➔ `50` ➔ *Preenchimento Vermelho Claro*. Ficam vermelhos **2** valores: R$ 85,40 e R$ 64,30 (R$ 50,00 não é *maior* que 50).
    2. Com D2:D13 selecionado: *Formatação Condicional ➔ Barras de Dados* ➔ escolha uma cor. A mesma célula pode ter as duas regras.
    3. Selecione **B2:B13** ➔ *Dados ➔ Validação de Dados* ➔ *Permitir:* **Lista** ➔ *Fonte:* `Alimentação;Transporte;Lazer;Material escolar` ➔ *Alerta de Erro*: “Escolha uma categoria da lista” ➔ *OK*.

    **Teste:** na linha 14 (logo abaixo da tabela), digite uma data e, na categoria, `Lazr`. O Excel recusa e mostra a sua mensagem. Escolha **Lazer** pela setinha. Como a tabela cresceu, a validação e as formatações valem para a linha nova.

### Avançado (desafio)

1. Ao lado da tabela, monte um **resumo por categoria**: em **F1:H1** os títulos `Categoria`, `Gasto` e `Orçamento`; em F2:F5 as quatro categorias; em **G** o total gasto em cada uma, com fórmula que use a tabela `Gastos`; em **H** o orçamento: Alimentação 150, Transporte 120, Lazer 80, Material escolar 50.
2. Com **uma regra por fórmula**, pinte a **linha inteira do resumo** (F a H) das categorias que **estouraram** o orçamento.
3. Crie um gráfico de **colunas agrupadas** comparando *Gasto* e *Orçamento*, com um título que diga a conclusão.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. **G2:** `=SOMASE(Gastos[Categoria];F2;Gastos[Valor])` ➔ copie até G5. Resultados: Alimentação **R$ 172,00** · Transporte **R$ 118,70** · Lazer **R$ 84,90** · Material escolar **R$ 37,50** (soma: R$ 413,10, igual à Linha de Totais).
    2. Selecione **F2:H5** ➔ *Formatação Condicional ➔ Nova Regra ➔ Usar uma fórmula para determinar quais células devem ser formatadas* ➔ `=$G2>$H2` ➔ *Formatar* ➔ preenchimento laranja. Ficam pintadas **Alimentação** (R$ 22,00 acima) e **Lazer** (R$ 4,90 acima).
    3. Selecione **F1:H5** ➔ *Inserir ➔ Gráficos Recomendados* ➔ **Colunas Agrupadas**. Título: “Alimentação e Lazer passaram do orçamento”. Pelo **+**, ligue os *Rótulos de Dados*.

    **Por que `$G2` e não `G2`:** a regra é aplicada também às colunas F e H. O `$` trava a coluna, então todas as células da linha olham para o mesmo G e H — e a linha inteira é pintada junto.

---

## 💡 Resumo

- Dados organizados: uma linha por registro, cabeçalho único, nada em branco no meio.
- **Tabela** (`Ctrl + Alt + T`): filtros, crescimento automático, colunas calculadas, Linha de Totais e referências como `Gastos[Valor]`.
- **Formatação condicional** destaca sozinha; regra por fórmula com `$` pinta linhas inteiras.
- **Validação de dados** evita digitação errada com listas suspensas.
- Escolha o gráfico pela pergunta; título com a conclusão; nada de 3D.

## ➡️ Próximo passo

**[04 — Tabela dinâmica, funções modernas e automação](04_tabela_dinamica_e_automacao.md)**: resumir centenas de linhas em segundos, criar listas que se atualizam sozinhas e gravar sua primeira macro.
