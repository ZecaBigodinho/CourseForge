# 02 — Estilos, seções e numeração de páginas

> **Curso:** Pacote Office  
> **Módulo:** 01 — Word  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Aplicar e **modificar estilos** (Normal, Título 1, Título 2) para formatar o documento inteiro de uma vez.
- Numerar seções automaticamente (**1**, **1.1**, **1.2**, **2**...).
- Navegar e reorganizar o documento pelo **Painel de Navegação**.
- Dividir o documento em **seções** com quebras de seção.
- Numerar as páginas **no padrão ABNT**: contadas desde a folha de rosto e exibidas a partir da introdução.

## Pré-requisitos

- [Aula 01](01_primeiros_passos_e_formatacao.md): formatação de parágrafo e de página.

---

## Por que estilos?

Imagine um trabalho de 20 páginas com 12 títulos. O professor pede para trocar a fonte dos títulos. Sem estilos, você caça e muda os 12, um por um. **Com estilos, você muda o estilo uma vez e os 12 títulos mudam juntos.**

Um **estilo** é um “pacote” de formatação com nome. Os principais:

| Estilo | Uso |
|---|---|
| **Normal** | Todo o texto comum (é o estilo de base) |
| **Título 1** | Seções principais: 1 INTRODUÇÃO, 2 DESENVOLVIMENTO... |
| **Título 2** | Subseções: 2.1, 2.2... |
| **Legenda** | Títulos de figuras e tabelas (aula 03) |

Para aplicar: clique no parágrafo e escolha o estilo em *Página Inicial ➔ Estilos*.

!!! tip "Os títulos viram a espinha do documento"
    Tudo que está como *Título 1* e *Título 2* aparece no **Painel de Navegação** e, na próxima aula, no **sumário automático**. Título feito “na mão” (só negrito e tamanho maior) fica de fora.

---

## Modificar um estilo

Clique com o botão direito no estilo ➔ **Modificar**:

- Ajuste fonte, tamanho, negrito e alinhamento na própria janela.
- Em **Formatar ➔ Parágrafo**, ajuste recuos e espaçamentos.
- Em **Formatar ➔ Fonte**, marque **Todas em maiúsculas** se a norma pedir.

Um padrão comum para trabalhos (confira o manual da escola):

| Estilo | Formatação |
|---|---|
| **Título 1** | Arial 12, **negrito**, TODAS EM MAIÚSCULAS, alinhado à esquerda, sem recuo |
| **Título 2** | Arial 12, sem negrito, TODAS EM MAIÚSCULAS, alinhado à esquerda, sem recuo |
| **Normal** | Arial 12, justificado, 1,5 linha, recuo 1,25 cm |

!!! info "Atualizar estilo a partir da seleção"
    Outro jeito: formate um título do jeito que quer, clique com o botão direito no estilo e escolha **Atualizar Título 1 para Corresponder à Seleção**.

---

## Numeração progressiva das seções

Para os títulos ganharem **1**, **1.1**, **2** sozinhos:

1. Clique em um parágrafo com *Título 1*.
2. *Página Inicial ➔ Lista de Vários Níveis* (ícone com 1, a, i).
3. Escolha o modelo que mostra **“1 Título 1 / 1.1 Título 2”**.

Agora, se você inserir uma seção nova no meio, toda a numeração se ajusta.

---

## Painel de Navegação

*Exibir ➔ Painel de Navegação*. Ele lista os títulos do documento:

- Clique em um título para pular até ele.
- **Arraste** um título para cima ou para baixo: a seção inteira (título e texto) muda de lugar.

---

## Seções: partes do documento com configurações próprias

Uma **seção** é um trecho do documento que pode ter cabeçalho, rodapé, numeração e até orientação de página próprios. Crie com *Layout ➔ Quebras ➔ **Próxima Página*** (em *Quebras de Seção*).

!!! warning "Quebra de página × quebra de seção"
    `Ctrl + Enter` (quebra de **página**) só começa uma página nova. A quebra de **seção** começa uma página nova **e** uma parte independente do documento. Para a numeração ABNT, você precisa da de seção.

---

## Numeração de páginas no padrão ABNT

A regra: as páginas são **contadas a partir da folha de rosto** (a capa não conta), mas o número **só aparece a partir da primeira página do texto** (a Introdução), em algarismos arábicos, **no canto superior direito**.

Exemplo de trabalho com capa, folha de rosto, sumário e introdução:

| Página física | Conteúdo | Conta? | Número aparece? |
|---|---|---|---|
| 1 | Capa | Não | Não |
| 2 | Folha de rosto | Sim (1) | Não |
| 3 | Sumário | Sim (2) | Não |
| 4 | Introdução | Sim (3) | **Sim: 3** |

Passo a passo no Word:

1. No fim do sumário (antes da Introdução), insira *Layout ➔ Quebras ➔ **Próxima Página***. Agora o documento tem a **Seção 1** (capa, folha de rosto, sumário) e a **Seção 2** (do texto em diante).
2. Dê dois cliques no topo da página da Introdução para abrir o **cabeçalho**. Na aba *Cabeçalho e Rodapé*, **desligue *Vincular ao Anterior*** — assim o cabeçalho da Seção 2 deixa de copiar o da Seção 1.
3. *Número de Página ➔ Início da Página ➔ **Número Simples 3*** (alinhado à direita).
4. *Número de Página ➔ **Formatar Números de Página*** ➔ *Iniciar em*: **3** (folha de rosto = 1, sumário = 2, introdução = 3).
5. Vá ao cabeçalho da Seção 1 e confira que ele está **vazio**.

!!! tip "Quantas páginas tem o seu pré-textual?"
    O número de *Iniciar em* é: **páginas da folha de rosto até a introdução, contando a própria introdução**. Com agradecimentos ou resumo, o número aumenta.

---

??? note "Equivalentes gratuitos: LibreOffice Writer e Google Docs"
    | Tarefa | LibreOffice Writer | Google Docs |
    |---|---|---|
    | Estilos | Painel *Estilos* (`F11`); botão direito ➔ *Editar estilo* | *Texto normal / Título 1* na barra; *Atualizar "Título 1" para corresponder* |
    | Numeração de títulos | *Ferramentas ➔ Numeração de capítulos* | Não tem automático — numere à mão |
    | Navegação | *Exibir ➔ Navegador* (`F5`) | *Exibir ➔ Mostrar estrutura de tópicos* |
    | Numeração a partir de uma página | Use um estilo de página diferente para o texto (*Formatar ➔ Estilo de página*) | *Inserir ➔ Números de página ➔ Mais opções* (opções limitadas) |

---

## ⚠️ Erros comuns

- **Título “fantasiado”**: negrito e fonte grande no estilo *Normal*. Não entra no sumário. Use *Título 1/2*.
- **Esquecer de desligar “Vincular ao Anterior”**: o número aparece (ou some) em todas as seções ao mesmo tempo.
- **Numerar a capa**: na ABNT, a capa não é contada nem numerada.

---

## Exercícios

### Básico (fixação)

1. Crie um documento com três seções: **Introdução**, **Desenvolvimento** (com duas subseções: **Causas** e **Consequências**) e **Conclusão**, cada uma com um parágrafo curto.
2. Aplique *Título 1* às seções e *Título 2* às subseções.
3. Abra o **Painel de Navegação** e mova a *Conclusão* para antes do *Desenvolvimento* — depois desfaça.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. Digite os títulos e parágrafos, cada um terminado com `Enter`.
    2. Clique em “Introdução”, “Desenvolvimento” e “Conclusão” e escolha **Título 1** em *Página Inicial ➔ Estilos*; em “Causas” e “Consequências”, **Título 2**.
    3. *Exibir ➔ Painel de Navegação*. Arraste “Conclusão” para cima de “Desenvolvimento”: o parágrafo vai junto. `Ctrl + Z` desfaz.

    **Confira:** o painel mostra as subseções recuadas sob “Desenvolvimento”. Se algum título não aparece lá, ele não está com estilo de título.

### Intermediário (aplicação)

No documento do exercício anterior:

- Modifique **Título 1** e **Título 2** conforme a tabela da aula (Arial 12, maiúsculas, à esquerda, Título 1 em negrito).
- Faça os títulos ganharem numeração automática **1**, **2**, **2.1**, **2.2**, **3**.
- Insira uma seção nova “Metodologia” entre Introdução e Desenvolvimento e observe a renumeração.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Botão direito em **Título 1 ➔ Modificar**: Arial, 12, **Negrito**, cor *Automático*, alinhar à esquerda. *Formatar ➔ Fonte* ➔ marque **Todas em maiúsculas**. *Formatar ➔ Parágrafo* ➔ recuo *Primeira linha*: **(nenhum)**.
    2. Repita para **Título 2**, sem negrito.
    3. Clique em um *Título 1* ➔ *Página Inicial ➔ Lista de Vários Níveis* ➔ modelo **“1 Título 1 / 1.1 Título 2”**.
    4. Ao final da Introdução, `Enter`, digite “Metodologia” e aplique *Título 1*: ela vira **2** e as seguintes passam a **3** e **4** (com 3.1 e 3.2).

    **Por que os títulos ficam em maiúsculas sem você redigitar:** a opção *Todas em maiúsculas* muda só a aparência — o texto continua “Metodologia”.

### Avançado (desafio)

Monte a numeração ABNT completa num documento de 5 páginas: **capa**, **folha de rosto**, **sumário** (pode deixar só o título por enquanto), **introdução** e **desenvolvimento**.

- Capa, folha de rosto e sumário **sem número** visível.
- A introdução mostra **3** e o desenvolvimento **4**, no canto superior direito.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. Separe capa, folha de rosto e sumário com `Ctrl + Enter` (quebra de página).
    2. No fim do sumário, *Layout ➔ Quebras ➔ **Próxima Página*** (quebra de **seção**). Separe introdução e desenvolvimento com `Ctrl + Enter`.
    3. Dois cliques no cabeçalho da introdução ➔ desligue **Vincular ao Anterior**.
    4. *Número de Página ➔ Início da Página ➔ Número Simples 3*.
    5. *Número de Página ➔ Formatar Números de Página* ➔ **Iniciar em: 3**.
    6. Confira o cabeçalho da capa, da folha de rosto e do sumário: se algum número aparecer lá, apague-o (com *Vincular ao Anterior* desligado na seção 2, isso não afeta a introdução).

    **Confira com o ¶ ligado:** no fim do sumário deve aparecer *Quebra de Seção (Próxima Página)*.

---

## 💡 Resumo

- **Estilos** formatam o documento inteiro de uma vez — mude o estilo, não o texto.
- *Título 1* e *Título 2* alimentam o **Painel de Navegação** e o **sumário**.
- **Lista de Vários Níveis** numera as seções automaticamente.
- **Quebra de seção** cria partes independentes; **Vincular ao Anterior** desligado separa os cabeçalhos.
- ABNT: conta desde a **folha de rosto**, mostra a partir da **introdução**, no **canto superior direito**.

## ➡️ Próximo passo

**[03 — Sumário, citações e referências (ABNT)](03_sumario_citacoes_e_referencias.md)**: com os títulos prontos, o sumário se monta sozinho. Depois, você aprende a citar autores e a listar as referências.
