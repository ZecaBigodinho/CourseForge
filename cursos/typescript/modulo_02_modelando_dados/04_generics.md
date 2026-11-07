# 04 — Generics

> **Curso:** TypeScript  
> **Módulo:** 02 — Modelando dados  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o problema que os **generics** resolvem.
- Escrever funções genéricas (`<T>`) e restringir o tipo com `extends`.
- Criar tipos genéricos, como `Resposta<T>`.
- Reconhecer generics que você já usa: `Array<T>`, `Promise<T>`, `Record<K, V>`.

## Pré-requisitos

- [Aula 03](03_opcionais_e_null.md) deste módulo.

---

## O problema

Uma função que devolve o primeiro item de uma lista:

```ts
function primeiroQualquer(lista: any[]): any {
  return lista[0];
}
const n = primeiroQualquer([1, 2, 3]); // any: perdeu o tipo
```

Com `any`, o TypeScript esquece que era uma lista de números. Escrever uma versão para cada tipo também não dá. A solução são os **generics**: um “tipo variável”.

```ts
function primeiro<T>(lista: T[]): T | undefined {
  return lista[0];
}

const num = primeiro([1, 2, 3]);         // number | undefined
const nome = primeiro(["Ana", "Bruno"]); // string | undefined
```

`T` é preenchido na hora da chamada, pelo tipo que você passa. Leia `primeiro<T>` como “primeiro, para algum tipo T”.

---

## Restringir com `extends`

Às vezes o tipo pode variar, mas precisa ter alguma coisa:

```ts
function maisCaro<T extends { preco: number }>(itens: T[]): T | undefined {
  let maior: T | undefined;
  for (const item of itens) {
    if (!maior || item.preco > maior.preco) maior = item;
  }
  return maior;
}

const lanches = [
  { nome: "X-Salada", preco: 18 },
  { nome: "X-Bacon", preco: 22 },
];
console.log(maisCaro(lanches)?.nome); // X-Bacon
```

`T extends { preco: number }` aceita qualquer objeto **que tenha** `preco` numérico, e o resultado continua com o tipo completo (com `nome`).

---

## Tipos genéricos

```ts
type Resposta<T> =
  | { ok: true; dados: T }
  | { ok: false; erro: string };

function buscarAluno(id: number): Resposta<{ nome: string }> {
  if (id === 1) return { ok: true, dados: { nome: "Ana" } };
  return { ok: false, erro: "Aluno não encontrado" };
}

const r = buscarAluno(1);
if (r.ok) {
  console.log(r.dados.nome);
} else {
  console.log(r.erro);
}
```

## Generics que você já usa

| Tipo | Significa |
|---|---|
| `Array<number>` | O mesmo que `number[]` |
| `Promise<string>` | Uma promessa que vai entregar uma `string` (Módulo 03, `fetch`) |
| `Record<string, number>` | Um objeto com chaves `string` e valores `number` |
| `Partial<Produto>` | O `Produto` com todas as propriedades opcionais |

```ts
const estoque: Record<string, number> = { caderno: 40, caneta: 120 };
```

---

## Exercícios

### Básico (fixação)

Escreva `ultimo<T>(lista: T[]): T | undefined` e teste com números e com textos.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    function ultimo<T>(lista: T[]): T | undefined {
      return lista[lista.length - 1];
    }
    ultimo([1, 2, 3]);       // 3
    ultimo(["a", "b"]);      // "b"
    ultimo<number>([]);      // undefined
    ```

### Intermediário (aplicação)

Escreva `agruparPorTurma<T extends { turma: string }>(lista: T[]): Record<string, T[]>`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    function agruparPorTurma<T extends { turma: string }>(lista: T[]): Record<string, T[]> {
      const grupos: Record<string, T[]> = {};
      for (const item of lista) {
        (grupos[item.turma] ??= []).push(item);
      }
      return grupos;
    }
    ```
    `x ??= []` atribui um array vazio só se `x` ainda não existir.

### Avançado (desafio)

Use `Resposta<T>` para escrever `dividir(a: number, b: number): Resposta<number>`, que devolve erro quando `b` é 0.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    function dividir(a: number, b: number): Resposta<number> {
      if (b === 0) return { ok: false, erro: "Divisão por zero" };
      return { ok: true, dados: a / b };
    }
    const d = dividir(10, 0);
    console.log(d.ok ? d.dados : d.erro); // Divisão por zero
    ```
    Quem chama é **obrigado** a verificar `ok` antes de usar `dados`: o erro não pode ser ignorado.

---

## 💡 Resumo

- Generics (`<T>`) mantêm o tipo em funções que servem para vários tipos.
- `T extends { … }` exige um formato mínimo.
- Tipos genéricos como `Resposta<T>` modelam sucesso e erro.
- `Array<T>`, `Promise<T>`, `Record<K, V>` e `Partial<T>` já são generics.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_carrinho.md)** você modela um carrinho de compras.
