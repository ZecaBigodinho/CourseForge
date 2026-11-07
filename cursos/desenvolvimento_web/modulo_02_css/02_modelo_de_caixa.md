# 02 — Modelo de caixa

> **Curso:** Desenvolvimento Web  
> **Módulo:** 02 — CSS  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar as quatro camadas da caixa: **conteúdo**, **padding**, **borda** e **margem**.
- Controlar **largura** e **altura** com `box-sizing: border-box`.
- Diferenciar elementos de **bloco** e **em linha**.
- Centralizar um bloco na página e arredondar cantos.

## Pré-requisitos

- [Aula 01](01_seletores_cores_e_fontes.md) deste módulo.

---

## Toda tag é uma caixa

O navegador desenha cada elemento como um retângulo com quatro camadas, de dentro para fora:

| Camada | Propriedade | O que é |
|---|---|---|
| Conteúdo | `width`, `height` | O texto ou a imagem |
| Preenchimento | `padding` | Espaço **dentro** da caixa, entre o conteúdo e a borda (pega a cor de fundo) |
| Borda | `border` | A linha em volta |
| Margem | `margin` | Espaço **fora** da caixa, que afasta as vizinhas (sempre transparente) |

```css
.cartao {
  width: 300px;
  padding: 16px;
  border: 2px solid #4f35b5;
  border-radius: 12px;
  margin: 24px auto;
  background-color: white;
}
```

!!! tip "Veja a caixa no navegador"
    `F12` ➔ guia **Elementos** ➔ selecione um elemento. O painel **Computado** (ou *Layout*) desenha a caixa com as medidas de margem, borda e padding. É o melhor jeito de entender por que algo está fora do lugar.

### Atalhos de valores

| Escrita | Significa |
|---|---|
| `padding: 16px;` | 16 px nos quatro lados |
| `padding: 8px 16px;` | 8 em cima e embaixo, 16 nos lados |
| `padding: 8px 16px 4px 0;` | cima, direita, baixo, esquerda (sentido do relógio) |
| `margin-top: 24px;` | Só um lado |

---

## `box-sizing: border-box`

Por padrão, `width: 300px` vale só para o conteúdo: com padding e borda, a caixa fica com **336 px**. Isso confunde. Quase todo site começa com:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

Com `border-box`, os 300 px **incluem** padding e borda. O asterisco (`*`) seleciona todos os elementos.

---

## Bloco × em linha

| Tipo | Exemplos | Comportamento |
|---|---|---|
| **Bloco** (`block`) | `<p>`, `<h1>`, `<div>`, `<section>`, `<ul>` | Começa numa linha nova e ocupa toda a largura disponível |
| **Em linha** (`inline`) | `<a>`, `<strong>`, `<em>`, `<span>` | Fica no meio do texto; `width` e margens de cima e de baixo não funcionam |
| **Bloco em linha** (`inline-block`) | `<button>`, `<img>` | Fica na linha, mas aceita largura e altura |

Dá para trocar com `display`, por exemplo `display: block;` num link para ele ocupar a linha toda.

!!! info "`<div>` e `<span>`: caixas sem significado"
    Quando nenhuma tag semântica serve, use `<div>` (bloco) ou `<span>` (em linha) só para aplicar uma classe. Mas prefira as semânticas do Módulo 01 sempre que fizerem sentido.

---

## Centralizar e limitar a largura

Textos muito largos cansam a leitura. Para um conteúdo centralizado com largura máxima:

```css
main {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
}
```

- `max-width`: no máximo 800 px, mas encolhe em telas menores.
- `margin: 0 auto`: margens laterais automáticas e iguais, que **centralizam** o bloco.
- O `padding` lateral evita o texto colado na borda do celular.

---

## Exercícios

### Básico (fixação)

Transforme cada `<section>` da página de apresentação num cartão branco, com padding de 24 px, borda roxa de 2 px e cantos arredondados.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```css
    section {
      background-color: white;
      padding: 24px;
      border: 2px solid #4f35b5;
      border-radius: 12px;
      margin-bottom: 24px;
    }
    ```

### Intermediário (aplicação)

Uma caixa tem `width: 200px`, `padding: 20px` e `border: 5px solid`. Qual a largura total com e sem `border-box`?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    **Sem** `border-box` (padrão `content-box`): 200 + 20 + 20 + 5 + 5 = **250 px**. **Com** `border-box`: **200 px** (o conteúdo encolhe para 150 px). As margens nunca entram nessa conta.

### Avançado (desafio)

Centralize o `<main>` com no máximo 720 px e faça os links do menu parecerem botões (fundo roxo, texto branco, padding e cantos arredondados).

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```css
    main { max-width: 720px; margin: 0 auto; padding: 0 16px; }
    nav a {
      display: inline-block;
      padding: 8px 16px;
      background-color: #4f35b5;
      color: white;
      text-decoration: none;
      border-radius: 8px;
    }
    ```
    O `inline-block` é o que faz o padding de cima e de baixo funcionar no link, que é em linha.

---

## 💡 Resumo

- Caixa = conteúdo + `padding` + `border` + `margin`.
- Comece todo CSS com `box-sizing: border-box`.
- Bloco ocupa a linha; em linha fica no texto; `display` troca o tipo.
- `max-width` + `margin: 0 auto` centralizam o conteúdo.

## ➡️ Próximo passo

Na **[aula 03](03_flexbox.md)** você alinha elementos lado a lado com Flexbox.
