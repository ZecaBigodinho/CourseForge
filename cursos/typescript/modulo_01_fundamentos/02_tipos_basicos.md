# 02 — Tipos básicos e inferência

> **Curso:** TypeScript  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Usar os tipos `string`, `number`, `boolean`, `null` e `undefined`.
- Entender a **inferência**: quando o TypeScript descobre o tipo sozinho.
- Saber por que evitar `any` e quando usar `unknown`.
- Converter valores com segurança (texto ➔ número).

## Pré-requisitos

- [Aula 01](01_primeiro_programa.md) deste módulo.

---

## Os tipos básicos

```ts
const nome: string = "Ana";
const preco: number = 18.5;      // inteiros e decimais são todos number
const ativo: boolean = true;
let apelido: string | null = null; // texto OU null (mais na aula de uniões)
```

| Tipo | Valores |
|---|---|
| `string` | Textos: `"Ana"`, `'pão'`, `` `Olá ${nome}` `` |
| `number` | Números: `18`, `9.5`, `-3` |
| `boolean` | `true` ou `false` |
| `null` / `undefined` | “Sem valor” |

Os tipos são escritos em **minúsculas**. `String` com maiúscula é outra coisa: não use.

---

## Inferência: nem sempre precisa escrever o tipo

Quando você dá um valor na hora de criar a variável, o TypeScript **deduz** o tipo:

```ts
let total = 0;          // o TypeScript sabe: number
total = total + 18;     // ok
// total = "dezoito";   // erro: o tipo 'string' não pode ser atribuído ao tipo 'number'
```

No VS Code, pare o mouse sobre `total` e veja `let total: number`.

!!! tip "Regra prática"
    Deixe a inferência trabalhar nas **variáveis com valor inicial**. Escreva o tipo nos **parâmetros de funções** (aula 04) e quando a variável começa vazia (`let nome: string;`).

Com `const`, o tipo fica ainda mais exato: `const turno = "manhã";` tem o tipo `"manhã"`, e não só `string`, porque o valor nunca muda. Isso será útil no Módulo 02.

---

## `any` e `unknown`

`any` desliga a conferência: a variável aceita qualquer coisa e você perde toda a ajuda.

```ts
let qualquer: any = "texto";
qualquer.toFixed(2); // o compilador aceita, mas quebra ao rodar
```

`unknown` também aceita qualquer valor, mas **obriga a conferir** antes de usar:

```ts
let valor: unknown = "texto";
if (typeof valor === "number") {
  console.log(valor.toFixed(2)); // aqui o TypeScript sabe que é número
}
```

!!! warning "Evite `any`"
    Cada `any` é um buraco por onde os erros passam. Se você não sabe o tipo (dados de fora, por exemplo), use `unknown` e confira com `typeof`.

---

## Converter texto em número

Valores de formulário e de `prompt` chegam como texto. O TypeScript obriga a converter:

```ts
const digitado: string = "7.5";
const nota: number = Number(digitado);

if (Number.isNaN(nota)) {
  console.log("Não é um número válido.");
} else {
  console.log(nota + 1); // 8.5
}
```

`Number("abc")` dá `NaN` (*Not a Number*), que também é do tipo `number`. Por isso confira com `Number.isNaN`.

---

## Exercícios

### Básico (fixação)

Declare as variáveis de um produto: nome, preço, quantidade em estoque e se está à venda, deixando a inferência agir. Passe o mouse sobre cada uma no VS Code e confira o tipo.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    const produto = "Caderno";   // string
    const preco = 12.9;          // number
    let estoque = 40;            // number
    let aVenda = true;           // boolean
    ```

### Intermediário (aplicação)

Qual destas linhas dá erro no TypeScript e por quê?

```ts
let quantidade = 3;
quantidade = quantidade + 1;
quantidade = "quatro";
let mensagem: string;
mensagem = 10;
```

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    A **3ª** (`quantidade` foi inferida como `number` e não aceita texto) e a **5ª** (`mensagem` foi declarada `string` e não aceita número). As outras estão certas.

### Avançado (desafio)

Escreva o código que recebe `entrada: unknown` e mostra o dobro se for número, o texto em maiúsculas se for string, e “tipo não suportado” no resto.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    function processar(entrada: unknown): void {
      if (typeof entrada === "number") {
        console.log(entrada * 2);
      } else if (typeof entrada === "string") {
        console.log(entrada.toUpperCase());
      } else {
        console.log("tipo não suportado");
      }
    }
    processar(21);      // 42
    processar("ana");   // ANA
    processar(true);    // tipo não suportado
    ```
    Dentro de cada `if`, o TypeScript **estreita** o tipo: isso se chama *narrowing* (Módulo 02).

---

## 💡 Resumo

- `string`, `number`, `boolean`, `null`, `undefined`, sempre em minúsculas.
- Com valor inicial, a **inferência** descobre o tipo; escreva o tipo quando não houver valor.
- `any` desliga a ajuda; `unknown` obriga a conferir com `typeof`.
- Texto ➔ número com `Number()` e confira `Number.isNaN`.

## ➡️ Próximo passo

Na **[aula 03](03_arrays_tuplas_e_objetos.md)** você tipa listas e objetos.
