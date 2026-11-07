# 02 — Funções e arrays

> **Curso:** Desenvolvimento Web  
> **Módulo:** 03 — JavaScript  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar **funções** com parâmetros e `return`, inclusive em forma de **arrow function**.
- Guardar listas em **arrays** e usar `push`, `length` e índices.
- Transformar listas com `map`, `filter` e `reduce`.
- Representar coisas com **objetos** (`{ nome: "X-Salada", preco: 18 }`).

## Pré-requisitos

- [Aula 01](01_variaveis_condicoes_e_lacos.md) deste módulo.

---

## Funções

Uma função é um bloco de código com nome, que você escreve uma vez e usa quantas vezes quiser:

```js
function calcularMedia(n1, n2) {
  return (n1 + n2) / 2;
}

console.log(calcularMedia(8, 9));   // 8.5
console.log(calcularMedia(5, 6.5)); // 5.75
```

- `n1` e `n2` são **parâmetros**: os valores que a função recebe.
- `return` devolve o resultado e **encerra** a função.

A mesma função em forma de **arrow function** (seta), muito usada no JavaScript moderno:

```js
const calcularMedia = (n1, n2) => (n1 + n2) / 2;
```

!!! tip "Uma função, uma tarefa"
    Dê nomes que digam o que a função faz (`calcularMedia`, `formatarPreco`) e mantenha cada uma curta. Fica mais fácil testar e reaproveitar.

---

## Arrays (listas)

```js
const notas = [8, 6.5, 9];
console.log(notas[0]);      // 8  (o primeiro é o índice 0)
console.log(notas.length);  // 3
notas.push(7);              // acrescenta no fim
console.log(notas);         // [8, 6.5, 9, 7]
```

### `map`, `filter` e `reduce`

Em vez de laços, os arrays têm métodos que recebem uma função:

```js
const precos = [18, 22, 10];

const comTaxa = precos.map((p) => p * 1.1);      // transforma cada item
const baratos = precos.filter((p) => p <= 18);   // fica com quem passa no teste
const total = precos.reduce((soma, p) => soma + p, 0); // junta tudo num valor

console.log(baratos); // [18, 10]
console.log(total);   // 50
```

| Método | Devolve | Pense como |
|---|---|---|
| `map` | Lista **do mesmo tamanho**, transformada | “Para cada item, faça…” |
| `filter` | Lista **menor**, só com quem passou | “Fique só com…” |
| `reduce` | **Um valor** | “Some / junte tudo” |
| `find` | **O primeiro** item que passa | “Ache o…” |

---

## Objetos

Um objeto agrupa informações sobre uma coisa, em pares **chave: valor**:

```js
const lanche = {
  nome: "X-Salada",
  preco: 18,
  vegetariano: false,
};

console.log(lanche.nome);  // X-Salada
lanche.preco = 19;         // altera
```

Arrays de objetos são o formato mais comum de dados na web:

```js
const cardapio = [
  { nome: "X-Salada", preco: 18 },
  { nome: "X-Bacon", preco: 22 },
  { nome: "Misto quente", preco: 10 },
];

const nomes = cardapio.map((item) => item.nome);
console.log(nomes); // ["X-Salada", "X-Bacon", "Misto quente"]
```

!!! info "JSON"
    Quando um site busca dados de um servidor (Módulo 04), eles chegam em **JSON**, um texto com exatamente esse formato de objetos e arrays.

---

## Exercícios

### Básico (fixação)

Escreva a função `formatarPreco(valor)` que devolve, por exemplo, `"R$ 18.00"` para `18`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```js
    function formatarPreco(valor) {
      return `R$ ${valor.toFixed(2)}`;
    }
    console.log(formatarPreco(18)); // R$ 18.00
    ```
    Para o formato brasileiro (`R$ 18,00`), use `valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })`.

### Intermediário (aplicação)

Com o array `cardapio` da aula, calcule o **total** de um pedido com um item de cada.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```js
    const total = cardapio.reduce((soma, item) => soma + item.preco, 0);
    console.log(total); // 50
    ```

### Avançado (desafio)

Ainda com o `cardapio`, mostre no Console só os nomes dos lanches de até R$ 20, em ordem alfabética.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```js
    const resultado = cardapio
      .filter((item) => item.preco <= 20)
      .map((item) => item.nome)
      .sort();
    console.log(resultado); // ["Misto quente", "X-Salada"]
    ```
    Os métodos podem ser **encadeados**: cada um recebe o resultado do anterior.

---

## 💡 Resumo

- Funções recebem **parâmetros** e devolvem com `return`; arrow function: `(a, b) => a + b`.
- Arrays começam no índice **0**; `push` acrescenta; `length` conta.
- `map` transforma, `filter` filtra, `reduce` junta, `find` acha.
- Objetos agrupam dados em `chave: valor`; arrays de objetos = dados da web.

## ➡️ Próximo passo

Na **[aula 03](03_dom.md)** você usa o JavaScript para mudar a página.
