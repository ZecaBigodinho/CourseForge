# 01 — type × interface

> **Curso:** TypeScript  
> **Módulo:** 02 — Modelando dados  
> **Tempo estimado:** 1 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Descrever objetos com `interface`.
- Estender modelos com `extends` (interface) e `&` (type).
- Saber o que **só** o `type` faz e qual escolher no dia a dia.

## Pré-requisitos

- [Módulo 01](../modulo_01_fundamentos/index.md) completo.

---

## `interface`

Uma `interface` descreve o formato de um objeto, como o `type` do Módulo 01:

```ts
interface Produto {
  id: number;
  nome: string;
  preco: number;
  descricao?: string;
}

const caderno: Produto = { id: 1, nome: "Caderno", preco: 12.9 };
```

## Estender

Muitas vezes um modelo é “o outro, com mais coisas”:

```ts
interface ProdutoFisico extends Produto {
  pesoKg: number;
}

const mochila: ProdutoFisico = { id: 2, nome: "Mochila", preco: 89.9, pesoKg: 0.8 };
```

Com `type`, o mesmo se faz com `&` (interseção):

```ts
type Pessoa = { nome: string; email: string };
type Cliente = Pessoa & { pontos: number };

const cliente: Cliente = { nome: "Ana Souza", email: "ana.souza@example.com", pontos: 120 };
```

---

## Qual usar?

| Recurso | `interface` | `type` |
|---|---|---|
| Formato de objeto | ✅ | ✅ |
| Estender | `extends` | `&` |
| União (`"pix" \| "cartao"`) | ❌ | ✅ |
| Tipo de função, tupla, apelido de primitivo | Desajeitado | ✅ |
| Pode ser “reaberta” e completada em outro lugar | ✅ | ❌ |

!!! tip "Regra prática do curso"
    Use **`type`** por padrão: ele faz tudo o que você vai precisar, inclusive uniões (próxima aula). Use **`interface`** quando estiver modelando objetos que outras partes do código vão estender, ou quando o projeto da empresa já usar esse padrão. O importante é ser **consistente** num mesmo projeto.

---

## Exercícios

### Básico (fixação)

Crie a `interface Aluno` (nome, matrícula, e-mail opcional) e um objeto que a respeite.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    interface Aluno {
      nome: string;
      matricula: number;
      email?: string;
    }
    const ana: Aluno = { nome: "Ana Souza", matricula: 2026001 };
    ```

### Intermediário (aplicação)

Crie `interface Professor extends Pessoa` com a lista de disciplinas, partindo de `interface Pessoa { nome: string; email: string }`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    interface Pessoa { nome: string; email: string; }
    interface Professor extends Pessoa { disciplinas: string[]; }
    const prof: Professor = {
      nome: "Pedro Paulo",
      email: "professor@example.com",
      disciplinas: ["Informática", "Programação"],
    };
    ```

### Avançado (desafio)

Tente escrever `interface Pagamento = "pix" | "cartao"`. O que acontece? Como resolver?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Não compila: `interface` só descreve objetos, não aceita `=` nem uniões de valores. O certo é `type Pagamento = "pix" | "cartao";`. É exatamente o caso em que o `type` é necessário.

---

## 💡 Resumo

- `interface` e `type` descrevem objetos; `extends` e `&` estendem.
- Só o `type` faz uniões, tuplas e tipos de função.
- No curso: `type` por padrão; seja consistente no projeto.

## ➡️ Próximo passo

Na **[aula 02](02_unioes_e_narrowing.md)** você usa uniões para dizer “isto OU aquilo”.
