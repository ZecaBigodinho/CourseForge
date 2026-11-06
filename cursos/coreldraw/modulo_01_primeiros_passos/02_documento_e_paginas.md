# 02 — Documento: tamanho, unidades e páginas

> **Curso:** CorelDRAW  
> **Módulo:** 01 — Primeiros passos  
> **Tempo estimado:** 1 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar um documento pela janela **Criar um novo documento**, escolhendo nome, tamanho, unidade, orientação e número de páginas.
- Entender as opções **CMYK × RGB** e **resolução** dessa janela.
- Mudar o tamanho e a unidade de um documento **já aberto**, pela barra de propriedades.
- Acrescentar, renomear e apagar **páginas**.

## Pré-requisitos

- [Aula 01](01_conhecendo_o_coreldraw.md) deste módulo.

---

## Criar um novo documento

Na tela de boas-vindas, clique em **Novo documento**, ou use `Ctrl + N` a qualquer momento. Abre esta janela:

<figure markdown="span">
  ![Janela Criar um novo documento: à esquerda as predefinições Padrões do Corel 210 × 297 mm, CMYK padrão, Ofício, Carta, Cartão de visita, envelopes e outras; à direita o Nome, o Número de páginas, a Vista de página, o Modo de cores primárias CMYK ou RGB, a Largura, a Altura e a unidade, a Orientação, a Resolução e o botão OK](assets/02_novo_documento.webp){ loading=lazy }
  <figcaption>(1) predefinições de tamanho · (2) <strong>Nome</strong> do documento · (3) <strong>Número de páginas</strong> · (4) <strong>Modo de cores</strong> · (5) <strong>Largura</strong>, <strong>Altura</strong> e unidade · (6) <strong>Orientação</strong> · (7) <strong>Resolução</strong> · (8) <strong>OK</strong>.</figcaption>
</figure>

1. **Predefinição (1).** *Padrões do Corel* é o A4 (210 × 297 mm). Há também Ofício, Carta, envelopes… Atenção: o *Cartão de visita* da lista tem **3,5 × 2 polegadas** (padrão americano). Para o cartão brasileiro, digite as medidas (passo 4).
2. **Nome (2).** Dê um nome claro já agora, como `cartao_ana_souza`. Ele vira o nome sugerido ao salvar.
3. **Número de páginas (3).** Um panfleto frente e verso, por exemplo, tem 2.
4. **Largura e Altura (5).** Escolha primeiro a **unidade** na lista ao lado (*milímetros*) e depois digite as medidas. Ao mudar as medidas, a predefinição vira *Personalizado*.
5. **Orientação (6).** Retrato (em pé) ou paisagem (deitado). Trocar a orientação inverte largura e altura.
6. Clique em **OK (8)**.

!!! info "CMYK, RGB e resolução, sem susto"
    - **Modo de cores (4):** **CMYK** é o modo das tintas de impressão (ciano, magenta, amarelo e preto); **RGB** é o das telas. Para material impresso, deixe **CMYK**. O Módulo 03 aprofunda o assunto.
    - **Resolução (7):** só vale para efeitos e imagens de pixels dentro do documento. As formas vetoriais não dependem dela. Deixe **300 dpi**, o padrão para impressão.

!!! tip "Unidade certa desde o começo"
    Gráficas no Brasil falam em **milímetros** e **centímetros**. Se o documento estiver em polegadas, as medidas aparecem quebradas (3,543 pol.) e é fácil errar.

---

## Mudar o documento depois

Com a ferramenta **Seleção** ativa e **nada selecionado** (clique numa área vazia), a barra de propriedades mostra as configurações da página:

<figure markdown="span">
  ![Barra de propriedades do CorelDRAW com nada selecionado: lista de tamanho A4, largura 210,0 mm e altura 297,0 mm, botões de orientação retrato e paisagem e a lista Unidades em milímetros; embaixo, o navegador de páginas com 1 de 2, as abas Página 1 e Página 2 e o botão de adicionar página](assets/02_paginas.webp){ loading=lazy }
  <figcaption>(1) tamanho predefinido · (2) <strong>largura</strong> e <strong>altura</strong> da página · (3) <strong>retrato</strong> ou <strong>paisagem</strong> · (4) <strong>Unidades</strong> · (5) navegador de páginas: “1 de 2”, as abas e o <strong>+</strong>.</figcaption>
</figure>

- Para mudar o tamanho, digite na largura e na altura (2) e tecle `Enter`.
- A unidade escolhida em (4) passa a valer para as réguas e para todas as medidas da barra de propriedades.

!!! warning "Mudar o tamanho não reorganiza o desenho"
    Se você reduz uma página que já tem objetos, eles **não** encolhem junto: ficam onde estavam, alguns para fora da página. Defina o tamanho **antes** de começar a desenhar.

---

## Páginas

No **navegador de páginas** (5):

| Para... | Faça |
|---|---|
| Acrescentar uma página no fim | Clique no **+** à direita das abas |
| Acrescentar antes ou depois de uma página | Botão direito na aba ➔ opção de **inserir página** antes ou depois |
| Ir para outra página | Clique na aba, ou use as setas e o “1 de 2” |
| Renomear (ex.: *Frente*, *Verso*) | Botão direito na aba ➔ **renomear página** |
| Apagar | Botão direito na aba ➔ **excluir página** |

Os mesmos comandos ficam no menu **Layout**.

---

??? note "No Inkscape"
    - Tamanho e unidade: **Arquivo ➔ Propriedades do documento** (`Ctrl + Shift + D`). Escolha o *formato* (A4, A5…) ou digite largura e altura, e a unidade *mm*.
    - Orientação: os botões de retrato e paisagem na mesma janela.
    - Várias páginas: a partir do Inkscape 1.2, ferramenta **Páginas** na caixa de ferramentas; clique no **+** da barra de controles para criar outra.
    - O Inkscape trabalha em **RGB**. O CMYK para gráfica é tratado no Módulo 03.

---

## Exercícios

### Básico (fixação)

Crie um documento A4 em **paisagem**, com **2 páginas**, chamado `exercicio_paginas`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    `Ctrl + N` ➔ Nome `exercicio_paginas` ➔ Número de páginas **2** ➔ predefinição *Padrões do Corel* (A4) ➔ Orientação **paisagem** (a largura passa a 297 mm e a altura a 210 mm) ➔ **OK**. O navegador mostra “1 de 2”.

### Intermediário (aplicação)

Num documento aberto, mude a página para **9 × 5 cm** em milímetros e acrescente uma segunda página chamada **Verso**.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. Clique numa área vazia (nada selecionado).
    2. Na barra de propriedades, **Unidades** ➔ *milímetros*; largura **90**, altura **50**, `Enter`. A predefinição vira *Personalizado*.
    3. No navegador de páginas, clique no **+**; botão direito na aba nova ➔ renomear página ➔ `Verso`.

### Avançado (desafio)

Uma gráfica pediu um **marcador de páginas** de 5 × 18 cm, frente e verso. Crie o documento já certo, pela janela de novo documento, e explique a escolha de cada campo.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    `Ctrl + N` ➔ Nome `marcador_paginas` ➔ Número de páginas **2** (frente e verso) ➔ Modo de cores **CMYK** (é para imprimir) ➔ unidade **milímetros**, Largura **50**, Altura **180** (a orientação fica retrato sozinha) ➔ Resolução **300** dpi ➔ **OK**. Depois, renomeie as páginas para *Frente* e *Verso*.

---

## 💡 Resumo

- `Ctrl + N` abre **Criar um novo documento**: nome, páginas, cores, tamanho, unidade, orientação, resolução.
- **CMYK** para imprimir, **RGB** para tela; 300 dpi é o padrão de impressão.
- Com nada selecionado, a **barra de propriedades** muda tamanho, orientação e unidade da página.
- Páginas: **+** no navegador; botão direito na aba para inserir, renomear ou excluir.

## ➡️ Próximo passo

Na **[aula 03](03_formas_selecao_e_texto.md)** você desenha as primeiras formas e textos.
