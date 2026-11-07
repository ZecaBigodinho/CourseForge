# 03 — Valores opcionais e null

> **Curso:** TypeScript  
> **Módulo:** 02 — Modelando dados  
> **Tempo estimado:** 1 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Entender por que o modo `strict` reclama de `undefined` e `null`.
- Usar o **encadeamento opcional** (`?.`) e o **coalescência nula** (`??`).
- Diferenciar `??` de `||`.
- Saber quando (não) usar o `!`.

## Pré-requisitos

- [Aula 02](02_unioes_e_narrowing.md) deste módulo.

---

## O erro de um bilhão de dólares

Em JavaScript, `Cannot read properties of undefined` é provavelmente o erro mais comum. Com `strict`, o TypeScript sabe quando um valor **pode faltar** e obriga a tratar:

```ts
type Endereco = { rua: string; cidade: string };
type Cliente = { nome: string; endereco?: Endereco; apelido: string | null };

const cliente: Cliente = { nome: "Ana Souza", apelido: null };

// console.log(cliente.endereco.cidade);
// erro: 'cliente.endereco' é possivelmente 'indefinido'.
```

---

## `?.` — encadeamento opcional

```ts
const cidade = cliente.endereco?.cidade;   // string | undefined
```

Se `endereco` não existir, a expressão para ali e devolve `undefined`, sem quebrar. Funciona também com funções e índices: `config.aoSalvar?.()`, `lista?.[0]`.

## `??` — valor padrão quando falta

```ts
const cidadeTexto = cliente.endereco?.cidade ?? "Cidade não informada";
const nomeExibido = cliente.apelido ?? cliente.nome;   // "Ana Souza"
```

`a ?? b` usa `b` **só** quando `a` é `null` ou `undefined`.

### `??` × `||`

```ts
const desconto = 0;
console.log(desconto || 10);  // 10  ← o || trata 0 como "falso"
console.log(desconto ?? 10);  // 0   ← o ?? só troca null/undefined
```

!!! warning "Use `??` para valores padrão"
    Com `||`, um desconto de `0`, um estoque de `0` ou um texto vazio `""` são trocados pelo padrão sem você perceber. O `??` respeita esses valores.

---

## O `!` (não nulo): use com muito cuidado

```ts
const campo = document.querySelector("#nome")!;  // "confie em mim, existe"
```

O `!` diz ao compilador “este valor **não** é nulo” e desliga a conferência. Se você estiver errado, o erro volta a aparecer só rodando. Prefira conferir:

```ts
const campo2 = document.querySelector("#nome");
if (campo2) {
  campo2.textContent = "Ana";
}
```

---

## Exercícios

### Básico (fixação)

Com `type Usuario = { nome: string; telefone?: string }`, mostre o telefone ou “sem telefone”.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    type Usuario = { nome: string; telefone?: string };
    const u: Usuario = { nome: "Ana" };
    console.log(u.telefone ?? "sem telefone");
    ```

### Intermediário (aplicação)

Um produto tem `estoque?: number`. Mostre “Esgotado” quando o estoque for 0, “Consultar” quando não for informado e o número nos outros casos.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    function textoEstoque(estoque?: number): string {
      if (estoque === undefined) return "Consultar";
      if (estoque === 0) return "Esgotado";
      return `${estoque} unidades`;
    }
    ```
    Usar `estoque || "Consultar"` trataria o 0 como “não informado”: o mesmo problema do `||`.

### Avançado (desafio)

Escreva `cidadeDoPrimeiroCliente(clientes: Cliente[]): string`, que devolve a cidade do primeiro cliente ou “—” se a lista estiver vazia ou o cliente não tiver endereço, numa única linha.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    function cidadeDoPrimeiroCliente(clientes: Cliente[]): string {
      return clientes[0]?.endereco?.cidade ?? "—";
    }
    ```
    `clientes[0]` pode ser `undefined` (lista vazia): o `?.` cobre os dois níveis e o `??` dá o padrão.

---

## 💡 Resumo

- Com `strict`, o TypeScript obriga a tratar o que pode ser `undefined` ou `null`.
- `a?.b` não quebra se `a` faltar; `a ?? padrão` troca só `null`/`undefined`.
- Prefira `??` a `||` para valores padrão.
- O `!` desliga a conferência: prefira um `if`.

## ➡️ Próximo passo

Na **[aula 04](04_generics.md)** você escreve código que funciona com qualquer tipo, sem perder a tipagem.
