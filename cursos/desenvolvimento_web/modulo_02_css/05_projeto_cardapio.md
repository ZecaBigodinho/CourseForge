# 05 — Projeto do módulo: cardápio

> **Curso:** Desenvolvimento Web  
> **Módulo:** 02 — CSS  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final deste projeto, você terá:

- O **cardápio** de uma lanchonete (inventada) em HTML e CSS.
- Um layout com cabeçalho em **Flexbox** e cartões em **Grid** que se ajustam ao celular.
- Cores e fontes organizadas em **variáveis** CSS.

## Pré-requisitos

- Aulas [01](01_seletores_cores_e_fontes.md) a [04](04_grid_e_responsivo.md) deste módulo.

---

## O pedido

> *“Quero o cardápio da Lanchonete do Bairro num link, para mandar no WhatsApp. Tem de ficar bom no celular.”*

A lanchonete e os preços são inventados.

---

## Variáveis CSS

Antes do código, um recurso novo: **variáveis** guardam cores e medidas num lugar só.

```css
:root {
  --cor-principal: #e8781e;
  --cor-texto: #2b2b2b;
}
h1 { color: var(--cor-principal); }
```

Para mudar a cor do site inteiro, basta trocar o valor em `:root`.

---

## O HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cardápio — Lanchonete do Bairro</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="topo">
    <h1>Lanchonete do Bairro</h1>
    <nav>
      <ul class="menu">
        <li><a href="#lanches">Lanches</a></li>
        <li><a href="#bebidas">Bebidas</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section id="lanches">
      <h2>Lanches</h2>
      <div class="cartoes">
        <article class="cartao">
          <h3>X-Salada</h3>
          <p>Pão, hambúrguer, queijo, alface e tomate.</p>
          <p class="preco">R$ 18,00</p>
        </article>
        <article class="cartao">
          <h3>X-Bacon</h3>
          <p>Pão, hambúrguer, queijo e bacon crocante.</p>
          <p class="preco">R$ 22,00</p>
        </article>
        <article class="cartao">
          <h3>Misto quente</h3>
          <p>Pão de forma, presunto e queijo na chapa.</p>
          <p class="preco">R$ 10,00</p>
        </article>
      </div>
    </section>

    <section id="bebidas">
      <h2>Bebidas</h2>
      <div class="cartoes">
        <article class="cartao">
          <h3>Suco de laranja</h3>
          <p>Natural, 400 ml.</p>
          <p class="preco">R$ 9,00</p>
        </article>
        <article class="cartao">
          <h3>Refrigerante lata</h3>
          <p>350 ml.</p>
          <p class="preco">R$ 6,00</p>
        </article>
      </div>
    </section>
  </main>

  <footer class="rodape">
    <p>Pedidos: <a href="tel:+5511900000000">(11) 90000-0000</a> · Seg. a sáb., das 11h às 22h</p>
  </footer>
</body>
</html>
```

## O CSS (`style.css`)

```css
:root {
  --cor-principal: #e8781e;
  --cor-fundo: #fff8f1;
  --cor-texto: #2b2b2b;
  --raio: 12px;
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  font-family: "Segoe UI", Arial, sans-serif;
  line-height: 1.5;
  color: var(--cor-texto);
  background-color: var(--cor-fundo);
}

.topo {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  background-color: var(--cor-principal);
  color: white;
}
.topo h1 { margin: 0; font-size: 1.5rem; }

.menu { display: flex; gap: 16px; list-style: none; margin: 0; padding: 0; }
.menu a { color: white; text-decoration: none; font-weight: 600; }
.menu a:hover { text-decoration: underline; }

main { max-width: 960px; margin: 0 auto; padding: 0 16px 32px; }
h2 { color: var(--cor-principal); }

.cartoes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
.cartao {
  background-color: white;
  padding: 16px;
  border-radius: var(--raio);
  box-shadow: 0 2px 8px rgb(0 0 0 / 10%);
}
.cartao h3 { margin-top: 0; }
.preco { font-size: 1.25rem; font-weight: 700; color: var(--cor-principal); }

.rodape { text-align: center; padding: 16px; }
.rodape a { color: var(--cor-principal); }
```

!!! tip "Teste no “celular”"
    Abra com o Live Server, tecle `F12` ➔ `Ctrl + Shift + M` e escolha um celular. Os cartões passam para uma coluna e o menu desce para baixo do nome, sem nenhuma media query: quem faz isso é o `auto-fit` do Grid e o `flex-wrap` do cabeçalho.

---

## Entrega

1. A pasta do projeto compactada (`index.html` + `style.css`).
2. Dois prints: tela de computador e modo celular do `F12`.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| HTML | Semântico e válido no W3C; pelo menos duas seções e cinco itens |
| CSS separado | Um `style.css` ligado com `<link>`, com variáveis em `:root` |
| Layout | Cabeçalho com Flexbox; cartões com Grid que se ajusta ao celular |
| Legibilidade | Bom contraste; preço em destaque; nada colado nas bordas |

---

## Exercícios extras

### Básico (fixação)

Troque a identidade da lanchonete mudando **só** as variáveis: deixe-a verde.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Em `:root`, troque `--cor-principal: #e8781e;` por um verde, como `#2e7d32`. Cabeçalho, títulos, preços e link mudam juntos: é para isso que servem as variáveis.

### Intermediário (aplicação)

Marque o X-Bacon como **mais pedido** com uma etiqueta colorida no canto do cartão.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    No HTML, dentro do cartão: `<span class="etiqueta">Mais pedido</span>`. No CSS:
    ```css
    .etiqueta {
      display: inline-block;
      background-color: var(--cor-principal);
      color: white;
      font-size: 0.8rem;
      padding: 2px 8px;
      border-radius: 999px;
    }
    ```

### Avançado (desafio)

Faça os cartões “subirem” um pouco quando o mouse passa por cima, com uma transição suave.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```css
    .cartao { transition: transform 0.2s, box-shadow 0.2s; }
    .cartao:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 16px rgb(0 0 0 / 15%);
    }
    ```
    `transition` diz **quais** propriedades animam e em quanto tempo; o `:hover` diz o estado final.

---

## 💡 Resumo

- Variáveis em `:root` deixam cores e medidas num lugar só.
- Flexbox no cabeçalho, Grid com `auto-fit` nos cartões: responsivo quase de graça.
- Teste sempre no modo celular do `F12`.

## ➡️ Próximo passo

Você terminou o **Módulo 02**. Volte ao [índice do módulo](index.md) e confira o checklist. O **Módulo 03 — JavaScript**, que vai dar vida às páginas, está em produção.
