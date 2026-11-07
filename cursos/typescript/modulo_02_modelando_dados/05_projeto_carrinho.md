# 05 — Projeto do módulo: carrinho de compras

> **Curso:** TypeScript  
> **Módulo:** 02 — Modelando dados  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final deste projeto, você terá:

- Um **carrinho de compras** tipado que calcula subtotal, desconto, frete, acréscimo e total.
- **Cupons** e **formas de pagamento** modelados como uniões discriminadas.
- Regras de negócio que o compilador ajuda a manter certas.

## Pré-requisitos

- Aulas [01](01_type_e_interface.md) a [04](04_generics.md) deste módulo.

---

## As regras (da papelaria inventada)

- Três tipos de **cupom**: percentual (ex.: 10%), valor fixo (ex.: R$ 20) ou frete grátis. No máximo um por compra.
- **Frete** de R$ 15, grátis a partir de R$ 200 (depois do desconto) ou com o cupom de frete grátis.
- **Pix** sem acréscimo; **cartão** à vista sem acréscimo e parcelado com 5%.

---

## O código (`src/carrinho.ts`)

```ts
type Produto = {
  readonly id: number;
  nome: string;
  preco: number;
};

type Item = { produto: Produto; quantidade: number };

type Cupom =
  | { tipo: "percentual"; codigo: string; percentual: number }
  | { tipo: "valorFixo"; codigo: string; valor: number }
  | { tipo: "freteGratis"; codigo: string };

type Pagamento =
  | { forma: "pix" }
  | { forma: "cartao"; parcelas: number };

const FRETE = 15;

function subtotal(itens: Item[]): number {
  return itens.reduce((soma, i) => soma + i.produto.preco * i.quantidade, 0);
}

function desconto(valor: number, cupom?: Cupom): number {
  if (!cupom) return 0;
  switch (cupom.tipo) {
    case "percentual":
      return valor * (cupom.percentual / 100);
    case "valorFixo":
      return Math.min(cupom.valor, valor);
    case "freteGratis":
      return 0;
  }
}

function frete(valor: number, cupom?: Cupom): number {
  if (cupom?.tipo === "freteGratis" || valor >= 200) return 0;
  return FRETE;
}

function acrescimo(valor: number, pagamento: Pagamento): number {
  if (pagamento.forma === "cartao" && pagamento.parcelas > 1) {
    return valor * 0.05;
  }
  return 0;
}

function brl(valor: number): string {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function resumo(itens: Item[], pagamento: Pagamento, cupom?: Cupom): string {
  const sub = subtotal(itens);
  const desc = desconto(sub, cupom);
  const fre = frete(sub - desc, cupom);
  const acr = acrescimo(sub - desc + fre, pagamento);
  const total = sub - desc + fre + acr;
  const linhas = itens.map((i) => `${i.quantidade}x ${i.produto.nome.padEnd(10)} ${brl(i.produto.preco * i.quantidade)}`);
  return [
    ...linhas,
    `Subtotal:  ${brl(sub)}`,
    `Desconto: -${brl(desc)}${cupom ? ` (${cupom.codigo})` : ""}`,
    `Frete:     ${brl(fre)}`,
    `Acréscimo: ${brl(acr)}`,
    `TOTAL:     ${brl(total)}`,
  ].join("\n");
}

const caderno: Produto = { id: 1, nome: "Caderno", preco: 12.9 };
const caneta: Produto = { id: 2, nome: "Caneta", preco: 2.5 };
const mochila: Produto = { id: 3, nome: "Mochila", preco: 89.9 };

const carrinho: Item[] = [
  { produto: caderno, quantidade: 3 },
  { produto: caneta, quantidade: 4 },
  { produto: mochila, quantidade: 1 },
];

console.log(resumo(carrinho, { forma: "pix" }, { tipo: "percentual", codigo: "VOLTA10", percentual: 10 }));
console.log("---");
console.log(resumo(carrinho, { forma: "cartao", parcelas: 3 }));
```

Compile e rode (`npx tsc` e `node dist/carrinho.js`):

```text
3x Caderno    R$ 38,70
4x Caneta     R$ 10,00
1x Mochila    R$ 89,90
Subtotal:  R$ 138,60
Desconto: -R$ 13,86 (VOLTA10)
Frete:     R$ 15,00
Acréscimo: R$ 0,00
TOTAL:     R$ 139,74
---
3x Caderno    R$ 38,70
4x Caneta     R$ 10,00
1x Mochila    R$ 89,90
Subtotal:  R$ 138,60
Desconto: -R$ 0,00
Frete:     R$ 15,00
Acréscimo: R$ 7,68
TOTAL:     R$ 161,28
```

| Recurso do módulo | Onde aparece |
|---|---|
| Uniões discriminadas (aula 02) | `Cupom` (pelo `tipo`) e `Pagamento` (pela `forma`) |
| Opcional e `?.` (aula 03) | `cupom?: Cupom` e `cupom?.tipo === "freteGratis"` |
| `readonly` | O `id` do produto não pode ser trocado |
| `switch` com todos os casos | `desconto`: se um tipo de cupom novo surgir, o TypeScript avisa que a função pode não devolver um número |

!!! tip "Estados impossíveis não compilam"
    Tente escrever `{ forma: "pix", parcelas: 3 }` ou um cupom `{ tipo: "percentual", codigo: "X" }` sem o `percentual`: o compilador recusa. As regras do negócio estão nos **tipos**, e não só na cabeça de quem programou.

---

## Entrega

1. O `src/carrinho.ts` com **um tipo de cupom novo** criado por você (por exemplo, “leve 3, pague 2” num produto).
2. Um print com `npx tsc` sem erros e a saída de três cenários diferentes.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Compila | `strict: true`, nenhum erro, nenhum `any` |
| Modelagem | Cupons e pagamentos como uniões discriminadas |
| Regras | Contas certas nos cenários entregues |
| Clareza | Funções pequenas: subtotal, desconto, frete, acréscimo, resumo |

---

## Exercícios extras

### Básico (fixação)

Rode o carrinho com o cupom de valor fixo `{ tipo: "valorFixo", codigo: "BEMVINDO", valor: 20 }` e pagamento em pix. Qual o total?

<!-- gabarito -->
??? success "Gabarito — Básico"
    Subtotal R$ 138,60 − desconto R$ 20,00 = R$ 118,60, mais frete de R$ 15,00 = **R$ 133,60** (pix não tem acréscimo).

### Intermediário (aplicação)

Acrescente ao carrinho itens suficientes para passar de R$ 200 e confira que o frete zera.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Por exemplo, mude a quantidade da mochila para 2: subtotal R$ 228,50. Sem cupom, o valor depois do desconto já passa de R$ 200, e `frete` devolve 0.

### Avançado (desafio)

Acrescente o pagamento `{ forma: "boleto"; vencimento: string }`, com 2% de desconto à vista. O que o compilador obriga você a mudar?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Acrescente o formato à união `Pagamento`. A função `acrescimo` usa `if`, então continua compilando: é você quem precisa lembrar de tratar o boleto (devolvendo, por exemplo, `-valor * 0.02`). Se `acrescimo` usasse `switch` com o `never` no `default` (aula 02), o compilador apontaria o caso faltando. É um bom motivo para preferir `switch` em uniões discriminadas.

---

## 💡 Resumo

- Regras de negócio viram tipos: cupons e pagamentos como uniões discriminadas.
- Opcionais com `?` e `?.`; `readonly` no que não pode mudar.
- `switch` (com `never`) ajuda o compilador a avisar quando surge um caso novo.

## ➡️ Próximo passo

Você terminou o **Módulo 02**. Volte ao [índice do módulo](index.md) e confira o checklist. Depois, siga para o **[Módulo 03 — TypeScript no navegador](../modulo_03_navegador/index.md)**.
