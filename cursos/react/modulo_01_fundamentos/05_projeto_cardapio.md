# 05 — Projeto do módulo: cardápio com pedido

> **Curso:** React
> **Módulo:** 01 — Fundamentos
> **Tempo estimado:** 1 h 30 min

---

## Objetivos

Ao final deste projeto, você terá:

- Um **cardápio** em React em que o cliente escolhe as quantidades com **−** e **+**.
- O **total do pedido** calculado e atualizado na hora.
- Componentes com props tipadas e o estado guardado no componente certo.

## Pré-requisitos

- Aulas [01](01_primeiro_projeto.md) a [04](04_estado_e_eventos.md) deste módulo.

---

## O pedido

> *“Quero que o cliente monte o pedido no celular e já veja quanto vai dar.”*

A lanchonete e os preços são inventados (os mesmos do curso de Web).

---

## Onde fica o estado?

As quantidades são usadas por **dois** componentes: cada `ItemCardapio` mostra a sua, e o `ResumoPedido` soma todas. Por isso o estado fica no **pai comum**, o `App`, que passa a quantidade para cada item e recebe de volta os cliques por uma função (`aoAlterar`). Isso se chama **elevar o estado** e volta com força no Módulo 03.

```text
App  (estado: quantidades)
├── ItemCardapio × 3   ← recebe quantidade e aoAlterar
└── ResumoPedido       ← recebe itens e total (calculados)
```

---

## O código

Crie o projeto (`npm create vite@latest cardapio -- --template react-ts`), apague o `src/App.css` e substitua os arquivos abaixo.

### `src/App.tsx`

```tsx
import { useState } from "react";

type Produto = {
  id: number;
  nome: string;
  descricao: string;
  preco: number;
};

const CARDAPIO: Produto[] = [
  { id: 1, nome: "X-Salada", descricao: "Pão, hambúrguer, queijo, alface e tomate.", preco: 18 },
  { id: 2, nome: "X-Bacon", descricao: "Pão, hambúrguer, queijo e bacon crocante.", preco: 22 },
  { id: 3, nome: "Suco de laranja", descricao: "Natural, 400 ml.", preco: 9 },
];

function formatarPreco(valor: number): string {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

type ItemCardapioProps = {
  produto: Produto;
  quantidade: number;
  aoAlterar: (variacao: number) => void;
};

function ItemCardapio({ produto, quantidade, aoAlterar }: ItemCardapioProps) {
  return (
    <li className="item">
      <div className="info">
        <h2>{produto.nome}</h2>
        <p>{produto.descricao}</p>
        <p>{formatarPreco(produto.preco)}</p>
      </div>
      <div className="qtd">
        <button
          type="button"
          onClick={() => aoAlterar(-1)}
          disabled={quantidade === 0}
          aria-label={`Tirar um ${produto.nome}`}
        >
          −
        </button>
        <span aria-live="polite">{quantidade}</span>
        <button type="button" onClick={() => aoAlterar(+1)} aria-label={`Pôr mais um ${produto.nome}`}>
          +
        </button>
      </div>
    </li>
  );
}

type ResumoProps = { itens: number; total: number };

function ResumoPedido({ itens, total }: ResumoProps) {
  if (itens === 0) {
    return <p className="resumo">Seu pedido está vazio.</p>;
  }
  return (
    <p className="resumo">
      {itens} {itens === 1 ? "item" : "itens"} · Total: <strong>{formatarPreco(total)}</strong>
    </p>
  );
}

export default function App() {
  const [quantidades, setQuantidades] = useState<Record<number, number>>({});

  function alterarQuantidade(id: number, variacao: number) {
    setQuantidades((atual) => ({
      ...atual,
      [id]: Math.max(0, (atual[id] ?? 0) + variacao),
    }));
  }

  const itens = CARDAPIO.reduce((soma, p) => soma + (quantidades[p.id] ?? 0), 0);
  const total = CARDAPIO.reduce((soma, p) => soma + p.preco * (quantidades[p.id] ?? 0), 0);

  return (
    <main className="app">
      <h1>Lanchonete do Bairro</h1>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {CARDAPIO.map((produto) => (
          <ItemCardapio
            key={produto.id}
            produto={produto}
            quantidade={quantidades[produto.id] ?? 0}
            aoAlterar={(variacao) => alterarQuantidade(produto.id, variacao)}
          />
        ))}
      </ul>
      <ResumoPedido itens={itens} total={total} />
    </main>
  );
}
```

### `src/index.css`

```css
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; background: #fff8f1; color: #2b2b2b; }
.app { max-width: 640px; margin: 0 auto; padding: 24px 16px; }
h1 { color: #e8781e; }
.item { display: flex; align-items: center; gap: 12px; background: white; padding: 12px 16px; border-radius: 12px; margin-bottom: 8px; }
.item .info { flex: 1; }
.item h2 { font-size: 1.1rem; margin: 0; }
.item p { margin: 4px 0 0; color: #666; }
.qtd { display: flex; align-items: center; gap: 8px; }
.qtd button { width: 32px; height: 32px; border: 0; border-radius: 50%; background: #e8781e; color: white; font-size: 1.2rem; cursor: pointer; }
.qtd button:disabled { background: #ccc; cursor: default; }
.resumo { margin-top: 16px; padding: 16px; background: white; border-radius: 12px; font-size: 1.1rem; }
```

Rode `npm run dev` e monte um pedido.

| Detalhe | Por quê |
|---|---|
| `Record<number, number>` | Um objeto “id do produto ➔ quantidade”; produto sem chave conta como 0 (`?? 0`) |
| `aoAlterar(-1)` / `aoAlterar(+1)` | O item avisa só a **variação**; quem calcula a nova quantidade é o `App`, a partir do estado atual |
| `setQuantidades((atual) => …)` | Forma funcional: cliques rápidos em sequência não se perdem (aula 04) |
| `Math.max(0, …)` | A quantidade nunca fica negativa; o botão **−** também fica desabilitado no 0 |
| `itens` e `total` sem `useState` | São **calculados** a partir das quantidades a cada renderização: nunca ficam desatualizados |
| `aria-label` e `aria-live` | O leitor de tela diz o que cada botão faz e anuncia a quantidade nova |

---

## Entrega

1. A pasta `src/` do projeto compactada (sem `node_modules/`).
2. Um print do cardápio com um pedido montado e o total.
3. A saída do `npm run build` **sem erros**.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Componentes | Pelo menos `ItemCardapio` e `ResumoPedido`, com props tipadas |
| Estado | No `App`, atualizado com a forma funcional e sem alterar o objeto no lugar |
| Funciona | Quantidades nunca negativas; total certo; mensagem de pedido vazio |
| Build | `npm run build` sem erros de TypeScript |

---

## Exercícios extras

### Básico (fixação)

Acrescente mais dois produtos ao cardápio. Quantas linhas do resto do código você precisou mudar?

<!-- gabarito -->
??? success "Gabarito — Básico"
    Só o array `CARDAPIO` (com `id` novos e únicos). Os itens, as quantidades e o total se ajustam sozinhos: a tela é calculada a partir dos dados.

### Intermediário (aplicação)

Acrescente um botão **Limpar pedido** que zera todas as quantidades.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    <button type="button" onClick={() => setQuantidades({})} disabled={itens === 0}>
      Limpar pedido
    </button>
    ```
    Um objeto vazio: todo produto volta a contar como 0.

### Avançado (desafio)

Dê **10% de desconto** quando o pedido tiver 5 itens ou mais e mostre o desconto no resumo.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    No `App`: `const desconto = itens >= 5 ? total * 0.1 : 0;` e passe `desconto` para o `ResumoPedido` (acrescente `desconto: number` ao tipo das props). No resumo:
    ```tsx
    {desconto > 0 && <span> · Desconto: −{formatarPreco(desconto)}</span>}
    · Total: <strong>{formatarPreco(total - desconto)}</strong>
    ```
    O desconto também é **calculado**, sem `useState`.

---

## 💡 Resumo

- O estado fica no componente que é **dono** do dado (o pai comum); os filhos recebem props e avisam por funções.
- Forma funcional no `set` e cópias novas de objetos e arrays.
- O que pode ser calculado a partir do estado não vira outro estado.

## ➡️ Próximo passo

Você terminou o **Módulo 01**. Volte ao [índice do módulo](index.md) e confira o checklist. Depois, siga para o **[Módulo 02 — Listas, formulários e efeitos](../modulo_02_formularios_e_efeitos/index.md)**.
