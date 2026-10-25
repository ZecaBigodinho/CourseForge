# 05 — Projeto do módulo: controle de notas da turma

> **Curso:** Pacote Office  
> **Módulo:** 02 — Excel  
> **Tempo estimado:** 2 h 30 min  

---

## Objetivos

Ao final deste projeto, você terá uma pasta de trabalho `controle_turma.xlsx` que:

- Guarda as notas e faltas da turma em uma **Tabela** do Excel.
- Calcula **média**, **frequência** e **situação** de cada aluno sozinha.
- Destaca os casos que pedem atenção com **formatação condicional**.
- Tem uma **ficha de consulta** com lista suspensa e um **painel** com tabela dinâmica e gráfico.
- Gera a **lista de aprovados** que alimenta os certificados da mala direta do Word.

## Pré-requisitos

- [Aulas 01 a 04](index.md) deste módulo.
- Para a última etapa: [Mala direta](../modulo_01_word/04_mala_direta.md), do Módulo 01 — Word.

---

## A estrutura da pasta de trabalho

| Planilha | O que tem |
|---|---|
| **Notas** | A Tabela `Notas` com os dados e as colunas calculadas |
| **Consulta** | A ficha de um aluno escolhido em uma lista suspensa |
| **Painel** | O resumo da turma: contagens, médias, tabela dinâmica e gráfico |
| **Certificados** | A lista de aprovados, pronta para a mala direta |

### As regras da escola

- **Média:** média simples dos quatro bimestres.
- **Frequência:** o ano teve **80 aulas**; frequência = 1 − faltas ÷ 80.
- **Aprovado:** média **6 ou mais** **e** no máximo **20 faltas** (75% de frequência).
- **Recuperação:** média **4 ou mais** **e** no máximo 20 faltas.
- **Reprovado:** todos os outros casos.

!!! info "Use as regras da sua escola"
    Se a sua escola usa média ponderada, outra nota mínima ou outra frequência, troque as regras — o projeto é o mesmo. Combine com o professor.

### Os dados

Copie e cole na célula **A1** da planilha **Notas** (ou use os dados da sua turma, com autorização do professor).

| Aluno | Turma | B1 | B2 | B3 | B4 | Faltas |
|---|---|---|---|---|---|---|
| Ana Souza | A | 8 | 7,5 | 9 | 8,5 | 4 |
| Bruno Lima | B | 5 | 6 | 4,5 | 5,5 | 10 |
| Carla Mendes | A | 9 | 9,5 | 10 | 9 | 0 |
| Diego Rocha | B | 6,5 | 7 | 6 | 7,5 | 6 |
| Elisa Prado | A | 7 | 6 | 5 | 6 | 22 |
| Felipe Costa | B | 8 | 8,5 | 7 | 9 | 3 |
| Gabriela Nunes | A | 4 | 5 | 6 | 4,5 | 12 |
| Henrique Alves | B | 3 | 4 | 2,5 | 3,5 | 15 |
| Isabela Torres | A | 6 | 5,5 | 6,5 | 6 | 8 |
| João Pereira | B | 7,5 | 6 | 8 | 7 | 18 |

!!! warning "Dados de alunos são dados pessoais"
    Notas e faltas de pessoas reais não devem circular por aí. Se usar os dados da sua turma, guarde o arquivo no OneDrive da escola e não compartilhe com quem não precisa.

---

## Passo a passo

### 1. Tabela e colunas calculadas (aulas 01 a 03)

- Transforme os dados em uma Tabela chamada **`Notas`** (`Ctrl + Alt + T`; *Design da Tabela ➔ Nome da Tabela*).
- Crie as colunas **Média**, **Frequência** e **Situação** digitando o título na primeira coluna vazia — a tabela cresce sozinha. As fórmulas usam `[@B1]`, `[@Faltas]`...
- Formatos: Média com **uma casa decimal**; Frequência em **%**.
- **Congele** o cabeçalho: *Exibir ➔ Congelar Painéis ➔ Congelar Linha Superior*.

### 2. Destaques (aula 03)

- **Situação:** *Regras de Realce das Células ➔ Texto que Contém* — *Aprovado* em verde, *Recuperação* em amarelo, *Reprovado* em vermelho.
- **Frequência abaixo de 75%** em vermelho.
- **Notas dos bimestres:** uma **escala de cores** ajuda a ver quem caiu ao longo do ano.

### 3. Ficha de consulta (aulas 02 e 03)

- Na planilha **Consulta**, uma célula com **lista suspensa** dos nomes dos alunos.
- Ao lado, com `PROCX`, a turma, a média, a frequência e a situação do aluno escolhido.

### 4. Painel (aulas 02 a 04)

- Quantos alunos em cada situação (`CONT.SE`) e a média de cada turma (`MÉDIASE`).
- Uma **tabela dinâmica** com a contagem de alunos por *Turma* e *Situação* e um **gráfico** com título que diz a conclusão.

### 5. Lista para os certificados (aula 04 + Word)

- Na planilha **Certificados**, a lista de aprovados com `FILTRO`.
- Copiada como **valores** para um arquivo `participantes.xlsx`, no formato que a mala direta do Word espera (`Nome`, `Curso`, `Carga`, `Data`).

---

## ✅ Checklist de entrega

- [ ] Os dados estão em uma **Tabela** chamada `Notas`, sem linhas vazias.
- [ ] Média, Frequência e Situação são **fórmulas** — mudar uma nota muda a situação na hora.
- [ ] As regras de aprovação estão certas também nos **casos de limite** (média exatamente 6; faltas exatamente 20).
- [ ] Formatação condicional nas situações e na frequência.
- [ ] A ficha de consulta funciona escolhendo **qualquer** aluno da lista.
- [ ] O painel mostra as contagens, as médias por turma, a tabela dinâmica **atualizada** e um gráfico com título.
- [ ] A lista de aprovados vem do `FILTRO` (não foi digitada à mão).
- [ ] `participantes.xlsx` está no formato da mala direta e os certificados foram gerados no Word.

---

## Exercícios

O projeto tem três entregas, uma por nível. Faça na ordem.

### Básico (fixação)

Monte a planilha **Notas**: a Tabela `Notas` com as colunas **Média**, **Frequência** e **Situação** calculadas, nos formatos certos, com o cabeçalho congelado e a formatação condicional das situações e da frequência.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Fórmulas na primeira linha de cada coluna (a tabela copia para as outras):

    - **Média:** `=MÉDIA(Notas[@[B1]:[B4]])` — ou clique de C2 até F2 enquanto escreve `=MÉDIA(`. Formato com uma casa decimal.
    - **Frequência:** `=1-[@Faltas]/80` ➔ formato **%**.
    - **Situação:** `=SES(E([@Média]>=6;[@Faltas]<=20);"Aprovado";E([@Média]>=4;[@Faltas]<=20);"Recuperação";VERDADEIRO;"Reprovado")`

    **Confira:**

    | Aluno | Média | Frequência | Situação |
    |---|---|---|---|
    | Ana Souza | 8,3 | 95% | Aprovado |
    | Bruno Lima | 5,3 | 88% | Recuperação |
    | Carla Mendes | 9,4 | 100% | Aprovado |
    | Diego Rocha | 6,8 | 93% | Aprovado |
    | Elisa Prado | 6,0 | 73% | **Reprovado** (22 faltas) |
    | Felipe Costa | 8,1 | 96% | Aprovado |
    | Gabriela Nunes | 4,9 | 85% | Recuperação |
    | Henrique Alves | 3,3 | 81% | Reprovado |
    | Isabela Torres | 6,0 | 90% | **Aprovado** (média exatamente 6) |
    | João Pereira | 7,1 | 78% | Aprovado |

    Total: **6 aprovados, 2 em recuperação, 2 reprovados**. Se a Isabela aparecer em *Recuperação*, o teste está com `>` no lugar de `>=`.

    As médias aparecem arredondadas pelo formato (Ana tem 8,25 de verdade). A frequência com casas decimais mostra Bruno com 87,5%, Diego com 92,5%...

### Intermediário (aplicação)

Monte a planilha **Consulta** — lista suspensa com os nomes em **B1** e a turma, a média, a frequência e a situação do aluno escolhido em **B2:B5** — e a parte de **fórmulas do Painel**: quantos alunos em cada situação e a média de cada turma.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    **Consulta:**

    1. Em A1:A5, os rótulos `Aluno`, `Turma`, `Média`, `Frequência`, `Situação`.
    2. **B1:** *Dados ➔ Validação de Dados ➔ Lista* ➔ em *Fonte*, clique na planilha **Notas** e selecione **A2:A11** (o Excel escreve `=Notas!$A$2:$A$11`).
    3. **B2:** `=PROCX($B$1;Notas[Aluno];Notas[Turma];"Escolha um aluno")`. Para B3, B4 e B5, troque `Notas[Turma]` por `Notas[Média]`, `Notas[Frequência]` e `Notas[Situação]`, e aplique os formatos de número.

    **Teste:** escolha *Elisa Prado* ➔ A · 6,0 · 73% · Reprovado.

    **Painel:**

    - `=CONT.SE(Notas[Situação];"Aprovado")` ➔ **6** · *Recuperação* ➔ **2** · *Reprovado* ➔ **2**
    - `=MÉDIASE(Notas[Turma];"A";Notas[Média])` ➔ **6,9** · turma B ➔ **6,1** · média geral `=MÉDIA(Notas[Média])` ➔ **6,5**

### Avançado (desafio)

1. Complete o **Painel** com uma tabela dinâmica que conte os alunos por *Turma* (linhas) e *Situação* (colunas), e um gráfico de colunas com um título que diga a conclusão.
2. Monte a planilha **Certificados** com a lista de aprovados gerada por fórmula. Leve a lista para um arquivo `participantes.xlsx` com as colunas `Nome`, `Curso` (*Pacote Office*), `Carga` e `Data` e gere os certificados com a **mala direta** do Word.
3. Prove que tudo está ligado: mude a nota do B4 do **Bruno Lima** para **9** e veja o que muda em cada planilha.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Clique na Tabela `Notas` ➔ *Inserir ➔ Tabela Dinâmica* ➔ **Planilha Existente** ➔ uma célula do Painel. **Turma** em *Linhas*, **Situação** em *Colunas*, **Aluno** em *Valores* (vira *Contagem de Aluno*). Resultado: turma **A** = 3 aprovados, 1 recuperação, 1 reprovado; turma **B** = o mesmo (3, 1, 1). Gráfico: *Análise da Tabela Dinâmica ➔ Gráfico Dinâmico ➔ Colunas*. Título, por exemplo: “As duas turmas tiveram 3 aprovados em 5”.
    2. Em **Certificados**, A1 `Nome` e em **A2**: `=FILTRO(Notas[Aluno];Notas[Situação]="Aprovado";"Nenhum aprovado")` ➔ Ana Souza, Carla Mendes, Diego Rocha, Felipe Costa, Isabela Torres e João Pereira.
        - Selecione os nomes ➔ `Ctrl + C` ➔ em um arquivo novo, A2 ➔ *Colar* ➔ **Colar Valores** (a mala direta precisa dos nomes, não da fórmula).
        - Cabeçalhos em A1:D1: `Nome`, `Curso`, `Carga`, `Data`; preencha *Pacote Office*, a carga horária e a data em todas as linhas. Salve como `participantes.xlsx` e **feche**.
        - No Word, siga o exercício básico da [aula de mala direta](../modulo_01_word/04_mala_direta.md) ➔ **6 certificados**.
    3. Com B4 = 9, a média do Bruno vai de 5,25 para **6,1** ➔ ele passa a *Aprovado* na Tabela e na Consulta; o Painel mostra **7** aprovados e **1** em recuperação; a lista do `FILTRO` ganha o Bruno. A **tabela dinâmica só muda depois de *Atualizar*** (botão direito ➔ *Atualizar*). E `participantes.xlsx` **não muda**, porque recebeu valores colados — para incluir o Bruno, copie a lista de novo.

    **Critérios que o professor costuma olhar:** nenhuma conta digitada à mão; regras certas nos casos de limite; planilhas com nomes claros; painel legível; lista de certificados batendo com as situações.

---

## 💡 Resumo do módulo

Você saiu da célula vazia para uma planilha que faz as contas, decide e se atualiza sozinha:

- **Fórmulas** com referências relativas e absolutas.
- **Funções** que decidem (`SE`, `SES`), contam e somam com condição (`CONT.SE`, `SOMASE`) e buscam (`PROCX`).
- **Tabelas**, **formatação condicional**, **listas suspensas** e **gráficos** que comunicam.
- **Tabela dinâmica** e **funções de matriz dinâmica** para resumir e filtrar.
- **Macros** para repetir tarefas — e o cuidado com as que vêm de fora.
- A planilha trabalhando junto com o **Word** na mala direta.

## ➡️ Próximo passo

**[Módulo 03 — PowerPoint](../modulo_03_powerpoint/index.md)**: transformar os números do seu painel em uma apresentação clara.
