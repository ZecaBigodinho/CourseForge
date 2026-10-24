# 03 — Planilhas e dados com IA

> **Curso:** Introdução à IA  
> **Módulo:** 03 — IA no estudo e no trabalho  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Pedir **fórmulas** de planilha dando as informações certas (idioma, colunas, exemplo).
- Pedir a **explicação** de uma fórmula pronta e a **causa** de um erro (`#N/D`, `#VALOR!`...).
- Usar a IA para **limpar** e organizar dados.
- Pedir uma **análise** de uma planilha — e **conferir** os números.
- Proteger **dados pessoais** ao trabalhar com planilhas.

## Pré-requisitos

- [Aula 02](02_escrever_e_comunicar.md) (anonimizar).
- Recomendado: [Módulo 02 do curso de Pacote Office](../../pacote_office/modulo_02_excel/index.md) (Excel). As fórmulas aqui seguem o **Excel em português**.

---

## Pedindo uma fórmula

A IA não vê a sua planilha (a não ser que você anexe). Diga **tudo** o que ela precisa saber:

| Informação | Exemplo |
|---|---|
| **Programa e idioma** | “Excel em português” (as funções mudam de nome: `SOMASE` × `SUMIF`) |
| **Separador** | “Use ponto e vírgula” |
| **Onde estão os dados** | “Categorias em B2:B13, valores em D2:D13” |
| **O que você quer** | “O total gasto com Alimentação” |
| **Um exemplo** | “Para Transporte, deve dar 118,70” |

```text
Excel em português, separador ponto e vírgula. Tenho categorias em B2:B13 e valores em D2:D13.
Quero, em uma célula, o total gasto com "Alimentação". Explique a fórmula em uma linha.
```

!!! tip "Teste com um valor que você sabe"
    Antes de confiar na fórmula, **teste** com um caso cuja resposta você conhece (some à mão duas ou três linhas, ou filtre a tabela). A IA pode errar o intervalo, a ordem dos argumentos ou o nome da função.

---

## Explicar e consertar

- **Fórmula pronta que ninguém entende:** cole a fórmula e peça “Explique esta fórmula do Excel parte por parte, em linguagem simples”.
- **Erro na célula:** diga o erro e a fórmula: “A fórmula `=PROCX(H2;A2:A9;B2:B9)` está dando `#N/D`. O que pode ser?” A resposta costuma listar as causas prováveis (o nome não existe, tem espaço sobrando...) — confira uma por uma.

---

## Limpar e organizar dados

| Problema | Pedido |
|---|---|
| Nomes escritos de jeitos diferentes (“alimentação”, “Alimentacao”, “ALIMENTAÇÃO”) | “Sugira uma forma de padronizar esta coluna” (ou use a lista suspensa do Excel) |
| Nome e sobrenome juntos | “Fórmula para separar o primeiro nome” — ou o **Preenchimento Relâmpago** do Excel |
| Datas em formatos misturados | “Como converter textos como 05.11.2026 em datas?” |
| Tabela colada de um PDF, toda torta | Cole o texto e peça “Organize em uma tabela com as colunas X, Y, Z” — e confira linha por linha |

---

## Analisar uma planilha

Muitos assistentes aceitam **anexar** uma planilha (`.xlsx` ou `.csv`) e respondem perguntas sobre ela: totais, médias, maiores valores, tendências e até gráficos. Por trás, alguns escrevem e rodam um pequeno programa para fazer as contas — o que ajuda, mas **não** garante o acerto: a IA pode ler a coluna errada ou ignorar linhas.

!!! warning "Confira os números no próprio Excel"
    Para cada número que for usado (em um relatório, uma decisão, um trabalho), confira na planilha com `SOMA`, `SOMASE`, filtro ou tabela dinâmica. Se a IA e o Excel discordarem, **o Excel** é a referência — e vale descobrir por que a IA errou.

### Assistentes dentro da planilha

O **Copilot no Excel** e o **Gemini no Google Planilhas** trabalham direto na planilha aberta (criam fórmulas, colunas, gráficos), **quando a licença inclui** esses recursos. As regras são as mesmas: diga o que quer com clareza e **confira**.

---

## Dados pessoais em planilhas

Planilhas de notas, de clientes, de funcionários ou de pacientes têm **dados pessoais**. Antes de anexar ou colar:

- Use a **conta institucional**, se a empresa ou a escola autorizar o uso.
- Ou **anonimize**: troque nomes por códigos (Aluno 1, Cliente 2), apague colunas de CPF, telefone e endereço.
- Ou use uma **amostra inventada** com a mesma estrutura só para descobrir a fórmula — e aplique a fórmula na planilha real, no seu computador.

---

??? note "Equivalentes e alternativas"
    | Tarefa | Excel | Google Planilhas | LibreOffice Calc |
    |---|---|---|---|
    | Fórmula pedida à IA | Funções em português, `;` | Peça “Google Planilhas” — alguns nomes são em inglês (`XLOOKUP`, `IFS`) | Peça “LibreOffice Calc em português” |
    | IA dentro da planilha | Copilot (com licença) | Gemini (com licença) | Não tem nativa |
    | Conferir números | `SOMASE`, filtro, tabela dinâmica | Os mesmos | Os mesmos |

---

## ⚠️ Erros comuns

- **Não dizer o idioma do Excel:** a fórmula vem em inglês e dá `#NOME?`.
- **Não dizer onde estão os dados:** a fórmula vem com intervalos inventados.
- **Usar a análise da IA sem conferir** no próprio Excel.
- **Anexar a planilha de notas da turma** em uma conta pessoal.
- **Copiar uma fórmula que você não entende.** Peça a explicação — senão você não consegue consertar quando der erro.

---

## Exercícios

Use a planilha de gastos do [Módulo 02 do curso de Office, aula 03](../../pacote_office/modulo_02_excel/03_tabelas_graficos_e_formatacao.md) (12 gastos de março, com Data em A, Categoria em B, Descrição em C e Valor em D, linhas 2 a 13).

### Básico (fixação)

Peça à IA, com todas as informações da tabela da aula, as fórmulas para: (1) o **total gasto com Alimentação**; (2) a **média** de todos os gastos. Teste as fórmulas no Excel.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. `=SOMASE(B2:B13;"Alimentação";D2:D13)` ➔ **R$ 172,00** (12,50 + 85,40 + 9,80 + 64,30).
    2. `=MÉDIA(D2:D13)` ➔ **R$ 34,43** (o valor guardado é 34,425; total de R$ 413,10 ÷ 12).

    **Teste:** filtre a categoria Alimentação e olhe a **Soma** na barra de status — tem que dar 172,00. Se a IA respondeu com `SUMIF` ou com vírgulas, faltou dizer “Excel em português, ponto e vírgula” no prompt.

### Intermediário (aplicação)

1. Peça à IA para **explicar parte por parte** a fórmula abaixo (do curso de Office) e confira se a explicação bate com as regras da escola descritas lá:

    ```text
    =SES(E(F2>=6;E2<=10);"Aprovado";E(F2>=4;E2<=10);"Recuperação";VERDADEIRO;"Reprovado")
    ```

2. Peça uma fórmula para **contar quantos gastos passaram de R$ 50,00** e teste.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Explicação esperada: `SES` testa em ordem. **Primeiro teste:** média (F2) maior ou igual a 6 **e** faltas (E2) até 10 ➔ “Aprovado”. **Segundo:** média maior ou igual a 4 **e** faltas até 10 ➔ “Recuperação”. **`VERDADEIRO`** pega todos os outros casos ➔ “Reprovado” (média abaixo de 4 **ou** mais de 10 faltas). Se a explicação disse que quem tem 12 faltas e média 7 fica em “Recuperação”, ela está **errada**: com mais de 10 faltas, a pessoa não passa nos dois primeiros testes e cai em “Reprovado”.
    2. `=CONT.SE(D2:D13;">50")` ➔ **2** (R$ 85,40 e R$ 64,30). Os R$ 50,00 da recarga **não** contam, porque não são **maiores** que 50 — se a IA usou `">=50"`, o resultado seria 4.

### Avançado (desafio)

Monte uma cópia **sem dados pessoais** da planilha de gastos, **anexe** a um assistente que aceite planilhas e pergunte: (a) qual categoria teve o maior gasto; (b) quanto ela representa do total, em %; (c) qual foi o maior gasto único. **Confira** cada resposta no Excel e registre se a IA acertou.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    | Pergunta | Resposta certa | Como conferir no Excel |
    |---|---|---|
    | (a) Maior categoria | **Alimentação**, R$ 172,00 | `SOMASE` por categoria ou tabela dinâmica (Transporte 118,70 · Lazer 84,90 · Material escolar 37,50) |
    | (b) % do total | **41,6%** (172,00 ÷ 413,10) | `=172/413,1` ou a tabela dinâmica com *% do Total Geral* |
    | (c) Maior gasto único | **Mercado, R$ 85,40** (07/03) | `=MÁXIMO(D2:D13)` ou classificar do maior para o menor |

    **Registro:** para cada resposta, “acertou” ou “errou” e, se errou, o motivo provável (leu a coluna errada, somou o cabeçalho, esqueceu linhas). Se o assistente não aceitar anexos no plano gratuito, cole a tabela como texto — ou faça em dupla com quem tem o recurso.

---

## 💡 Resumo

- Para pedir fórmulas: **programa e idioma**, **separador**, **onde estão os dados**, **o que quer** e **um exemplo**.
- Peça **explicações** de fórmulas e **causas** de erros — e entenda antes de usar.
- A IA ajuda a **limpar** dados e a **analisar** planilhas, mas **o Excel é a referência**: confira os números.
- Dados pessoais: **conta institucional**, **anonimização** ou **amostra inventada**.

## ➡️ Próximo passo

**[04 — Código e imagens com IA](04_codigo_e_imagens.md)**: entender e consertar programas e criar imagens — com testes e cuidados de autoria.
