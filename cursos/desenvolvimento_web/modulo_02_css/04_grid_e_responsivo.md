# 04 — Grid e layout responsivo

> **Curso:** Desenvolvimento Web  
> **Módulo:** 02 — CSS  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Montar **grades** de linhas e colunas com `display: grid`.
- Usar a unidade `fr` e a função `repeat()`.
- Criar uma grade que se ajusta sozinha com `auto-fit` e `minmax()`.
- Mudar o layout no celular com **media queries** e imagens flexíveis.

## Pré-requisitos

- [Aula 03](03_flexbox.md) deste módulo.

---

## Flexbox ou Grid?

| | Flexbox | Grid |
|---|---|---|
| Dimensão | **Uma** (linha *ou* coluna) | **Duas** (linhas *e* colunas) |
| Bom para | Menus, barras, alinhar itens | Grades de cartões, galerias, o layout da página inteira |

Os dois convivem: é comum usar Grid na página e Flexbox dentro de cada cartão.

---

## O básico do Grid

```css
.galeria {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
```

- `grid-template-columns` define as colunas. `1fr 1fr 1fr` = três colunas iguais.
- `fr` (*fração*) divide o espaço livre: `2fr 1fr` faz a primeira coluna ter o dobro da segunda.
- `repeat(3, 1fr)` é o mesmo que `1fr 1fr 1fr`.
- Os itens preenchem as células na ordem do HTML, linha por linha.

Um item pode ocupar mais de uma coluna:

```css
.destaque { grid-column: span 2; }
```

### A grade que se ajusta sozinha

```css
.cartoes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
```

“Ponha quantas colunas couberem, cada uma com no mínimo 220 px e dividindo o que sobrar.” No computador aparecem quatro colunas; no celular, uma, **sem nenhuma media query**.

---

## Layout responsivo

**Responsivo** é o site que funciona bem em qualquer tela. Três ingredientes:

### 1. A meta viewport

Já está no esqueleto do Módulo 01. Sem ela, o celular mostra a página “de longe”, miudinha:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 2. Imagens flexíveis

```css
img {
  max-width: 100%;
  height: auto;
}
```

A imagem nunca passa da largura do seu container e mantém a proporção.

### 3. Media queries

Regras que só valem a partir de certa largura de tela:

```css
/* celular primeiro: uma coluna */
.layout {
  display: grid;
  gap: 24px;
}

/* a partir de 768 px (tablet e computador): duas colunas */
@media (min-width: 768px) {
  .layout {
    grid-template-columns: 2fr 1fr;
  }
}
```

!!! tip "Comece pelo celular"
    Escreva primeiro o CSS da tela pequena (mais simples, uma coluna) e acrescente colunas com `min-width`. A maioria das pessoas acessa sites pelo celular.

!!! info "Teste sem celular"
    `F12` ➔ botão de **dispositivos** (ícone de celular e tablet) ou `Ctrl + Shift + M`. Escolha *iPhone*, *Galaxy* ou arraste a largura e veja o layout mudar.

---

## Exercícios

### Básico (fixação)

Monte uma galeria de 6 imagens em 3 colunas iguais com 12 px de espaço.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```css
    .galeria { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .galeria img { max-width: 100%; height: auto; }
    ```

### Intermediário (aplicação)

Troque a galeria para se ajustar sozinha: colunas de no mínimo 180 px. Teste no modo dispositivos do `F12`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```css
    .galeria { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
    ```
    Numa tela larga aparecem várias colunas; estreitando, elas diminuem até uma.

### Avançado (desafio)

Faça a página de apresentação ter, no computador, o conteúdo à esquerda (2/3) e a seção de contato à direita (1/3); no celular, tudo numa coluna.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```css
    main { display: grid; gap: 24px; }
    @media (min-width: 768px) {
      main { grid-template-columns: 2fr 1fr; }
      #contato { grid-column: 2; grid-row: 1 / span 2; }
    }
    ```
    No celular vale só a primeira regra (uma coluna). A partir de 768 px, duas colunas, e o contato vai para a coluna da direita, ocupando duas linhas.

---

## 💡 Resumo

- Grid = duas dimensões; Flexbox = uma. Use os dois juntos.
- `grid-template-columns: repeat(3, 1fr)`; `fr` divide o espaço livre.
- `repeat(auto-fit, minmax(220px, 1fr))` ajusta as colunas sozinho.
- Responsivo: meta viewport, `img { max-width: 100% }` e `@media (min-width: …)`, começando pelo celular.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_cardapio.md)** você monta o cardápio de uma lanchonete com tudo o que aprendeu.
