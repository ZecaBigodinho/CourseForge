# 01 — Variáveis, condições e laços

> **Curso:** Desenvolvimento Web  
> **Módulo:** 03 — JavaScript  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Ligar um arquivo **JavaScript** à página e usar o **Console**.
- Guardar valores em **variáveis** com `let` e `const`.
- Reconhecer os **tipos**: texto, número, booleano.
- Tomar decisões com `if`/`else` e repetir com `for`.

## Pré-requisitos

- [Módulo 02](../modulo_02_css/index.md) completo.

---

## Ligar o JavaScript e abrir o Console

Crie `script.js` ao lado do `index.html` e ligue-o **no fim do `<body>`**, ou no `<head>` com `defer`:

```html
<script src="script.js" defer></script>
```

O `defer` faz o script rodar **depois** que o HTML carregou, para ele encontrar os elementos da página.

No `script.js`:

```js
console.log("Olá do JavaScript!");
```

Abra a página, tecle `F12` ➔ guia **Console**: a mensagem aparece lá. O Console também mostra os **erros**, em vermelho, com a linha onde aconteceram. Ele é seu melhor amigo nesta disciplina.

---

## Variáveis

```js
const nome = "Ana";
let pontos = 0;
pontos = pontos + 10;
console.log(nome, pontos); // Ana 10
```

| Palavra | Quando usar |
|---|---|
| `const` | O valor **não** vai ser trocado (use por padrão) |
| `let` | O valor **vai** mudar (contadores, totais) |
| `var` | Forma antiga: evite |

Nomes de variáveis: sem espaço e sem acento, começando por letra, no estilo `precoTotal` (*camelCase*).

### Tipos

| Tipo | Exemplo |
|---|---|
| Texto (`string`) | `"Ana"`, `'pão'`, `` `Olá, ${nome}` `` |
| Número (`number`) | `18`, `9.5` (decimal com **ponto**) |
| Booleano (`boolean`) | `true`, `false` |
| Vazio | `null`, `undefined` |

A crase cria um **template string**, que encaixa valores no texto:

```js
const preco = 18;
console.log(`O X-Salada custa R$ ${preco.toFixed(2)}`); // O X-Salada custa R$ 18.00
```

!!! warning "Texto + número"
    `"5" + 2` dá `"52"` (junta os textos), mas `"5" * 2` dá `10`. O que vem de um campo de formulário é **sempre texto**: converta com `Number(valor)` antes de fazer contas.

---

## Condições

```js
const nota = 6.5;

if (nota >= 7) {
  console.log("Aprovado");
} else if (nota >= 5) {
  console.log("Recuperação");
} else {
  console.log("Reprovado");
}
```

| Operador | Significa |
|---|---|
| `===` / `!==` | Igual / diferente (sempre com **três** sinais) |
| `>`, `<`, `>=`, `<=` | Maior, menor, maior ou igual, menor ou igual |
| `&&` | E (as duas condições) |
| `\|\|` | OU (pelo menos uma) |
| `!` | NÃO (inverte) |

---

## Laços

**`for` clássico**, quando você sabe quantas vezes repetir:

```js
for (let i = 1; i <= 5; i++) {
  console.log(`Volta ${i}`);
}
```

**`for…of`**, para percorrer uma lista:

```js
const frutas = ["maçã", "banana", "uva"];
for (const fruta of frutas) {
  console.log(fruta);
}
```

**`while`**, enquanto uma condição for verdadeira:

```js
let saldo = 100;
while (saldo >= 30) {
  saldo = saldo - 30;
}
console.log(saldo); // 10
```

!!! danger "Laço infinito"
    Se a condição do `while` nunca ficar falsa, a página trava. Feche a aba e confira se a variável está mudando dentro do laço.

---

## Exercícios

### Básico (fixação)

Guarde o seu nome e o ano em que nasceu em variáveis e mostre no Console: “Ana tem 17 anos em 2026”.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```js
    const nome = "Ana";
    const anoNascimento = 2009;
    const anoAtual = 2026;
    console.log(`${nome} tem ${anoAtual - anoNascimento} anos em ${anoAtual}`);
    ```

### Intermediário (aplicação)

Dado um `total` de compra, aplique 10% de desconto se for de R$ 100 ou mais, e mostre o valor final com duas casas.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```js
    const total = 120;
    let final = total;
    if (total >= 100) {
      final = total * 0.9;
    }
    console.log(`Total a pagar: R$ ${final.toFixed(2)}`); // R$ 108.00
    ```

### Avançado (desafio)

Mostre a tabuada do 7 (de 1 a 10) e, ao lado de cada resultado, escreva “par” ou “ímpar”.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```js
    for (let i = 1; i <= 10; i++) {
      const r = 7 * i;
      const tipo = r % 2 === 0 ? "par" : "ímpar";
      console.log(`7 x ${i} = ${r} (${tipo})`);
    }
    ```
    `%` é o **resto da divisão**: resto 0 por 2 significa par. `condição ? a : b` é um `if` curto (operador ternário).

---

## 💡 Resumo

- `<script src="script.js" defer>`; `console.log` e erros na guia **Console** (`F12`).
- `const` por padrão, `let` quando muda; texto, número e booleano.
- `if`/`else if`/`else` com `===`, `&&`, `||`.
- `for`, `for…of` e `while` para repetir.

## ➡️ Próximo passo

Na **[aula 02](02_funcoes_e_arrays.md)** você organiza o código em funções e trabalha com listas.
