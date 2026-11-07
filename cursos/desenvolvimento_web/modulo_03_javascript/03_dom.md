# 03 — DOM: mexer na página pelo código

> **Curso:** Desenvolvimento Web  
> **Módulo:** 03 — JavaScript  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que é o **DOM**.
- Encontrar elementos com `querySelector` e `querySelectorAll`.
- Mudar **texto**, **atributos** e **classes** de um elemento.
- **Criar** elementos e colocá-los na página a partir de um array.

## Pré-requisitos

- [Aula 02](02_funcoes_e_arrays.md) deste módulo.

---

## O que é o DOM

Quando o navegador lê o HTML, ele monta na memória uma **árvore de objetos**, um para cada tag: o **DOM** (*Document Object Model*). O JavaScript não mexe no arquivo `.html`: ele mexe nessa árvore, e o navegador redesenha a página na hora. A guia **Elementos** do `F12` mostra o DOM ao vivo.

---

## Encontrar elementos

```html
<h1 id="titulo">Lanchonete do Bairro</h1>
<p class="preco">R$ 18,00</p>
<p class="preco">R$ 22,00</p>
```

```js
const titulo = document.querySelector("#titulo");      // o primeiro que combinar
const precos = document.querySelectorAll(".preco");    // todos (uma lista)
console.log(precos.length); // 2
```

O seletor é **o mesmo do CSS**: `#id`, `.classe`, `tag`, `nav a`…

!!! warning "Deu `null`?"
    `querySelector` devolve `null` quando não acha nada. As causas mais comuns: seletor escrito errado ou o script rodando **antes** do HTML carregar (falta o `defer`).

---

## Mudar o que já existe

```js
titulo.textContent = "Lanchonete do Bairro — aberta!";   // troca o texto

const foto = document.querySelector("img");
foto.src = "imagens/x-bacon.jpg";                         // troca um atributo
foto.alt = "X-Bacon com fritas";

titulo.classList.add("destaque");     // acrescenta uma classe
titulo.classList.remove("destaque");  // tira
titulo.classList.toggle("destaque");  // põe se não tem, tira se tem
```

!!! tip "Estilo pelo CSS, não pelo JavaScript"
    Dá para mudar `titulo.style.color = "red"`, mas o melhor é criar uma classe no CSS (`.destaque { … }`) e só **trocar a classe** pelo JavaScript. Cada linguagem fica com o seu papel.

---

## Criar elementos a partir de dados

```html
<ul id="lista-cardapio"></ul>
```

```js
const cardapio = [
  { nome: "X-Salada", preco: 18 },
  { nome: "X-Bacon", preco: 22 },
];

const lista = document.querySelector("#lista-cardapio");

for (const item of cardapio) {
  const li = document.createElement("li");
  li.textContent = `${item.nome} — R$ ${item.preco.toFixed(2)}`;
  lista.append(li);
}
```

1. `createElement("li")` cria a tag (ainda fora da página).
2. `textContent` coloca o texto.
3. `append` põe dentro do elemento escolhido, no fim.

Para apagar: `elemento.remove()`. Para esvaziar uma lista inteira: `lista.innerHTML = ""`.

!!! danger "Cuidado com `innerHTML` e texto do usuário"
    `innerHTML` interpreta o texto como HTML. Se você colocar ali algo que o **visitante digitou**, ele pode injetar código na página. Para texto, use sempre `textContent`.

---

## Exercícios

### Básico (fixação)

Numa página com `<p id="saudacao"></p>`, escreva “Bom dia, Ana!” pelo JavaScript.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```js
    document.querySelector("#saudacao").textContent = "Bom dia, Ana!";
    ```

### Intermediário (aplicação)

Escreva “Bom dia”, “Boa tarde” ou “Boa noite” conforme a hora do computador.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```js
    const hora = new Date().getHours();
    let texto = "Boa noite";
    if (hora >= 5 && hora < 12) texto = "Bom dia";
    else if (hora >= 12 && hora < 18) texto = "Boa tarde";
    document.querySelector("#saudacao").textContent = `${texto}, Ana!`;
    ```

### Avançado (desafio)

A partir do array `cardapio`, crie para cada item um `<article class="cartao">` com `<h3>` (nome) e `<p class="preco">` (preço) dentro de uma `<div class="cartoes">`, reaproveitando o CSS do Módulo 02.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```js
    const area = document.querySelector(".cartoes");
    for (const item of cardapio) {
      const cartao = document.createElement("article");
      cartao.classList.add("cartao");
      const h3 = document.createElement("h3");
      h3.textContent = item.nome;
      const preco = document.createElement("p");
      preco.classList.add("preco");
      preco.textContent = `R$ ${item.preco.toFixed(2)}`;
      cartao.append(h3, preco);
      area.append(cartao);
    }
    ```
    Agora o cardápio vem dos **dados**: para acrescentar um lanche, basta um item novo no array.

---

## 💡 Resumo

- DOM = a árvore de objetos que o navegador monta a partir do HTML.
- `querySelector` (um) e `querySelectorAll` (todos), com seletores de CSS.
- `textContent`, atributos (`src`, `alt`) e `classList` mudam o que existe.
- `createElement` + `append` criam elementos; `textContent` para texto do usuário.

## ➡️ Próximo passo

Na **[aula 04](04_eventos_e_formularios.md)** a página passa a reagir ao visitante.
