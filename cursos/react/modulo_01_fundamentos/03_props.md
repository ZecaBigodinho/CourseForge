# 03 — Props

> **Curso:** React  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Passar dados para componentes com **props**.
- Tipar as props com TypeScript (incluindo opcionais e valores padrão).
- Usar a prop especial **`children`**.
- Renderizar listas com `map` e entender a **`key`**.

## Pré-requisitos

- [Aula 02](02_jsx_e_componentes.md) deste módulo.

---

## Props: os parâmetros do componente

Props são como **atributos** de uma tag e chegam ao componente como um objeto:

```tsx
type CartaoProps = {
  titulo: string;
  preco: number;
  destaque?: boolean;
};

function Cartao({ titulo, preco, destaque = false }: CartaoProps) {
  return (
    <article className={destaque ? "cartao destaque" : "cartao"}>
      <h2>{titulo}</h2>
      <p>R$ {preco.toFixed(2)}</p>
    </article>
  );
}

export default function App() {
  return (
    <main>
      <Cartao titulo="X-Salada" preco={18} />
      <Cartao titulo="X-Bacon" preco={22} destaque />
    </main>
  );
}
```

- Texto vai entre aspas (`titulo="X-Salada"`); qualquer outro valor vai entre chaves (`preco={18}`).
- `destaque` sozinho é o mesmo que `destaque={true}`.
- O TypeScript confere tudo: esquecer `preco` ou passar `preco="dezoito"` vira erro.

!!! warning "Props são somente leitura"
    O componente **nunca** altera as próprias props. Se um dado precisa mudar, ele é **estado** (aula 04), guardado em quem é dono dele.

---

## `children`: o conteúdo entre as tags

```tsx
import type { ReactNode } from "react";

type CaixaProps = { titulo: string; children: ReactNode };

function Caixa({ titulo, children }: CaixaProps) {
  return (
    <section className="caixa">
      <h2>{titulo}</h2>
      {children}
    </section>
  );
}

<Caixa titulo="Horário">
  <p>Segunda a sábado, das 11h às 22h.</p>
</Caixa>
```

Tudo o que vai entre `<Caixa>` e `</Caixa>` chega como `children`. É assim que se fazem “molduras” reaproveitáveis.

---

## Listas com `map` e `key`

```tsx
type Produto = { id: number; nome: string; preco: number };

const produtos: Produto[] = [
  { id: 1, nome: "X-Salada", preco: 18 },
  { id: 2, nome: "X-Bacon", preco: 22 },
  { id: 3, nome: "Suco de laranja", preco: 9 },
];

export default function App() {
  return (
    <main>
      {produtos.map((p) => (
        <Cartao key={p.id} titulo={p.nome} preco={p.preco} />
      ))}
    </main>
  );
}
```

O `map` transforma cada objeto em um componente. A **`key`** identifica cada item da lista para o React saber, na próxima atualização, quem entrou, quem saiu e quem mudou de lugar.

!!! tip "Qual `key` usar"
    Use um **identificador estável e único** dos dados (o `id`). Evite o índice do `map` (`key={i}`) em listas que mudam de ordem ou perdem itens: o React pode trocar o conteúdo de um item pelo de outro. Sem `key`, o Console mostra um aviso.

---

## Exercícios

### Básico (fixação)

Crie `Saudacao` com a prop `nome: string` e use-a para dois nomes diferentes.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```tsx
    function Saudacao({ nome }: { nome: string }) {
      return <p>Olá, {nome}!</p>;
    }
    // no App:
    <Saudacao nome="Ana" />
    <Saudacao nome="Bruno" />
    ```

### Intermediário (aplicação)

Acrescente ao `Cartao` uma prop opcional `etiqueta?: string` que, quando existir, aparece acima do título.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    type CartaoProps = { titulo: string; preco: number; etiqueta?: string };
    function Cartao({ titulo, preco, etiqueta }: CartaoProps) {
      return (
        <article className="cartao">
          {etiqueta && <span className="etiqueta">{etiqueta}</span>}
          <h2>{titulo}</h2>
          <p>R$ {preco.toFixed(2)}</p>
        </article>
      );
    }
    ```
    `{condição && <JSX />}` mostra o elemento só quando a condição é verdadeira.

### Avançado (desafio)

Mostre só os produtos de até R$ 20, em ordem de preço, usando `filter`, `sort` e `map`, sem alterar o array original.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```tsx
    const baratos = produtos
      .filter((p) => p.preco <= 20)
      .sort((a, b) => a.preco - b.preco);
    // no JSX:
    {baratos.map((p) => <Cartao key={p.id} titulo={p.nome} preco={p.preco} />)}
    ```
    O `filter` já devolve um array **novo**, então o `sort` ordena essa cópia, e `produtos` continua intacto. Se fosse ordenar a lista inteira, use `[...produtos].sort(…)`: o `sort` altera o array em que é chamado, e no React os dados originais não devem ser alterados. (Existe também o `toSorted`, que sempre devolve cópia, mas ele exige `"ES2023"` na opção `lib` do `tsconfig`; o modelo do Vite vem com `ES2020`.)

---

## 💡 Resumo

- Props passam dados de cima para baixo; são **somente leitura**.
- Tipe as props com `type`; opcionais com `?` e padrão na desestruturação.
- `children` recebe o conteúdo entre as tags.
- Listas: `map` + `key` estável (o `id`, não o índice).

## ➡️ Próximo passo

Na **[aula 04](04_estado_e_eventos.md)** a tela passa a mudar com os cliques.
