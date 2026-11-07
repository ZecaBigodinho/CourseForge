# 02 — Uniões, literais e narrowing

> **Curso:** TypeScript  
> **Módulo:** 02 — Modelando dados  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Usar **uniões** (`string | number`) e **tipos literais** (`"pix" | "cartao"`).
- **Estreitar** tipos (*narrowing*) com `typeof`, `in` e comparações.
- Criar **uniões discriminadas** e tratá-las com `switch`.
- Garantir que **todos os casos** foram tratados com `never`.

## Pré-requisitos

- [Aula 01](01_type_e_interface.md) deste módulo.

---

## Uniões e literais

Uma **união** diz que um valor pode ser de um tipo **ou** de outro:

```ts
let codigo: string | number;
codigo = 123;    // ok
codigo = "A12";  // ok
```

Um **tipo literal** é um valor exato. Juntos, eles criam listas fechadas de opções:

```ts
type Turno = "manhã" | "tarde" | "noite";
let turno: Turno = "manhã";
// turno = "madrugada";  // erro: não está na lista
```

---

## Narrowing (estreitamento)

Com uma união, o TypeScript só deixa usar o que é comum aos dois tipos. Depois de um teste, ele **estreita** o tipo:

```ts
function formatarCodigo(codigo: string | number): string {
  if (typeof codigo === "number") {
    return codigo.toString().padStart(5, "0"); // aqui é number
  }
  return codigo.toUpperCase();                  // aqui só pode ser string
}

formatarCodigo(42);    // "00042"
formatarCodigo("a12"); // "A12"
```

| Teste | Estreita para |
|---|---|
| `typeof x === "string"` | Primitivos (`string`, `number`, `boolean`) |
| `Array.isArray(x)` | Arrays |
| `"propriedade" in x` | O objeto que tem aquela propriedade |
| `x === "pix"` | O literal comparado |

---

## Uniões discriminadas

O padrão mais útil do TypeScript: vários formatos de objeto, cada um com uma propriedade **em comum** (o *discriminante*) que diz qual é qual:

```ts
type Pagamento =
  | { forma: "pix"; chave: string }
  | { forma: "cartao"; parcelas: number }
  | { forma: "dinheiro"; troco: number };

function descrever(p: Pagamento): string {
  switch (p.forma) {
    case "pix":
      return `Pix para ${p.chave}`;          // aqui p tem chave
    case "cartao":
      return `Cartão em ${p.parcelas}x`;     // aqui p tem parcelas
    case "dinheiro":
      return `Dinheiro, troco para ${p.troco}`;
  }
}
```

Dentro de cada `case`, o TypeScript sabe exatamente qual formato é: tentar usar `p.parcelas` no caso `"pix"` dá erro. Assim, um pagamento em pix **com** parcelas é um estado **impossível** de escrever.

### Conferir que nenhum caso ficou de fora

```ts
function taxa(p: Pagamento): number {
  switch (p.forma) {
    case "pix": return 0;
    case "cartao": return p.parcelas > 1 ? 0.05 : 0.02;
    case "dinheiro": return 0;
    default: {
      const nuncaAcontece: never = p;
      return nuncaAcontece;
    }
  }
}
```

Se amanhã alguém acrescentar `{ forma: "boleto" }` à união, o `default` deixa de compilar e aponta exatamente a função que precisa tratar o boleto.

---

## Exercícios

### Básico (fixação)

Crie `type Tamanho = "P" | "M" | "G"` e uma função `preco(t: Tamanho): number` (P = 10, M = 14, G = 18).

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    type Tamanho = "P" | "M" | "G";
    function preco(t: Tamanho): number {
      if (t === "P") return 10;
      if (t === "M") return 14;
      return 18;
    }
    ```
    `preco("GG")` não compila.

### Intermediário (aplicação)

Escreva `total(valor: number | number[]): number`, que soma os itens quando recebe um array e devolve o próprio número caso contrário.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    function total(valor: number | number[]): number {
      if (Array.isArray(valor)) {
        return valor.reduce((s, n) => s + n, 0);
      }
      return valor;
    }
    total(5);          // 5
    total([5, 10, 2]); // 17
    ```

### Avançado (desafio)

Acrescente `{ forma: "boleto"; vencimento: string }` ao tipo `Pagamento` da aula. Quais funções deixam de compilar e por quê?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    A função **`taxa`** deixa de compilar: no `default`, `p` agora pode ser o boleto, que não é `never` (erro TS2322). A função `descrever` também acusa erro, porque nem todo caminho devolve uma `string` (TS2366). Os dois erros apontam exatamente onde o boleto precisa ser tratado: é o compilador ajudando a não esquecer um caso.

---

## 💡 Resumo

- União `A | B`; literais criam listas fechadas (`"pix" | "cartao"`).
- `typeof`, `Array.isArray`, `in` e `===` estreitam o tipo.
- Uniões discriminadas + `switch` = estados impossíveis não compilam.
- `never` no `default` garante que todos os casos foram tratados.

## ➡️ Próximo passo

Na **[aula 03](03_opcionais_e_null.md)** você lida com valores que podem faltar.
