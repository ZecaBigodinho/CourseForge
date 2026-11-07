# 02 — DOM com tipos

> **Curso:** TypeScript  
> **Módulo:** 03 — TypeScript no navegador  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Entender por que `querySelector` devolve `Element | null`.
- Obter o tipo certo de elemento (`HTMLInputElement`, `HTMLFormElement`…) com **`instanceof`**.
- Escrever uma função auxiliar que pega elementos com segurança.
- Tipar **eventos** (`SubmitEvent`, `MouseEvent`).

## Pré-requisitos

- [Aula 01](01_modulos_e_tsconfig.md) deste módulo.

---

## O problema

```ts
const campo = document.querySelector("#nome");
// campo.value = "Ana";
// erro: 'campo' é possivelmente 'null'.
// e mesmo sem o null: a propriedade 'value' não existe no tipo 'Element'.
```

O TypeScript não sabe:

1. se o elemento **existe** (pode ser `null`);
2. **que tipo** de elemento é: `#nome` pode ser um `<p>`, que não tem `value`.

---

## A solução: conferir com `instanceof`

```ts
const campo = document.querySelector("#nome");
if (campo instanceof HTMLInputElement) {
  campo.value = "Ana";      // aqui é HTMLInputElement: tem value
}
```

`instanceof` resolve os dois problemas de uma vez: se for `null` ou outro tipo de elemento, o `if` é falso.

| Tag | Tipo |
|---|---|
| `<input>` | `HTMLInputElement` |
| `<form>` | `HTMLFormElement` |
| `<button>` | `HTMLButtonElement` |
| `<ul>` / `<li>` | `HTMLUListElement` / `HTMLLIElement` |
| `<p>` | `HTMLParagraphElement` |
| qualquer um | `HTMLElement` |

!!! info "E o `as` e o `!`?"
    Você vai ver por aí `document.querySelector("#nome") as HTMLInputElement` ou `…!`. Os dois **mandam o compilador acreditar** sem conferir. Se o HTML mudar, o erro só aparece rodando. Neste curso, conferimos com `instanceof`.

### Uma função auxiliar

Conferir cada elemento com `if` cansa. Esta função faz a conferência e **para o programa com uma mensagem clara** se o HTML estiver errado:

```ts
function pegar<T extends HTMLElement>(seletor: string, tipo: { new (): T }): T {
  const el = document.querySelector(seletor);
  if (!(el instanceof tipo)) {
    throw new Error(`Elemento ${seletor} não encontrado`);
  }
  return el;
}

const campo = pegar("#nome", HTMLInputElement);   // HTMLInputElement
const form = pegar("#cadastro", HTMLFormElement);  // HTMLFormElement
campo.value = "Ana";                               // sem if, sem !, sem as
```

Ela usa um **generic** (Módulo 02): você passa a classe (`HTMLInputElement`) e recebe um elemento daquele tipo.

---

## Eventos com tipos

```ts
form.addEventListener("submit", (evento: SubmitEvent) => {
  evento.preventDefault();
  console.log(`Olá, ${campo.value}`);
});

campo.addEventListener("input", () => {
  console.log(campo.value.length);
});
```

Na maioria das vezes, o TypeScript **descobre** o tipo do evento pelo nome (`"submit"` ➔ `SubmitEvent`, `"click"` ➔ `MouseEvent`, `"keydown"` ➔ `KeyboardEvent`). Escrever o tipo é opcional, mas deixa o código mais claro.

!!! tip "`evento.target` não é o elemento que você imagina"
    `evento.target` tem o tipo `EventTarget | null`, porque o evento pode ter nascido num filho do elemento. Se precisar dele, confira com `instanceof`. Quase sempre é mais simples usar a variável que você já tem (`campo`).

---

## Exercícios

### Básico (fixação)

Com um `<p id="saudacao">` na página, escreva “Olá, Ana!” nele usando `instanceof`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    const p = document.querySelector("#saudacao");
    if (p instanceof HTMLParagraphElement) {
      p.textContent = "Olá, Ana!";
    }
    ```

### Intermediário (aplicação)

Use a função `pegar` para fazer um contador: um botão `#mais` que aumenta um número mostrado em `#valor`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    const botao = pegar("#mais", HTMLButtonElement);
    const valor = pegar("#valor", HTMLElement);
    let contagem = 0;
    botao.addEventListener("click", () => {
      contagem++;
      valor.textContent = String(contagem);
    });
    ```
    `textContent` aceita só texto: por isso o `String(contagem)`.

### Avançado (desafio)

Troque, no HTML, o `<input id="nome">` por um `<p id="nome">` e rode a página com a função `pegar`. O que acontece? Por que isso é melhor do que usar `as HTMLInputElement`?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    A página para logo no início, e o Console mostra `Error: Elemento #nome não encontrado`, apontando a linha. Com `as`, o código seguiria rodando, e o erro apareceria depois, em outro lugar (por exemplo, `value` vazio ou `undefined`), muito mais difícil de achar. Falhar cedo e com mensagem clara economiza tempo de depuração.

---

## 💡 Resumo

- `querySelector` devolve `Element | null`: confira antes de usar.
- `instanceof HTMLInputElement` confere a existência e o tipo de uma vez.
- A função `pegar(seletor, Tipo)` evita `as` e `!` no projeto inteiro.
- O tipo do evento costuma ser inferido; `evento.target` precisa de conferência.

## ➡️ Próximo passo

Na **[aula 03](03_fetch_tipado.md)** você busca dados de APIs com tipos.
