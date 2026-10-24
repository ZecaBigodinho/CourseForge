# 02 — Planilha de candidaturas

> **Curso:** Pacote Office  
> **Módulo:** 05 — Projeto final integrado  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você terá a planilha `candidaturas.xlsx`, que:

- Guarda cada candidatura em uma **Tabela** do Excel, com **lista suspensa** de status.
- Calcula sozinha há **quantos dias** cada candidatura espera resposta.
- **Destaca** quem precisa ser cobrado.
- Tem um **painel** com contagens, **taxa de resposta** e um **gráfico** — que vai para a sua apresentação.
- Está pronta para alimentar a **mala direta** das cartas no Word.

## Pré-requisitos

- [Aula 01](01_planejamento_do_projeto.md): objetivo, palavras-chave e pasta do projeto.
- Do [Módulo 02 — Excel](../modulo_02_excel/index.md): Tabela, `SE`, `CONT.SE`, formatação condicional, validação de dados, `FILTRO` e gráficos.

---

## A planilha

Use as **suas** candidaturas (reais ou simuladas). Para conferir as fórmulas com os gabaritos, comece com os dados abaixo — os endereços terminam em `.example` porque são inventados — e troque pelos seus depois.

Cole na célula **A1** da planilha `Candidaturas`:

| Empresa | Contato | E-mail | Vaga | Enviado em | Status |
|---|---|---|---|---|---|
| Padaria Bom Pão | Marta Rocha | rh@bompao.example | Atendimento | 03/11/2026 | Entrevista |
| Loja Tech Mais | Paulo Dias | vagas@techmais.example | Jovem Aprendiz — vendas | 05/11/2026 | Enviado |
| Escritório Contábil Silva | Lúcia Silva | contato@contabilsilva.example | Auxiliar administrativo | 06/11/2026 | Recusado |
| Supermercado Econômico | Rafael Lima | rh@economico.example | Jovem Aprendiz — estoque | 08/11/2026 | Enviado |
| Clínica Sorriso | Beatriz Nunes | recepcao@clinicasorriso.example | Recepção | 12/11/2026 | Entrevista |
| Agência Pixel | Igor Mendes | estagio@agenciapixel.example | Estágio em design | 14/11/2026 | Enviado |
| Biblioteca Municipal | Sônia Prado | biblioteca@prefeitura.example | Estágio administrativo |  | A enviar |
| Farmácia Saúde | Carlos Alves | rh@farmaciasaude.example | Atendente |  | A enviar |

### As regras

- **Status** possíveis: *A enviar*, *Enviado*, *Entrevista*, *Recusado*, *Aprovado*.
- **Dias sem resposta:** só para as candidaturas com status *Enviado* — a data de hoje menos a data de envio.
- **Cobrar:** candidatura *Enviada* há **mais de 10 dias** sem resposta merece um e-mail educado perguntando se há novidades.
- **Taxa de resposta:** das candidaturas enviadas, quantas tiveram alguma resposta (*Entrevista*, *Recusado* ou *Aprovado*).

!!! info "A data de hoje"
    Na sua planilha de verdade, a célula de “hoje” terá `=HOJE()` e tudo se atualiza sozinho a cada dia. Para os resultados baterem com os gabaritos, use nos exercícios a data **fixa** `20/11/2026`.

---

## Montando, parte por parte

### 1. A Tabela (Módulo 02, aula 03)

- `Ctrl + Alt + T` ➔ nome da tabela **`Candidaturas`**.
- Coluna *Enviado em* com formato de **data**; *Status* com **lista suspensa**.
- **Congelar** a linha do cabeçalho.

### 2. A coluna calculada (Módulo 02, aula 02)

- Em **I1** escreva `Hoje` e em **J1** a data de referência.
- Nova coluna **Dias sem resposta**, com um `SE`: se o status for *Enviado*, a diferença entre J1 e a data de envio; senão, vazio.

### 3. Os destaques (Módulo 02, aula 03)

- Formatação condicional **por fórmula** pintando a linha de quem precisa ser cobrado.
- Cores para os status (*Entrevista* em verde, *Recusado* em cinza...).

### 4. O painel (Módulo 02, aulas 02 a 04)

- Em uma planilha **Painel**: quantas candidaturas em cada status (`CONT.SE`), total enviado, **taxa de resposta** e um **gráfico** com título que diz a conclusão.
- A **lista de cobrança** com `FILTRO`.

!!! tip "Cabeçalhos pensando na mala direta"
    O Word vai usar os nomes das colunas como **campos** das cartas: «Empresa», «Contato», «Vaga». Nomes curtos e claros facilitam. E lembre: na hora da mala direta, a planilha precisa estar **salva e fechada**.

---

??? note "Equivalentes gratuitos: LibreOffice Calc e Google Planilhas"
    | Tarefa | LibreOffice Calc | Google Planilhas |
    |---|---|---|
    | Tabela com nome | Use um intervalo comum (`A1:G9`) ou *Dados ➔ Definir intervalo* | *Formatar ➔ Converter em tabela* |
    | Lista suspensa | *Dados ➔ Validade ➔ Permitir: Lista* | *Inserir ➔ Menu suspenso* |
    | Dias sem resposta | `=SE(F2="Enviado";$J$1-E2;"")` (endereços em vez de nomes de coluna) | A mesma fórmula com endereços |
    | Lista de cobrança | `FILTRO`, no LibreOffice 24.8 ou mais novo | `FILTER` |
    | Mala direta depois | O Writer lê a `.xlsx` ou a `.ods` | Faça o download em `.xlsx` para usar no Word ou no Writer |

---

## ⚠️ Erros comuns

- **Data digitada como texto** (`5/nov`, `05.11.2026`): a conta de dias dá `#VALOR!`. Use `05/11/2026` e confira se a data fica alinhada à **direita**.
- **Coluna de dias aparecendo como data** (`15/01/1900`): o Excel herdou o formato de data. Formate como **Geral** ou **Número**.
- **Status digitado à mão** com variações (“enviado”, “Enviada”): o `CONT.SE` não conta. Por isso, a lista suspensa.
- **Gráfico com os dados da Tabela inteira.** Faça o gráfico a partir do **resumo** do painel, não das linhas de candidatura.

---

## Exercícios

### Básico (fixação)

Monte a Tabela **`Candidaturas`** com os dados da aula, a lista suspensa de status, a data de referência `20/11/2026` em **J1** e a coluna calculada **Dias sem resposta** (G).

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Cole os dados em A1 ➔ `Ctrl + Alt + T` ➔ *Design da Tabela ➔ Nome da Tabela:* `Candidaturas`. Formate a coluna E como **Data Abreviada**.
    2. Selecione os status (F2:F9) ➔ *Dados ➔ Validação de Dados ➔ Lista* ➔ `A enviar;Enviado;Entrevista;Recusado;Aprovado`.
    3. **I1:** `Hoje` · **J1:** `20/11/2026`.
    4. Em **G1**, escreva `Dias sem resposta` (a tabela cresce) e em **G2**:

        ```text
        =SE([@Status]="Enviado";$J$1-[@[Enviado em]];"")
        ```

        A tabela copia para as outras linhas. Formate a coluna G como **Geral**.

    **Confira:** Loja Tech Mais **15** · Supermercado Econômico **12** · Agência Pixel **6** · as outras linhas **vazias**.

### Intermediário (aplicação)

1. Pinte de **laranja** a linha inteira das candidaturas que precisam ser **cobradas** (enviadas há mais de 10 dias).
2. Na planilha **Painel**, monte o resumo: quantas candidaturas em cada status, quantas foram **enviadas** e a **taxa de resposta**.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Selecione **A2:G9** ➔ *Formatação Condicional ➔ Nova Regra ➔ Usar uma fórmula*:

        ```text
        =E($F2="Enviado";$G2>10)
        ```

        ➔ preenchimento laranja. Ficam pintadas **Loja Tech Mais** (15 dias) e **Supermercado Econômico** (12). A Agência Pixel (6 dias) não.
    2. **Painel**, com os status em A2:A6 (*A enviar*, *Enviado*, *Entrevista*, *Recusado*, *Aprovado*) e, em **B2**, copiado até B6:

        ```text
        =CONT.SE(Candidaturas[Status];A2)
        ```

        ➔ **2 · 3 · 2 · 1 · 0**.
        - **Enviadas** (B8): `=CONT.VALORES(Candidaturas[Empresa])-B2` ➔ **6**.
        - **Taxa de resposta** (B9, formato %): `=(B4+B5+B6)/B8` ➔ **50%** (3 respostas em 6 envios).

### Avançado (desafio)

1. No Painel, crie a **lista de cobrança** com uma única fórmula: as empresas a cobrar, com o e-mail ao lado.
2. Crie um **gráfico de barras** com as candidaturas por status e um título que diga a conclusão. Ele vai para a apresentação da aula 04.
3. Mude o status da **Loja Tech Mais** para *Entrevista* e confira o que muda em cada parte da planilha.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Em **D2** do Painel (com `Cobrar` em D1):

        ```text
        =FILTRO(Candidaturas[[Empresa]:[E-mail]];(Candidaturas[Status]="Enviado")*(Candidaturas[Dias sem resposta]>10);"Ninguém para cobrar")
        ```

        O intervalo `[[Empresa]:[E-mail]]` traz as três primeiras colunas (Empresa, Contato e E-mail) e o resultado se espalha em D2:F3: **Loja Tech Mais** e **Supermercado Econômico**, com contato e e-mail.
    2. Selecione **A1:B6** do Painel (com títulos em A1:B1, como `Status` e `Candidaturas`) ➔ *Inserir ➔ Gráfico de Barras Agrupadas* ➔ título, por exemplo, “Metade das candidaturas enviadas já teve resposta” ➔ rótulos de dados ligados.
    3. Com a Loja Tech Mais em *Entrevista*: a coluna G dela fica **vazia**; a linha **deixa de ser laranja**; o Painel mostra **Enviado 2** e **Entrevista 3**; a taxa de resposta vai a **67%** (4 de 6); a lista de cobrança fica só com o **Supermercado Econômico**; e o gráfico se atualiza. Tudo sem digitar nenhum número.

---

## 💡 Resumo

- **Tabela** `Candidaturas` com lista suspensa de status e datas de verdade.
- **Dias sem resposta** com `SE` e a data de referência (`=HOJE()` na vida real).
- **Formatação condicional por fórmula** mostra quem cobrar; `FILTRO` monta a lista.
- **Painel:** `CONT.SE` por status, taxa de resposta e gráfico com título que conclui.
- A planilha é a **fonte** das cartas e do gráfico da apresentação.

## ➡️ Próximo passo

**[03 — Currículo e cartas de apresentação](03_curriculo_e_cartas.md)**: o currículo de uma página e as cartas personalizadas, geradas a partir desta planilha.
