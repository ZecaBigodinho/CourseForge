# 05 — Projeto do módulo: kit de lançamento

> **Curso:** CorelDRAW  
> **Módulo:** 04 — Peças comerciais  
> **Tempo estimado:** 3 h  

---

## Objetivos

Ao final desta aula, você terá um **kit de lançamento** para um negócio (a Padaria Pão Quente ou um seu), com:

- um **catálogo** de 4 páginas com página principal e numeração;
- **crachás** da equipe feitos com impressão mesclada;
- um **post** e um **story** para as redes;
- um **cartaz** de balcão com **QR code**;
- uma **faixa** de 3 × 1 m com ilhós.

## Pré-requisitos

- Aulas [01](01_catalogo_varias_paginas.md) a [04](04_faixa_e_qr_code.md) deste módulo, o [logotipo do Módulo 02](../modulo_02_vetor_na_pratica/05_projeto_logotipo.md) e o [kit para a gráfica do Módulo 03](../modulo_03_arquivos_para_grafica/05_projeto_kit_grafica.md).

---

## O pedido

> *“Vamos inaugurar a loja nova no dia 1º. Preciso de tudo com a mesma cara: catálogo, crachás, posts, cartaz com QR code e uma faixa para a fachada.”*

Um **kit** é mais que várias peças: é a **mesma identidade** em todas. O cliente reconhece a loja no post, na faixa e no crachá porque as cores, as fontes e o logotipo são os mesmos.

---

## Passo 1 — A identidade (antes de tudo)

Num arquivo de texto ou na primeira página de um documento, anote:

| Item | Exemplo (Padaria Pão Quente) |
|---|---|
| **Logotipo** | `logo_pao_quente_curvas.cdr` e `logo_pao_quente.png` (Módulo 02) |
| **Cor principal** | Laranja: C 0, M 35, Y 90, K 0 (impresso) · `#FBB141` (tela) |
| **Cor de apoio** | Marrom: C 0, M 60, Y 100, K 45 (impresso) e o equivalente RGB para a tela |
| **Fontes** | Uma para títulos, uma para textos (no máximo duas) |
| **Tom** | Acolhedor, frases curtas (“Pão quentinho às 6h e às 16h”) |

Essa tabela é um **mini guia de marca**: garante que todas as peças saiam iguais, mesmo feitas em dias diferentes ou por pessoas diferentes.

---

## Passo 2 — As peças

| Peça | Como | Aula |
|---|---|---|
| **Catálogo** A5, 4 páginas, CMYK | Página principal com cabeçalho, rodapé e número; uma categoria por página, com fotos em PowerClip | 01 e Módulo 03 |
| **Crachás** 86 × 54 mm | Modelo + planilha da equipe ➔ **Criar documento mesclado** | 02 |
| **Post** 1080 × 1080 e **story** 1080 × 1920, RGB | Mesma arte, reorganizada para cada formato; exportar JPG | 03 |
| **Cartaz** A4 de balcão, CMYK | Título + QR code do cardápio (tipo URL), com o endereço escrito embaixo | 04 |
| **Faixa** 3.000 × 1.000 mm | Pouco texto, logotipo grande; **Borda e ilhó** | 04 |

!!! tip "Comece pela peça mais difícil"
    Faça primeiro a peça com **mais restrições** (a faixa, que é vista de longe e tem pouquíssimo espaço para texto). Se a identidade funciona nela, funciona nas outras.

---

## Passo 3 — Conferência do kit

Para cada peça, antes de exportar:

- [ ] Documento certo: **CMYK e mm** (impresso) ou **RGB e px** (tela).
- [ ] Impressos com **sangria** e textos dentro da **margem de segurança**; a faixa com os **ilhós** no documento que vai para a gráfica.
- [ ] Mesmas **cores** (valores da tabela) e mesmas **fontes** em todas as peças.
- [ ] **Textos revisados**: preços, telefone, endereço, data da inauguração.
- [ ] **QR code** validado **e** testado com a câmera de um celular, impresso no tamanho real.
- [ ] Crachás conferidos **página por página** no documento mesclado.
- [ ] **Autor** preenchido nas Propriedades do documento antes de publicar os PDFs (Módulo 03, aula 05).

---

## Entrega

Uma pasta **kit_lancamento** com:

1. `catalogo_A5_PDFX4.pdf`
2. `crachas_PDFX4.pdf` (o documento mesclado)
3. `post_1080x1080.jpg` e `story_1080x1920.jpg`
4. `cartaz_A4_PDFX4.pdf`
5. `faixa_3x1m.pdf`
6. `identidade.txt` (a tabela do Passo 1)
7. Os arquivos `.cdr` editáveis (ficam com você).

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Identidade | Mesmas cores, fontes e logotipo em todas as peças. |
| Formato | Cada peça no tamanho, na unidade e no modo de cor certos. |
| Recursos | Página principal e numeração no catálogo; mesclagem nos crachás; QR code validado. |
| Leitura | Faixa legível de longe; post legível no celular; poucas palavras onde o espaço é pequeno. |
| Arquivos | PDFs para gráfica conferidos (sangria, marcas, autor); JPGs no tamanho exato. |
| Dados | Só dados inventados ou autorizados; nenhum dado pessoal além do necessário nos crachás. |

Este kit é **prática e portfólio**: o certificado do curso continua sendo o logotipo (Módulo 02) e o kit para a gráfica (Módulo 03). Junte o kit de lançamento ao portfólio para mostrar a um cliente ou num processo seletivo.

---

## Exercícios extras

### Básico (fixação)

Escreva a tabela de identidade (Passo 1) para um negócio **seu** ou inventado: logotipo, duas cores (CMYK e hex), duas fontes e o tom.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Exemplo para uma loja de bicicletas inventada: logotipo `pedal_certo.cdr`; azul C 90, M 50, Y 0, K 0 / `#1F6FC5`; amarelo C 0, M 15, Y 95, K 0 / `#FFD600`; títulos em *Montserrat Black*, textos em *Open Sans* (fontes gratuitas do Google Fonts, instaladas no Windows); tom “direto e animado”. Os valores hex saem da janela **Editar preenchimento** (Módulo 03, aula 01), com o modelo de cor trocado para RGB.

### Intermediário (aplicação)

Monte só o **cartaz** e o **post** do kit, com o mesmo QR code, e confira: um celular lê o QR do post **na tela de outro celular**?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Copie o QR code do cartaz para o post (`Ctrl + C`, `Ctrl + V`), mantendo o fundo claro e a margem em volta. Na tela, a maioria dos celulares lê bem um QR de pelo menos uns 300 × 300 px no post. Mas pense no uso: quem vê o post **já está no celular**, então um **link na bio** ou um botão costuma funcionar melhor do que um QR code na tela.

### Avançado (desafio)

A inauguração mudou do dia 1º para o dia 8. Liste o que precisa ser refeito e em quantos lugares, e diga o que poderia ter facilitado.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    A data aparece no post, no story, no cartaz, na faixa e talvez no catálogo: **cinco arquivos**, mais os PDFs e JPGs exportados de novo (e uma conferência completa). O que facilitaria: (1) uma **lista das peças** com onde cada informação aparece; (2) a data num lugar só quando possível (a **página principal** do catálogo, por exemplo); (3) **não pôr a data** nas peças que duram mais (faixa e catálogo), deixando-a só no post e no cartaz, que são baratos de refazer.

---

## 💡 Resumo

- Um kit começa pela **identidade** anotada: logotipo, cores (CMYK e hex), fontes e tom.
- Cada peça no **formato certo**: CMYK/mm/PDF para imprimir, RGB/px/JPG para a tela.
- Use os recursos certos: **página principal**, **impressão mesclada**, **QR code** validado, **ilhós**.
- Confira cada peça antes de exportar, e o kit **inteiro** junto, lado a lado.

## ➡️ Próximo passo

Você terminou o **Módulo 04** e o curso de **CorelDRAW**! Volte ao [índice do módulo](index.md) e confira o checklist. Para continuar: o curso de [Canva](../../canva/docs/index.md) usa o seu logotipo em posts e vídeos, e o curso de [Automação com Python](../../automacao_com_python/docs/index.md) gera certificados e crachás a partir de planilhas com código.
