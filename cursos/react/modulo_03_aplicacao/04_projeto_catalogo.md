# 04 — Projeto final: catálogo com busca e carrinho

> **Curso:** React
> **Módulo:** 03 — Aplicação completa
> **Tempo estimado:** 3 h

---

## Objetivos

Ao final deste projeto, você terá:

- O **catálogo** de uma papelaria (inventada) com **busca**, **filtro por categoria** e **carrinho**.
- O estado da busca **elevado** para o `App` e o carrinho compartilhado por **Context**.
- O carrinho guardado no navegador, com validação ao carregar.
- O app **publicado** no GitHub Pages (requisito do certificado).

## Pré-requisitos

- Aulas [01](01_elevar_o_estado.md) a [03](03_build_e_publicacao.md) deste módulo.

---

## O pedido

> *“Quero que os clientes vejam os produtos da papelaria, procurem o que precisam e montem o pedido antes de vir buscar.”*

A **Papelaria Ponto Final** e os preços são inventados.

## A organização

```text
src/
├── App.tsx                  ← estado da busca e da categoria; lista calculada
├── tipos.ts
├── dados.ts                 ← os produtos
├── formatar.ts              ← brl()
├── index.css
├── carrinho/
│   ├── contexto.ts          ← CarrinhoContext e o tipo do valor
│   ├── useCarrinho.ts       ← o hook que confere o Provider
│   └── CarrinhoProvider.tsx ← estado do carrinho, funções e localStorage
└── components/
    ├── Busca.tsx
    ├── CartaoProduto.tsx    ← usa adicionar()
    └── Carrinho.tsx         ← usa itens, totais, alterar() e limpar()
```

---

## O código

Crie o projeto (`npm create vite@latest catalogo -- --template react-ts`), apague `src/App.css` e escreva os arquivos.

### `src/tipos.ts`

```ts
export type Categoria = "cadernos" | "escrita" | "mochilas";

export type Produto = {
  id: number;
  nome: string;
  preco: number;
  categoria: Categoria;
};

export type ItemCarrinho = {
  produto: Produto;
  quantidade: number;
};
```

### `src/dados.ts`

```ts
import type { Produto } from "./tipos";

export const PRODUTOS: Produto[] = [
  { id: 1, nome: "Caderno universitário", preco: 24.9, categoria: "cadernos" },
  { id: 2, nome: "Caderno de desenho A4", preco: 18.5, categoria: "cadernos" },
  { id: 3, nome: "Caneta azul (kit com 4)", preco: 9.9, categoria: "escrita" },
  { id: 4, nome: "Lápis grafite (kit com 6)", preco: 7.5, categoria: "escrita" },
  { id: 5, nome: "Marca-texto amarelo", preco: 4.2, categoria: "escrita" },
  { id: 6, nome: "Mochila escolar", preco: 89.9, categoria: "mochilas" },
];
```

### `src/formatar.ts`

```ts
export function brl(valor: number): string {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}
```

### `src/carrinho/contexto.ts`

```ts
import { createContext } from "react";
import type { ItemCarrinho, Produto } from "../tipos";

export type CarrinhoValor = {
  itens: ItemCarrinho[];
  totalItens: number;
  totalValor: number;
  adicionar: (produto: Produto) => void;
  alterar: (id: number, variacao: number) => void;
  limpar: () => void;
};

export const CarrinhoContext = createContext<CarrinhoValor | null>(null);
```

### `src/carrinho/useCarrinho.ts`

```ts
import { useContext } from "react";
import { CarrinhoContext } from "./contexto";

export function useCarrinho() {
  const valor = useContext(CarrinhoContext);
  if (valor === null) {
    throw new Error("useCarrinho precisa estar dentro de <CarrinhoProvider>");
  }
  return valor;
}
```

### `src/carrinho/CarrinhoProvider.tsx`

```tsx
import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { CarrinhoContext } from "./contexto";
import type { ItemCarrinho, Produto } from "../tipos";

const CHAVE = "carrinho-papelaria";

function ehItem(valor: unknown): valor is ItemCarrinho {
  if (typeof valor !== "object" || valor === null) return false;
  const v = valor as Record<string, unknown>;
  const p = v.produto as Record<string, unknown> | null;
  return (
    typeof v.quantidade === "number" &&
    typeof p === "object" && p !== null &&
    typeof p.id === "number" && typeof p.nome === "string" && typeof p.preco === "number"
  );
}

function carregar(): ItemCarrinho[] {
  try {
    const dados: unknown = JSON.parse(localStorage.getItem(CHAVE) ?? "[]");
    return Array.isArray(dados) ? dados.filter(ehItem) : [];
  } catch {
    return [];
  }
}

export default function CarrinhoProvider({ children }: { children: ReactNode }) {
  const [itens, setItens] = useState<ItemCarrinho[]>(carregar);

  useEffect(() => {
    localStorage.setItem(CHAVE, JSON.stringify(itens));
  }, [itens]);

  function adicionar(produto: Produto) {
    setItens((atual) =>
      atual.some((i) => i.produto.id === produto.id)
        ? atual.map((i) => (i.produto.id === produto.id ? { ...i, quantidade: i.quantidade + 1 } : i))
        : [...atual, { produto, quantidade: 1 }],
    );
  }

  function alterar(id: number, variacao: number) {
    setItens((atual) =>
      atual
        .map((i) => (i.produto.id === id ? { ...i, quantidade: i.quantidade + variacao } : i))
        .filter((i) => i.quantidade > 0),
    );
  }

  function limpar() {
    setItens([]);
  }

  const totalItens = itens.reduce((s, i) => s + i.quantidade, 0);
  const totalValor = itens.reduce((s, i) => s + i.produto.preco * i.quantidade, 0);

  return (
    <CarrinhoContext.Provider value={{ itens, totalItens, totalValor, adicionar, alterar, limpar }}>
      {children}
    </CarrinhoContext.Provider>
  );
}
```

### `src/components/Busca.tsx`

```tsx
import type { Categoria } from "../tipos";

type Props = {
  termo: string;
  categoria: Categoria | "todas";
  aoMudarTermo: (termo: string) => void;
  aoMudarCategoria: (categoria: Categoria | "todas") => void;
};

export default function Busca({ termo, categoria, aoMudarTermo, aoMudarCategoria }: Props) {
  return (
    <div className="busca">
      <label htmlFor="termo">Buscar</label>
      <input id="termo" value={termo} onChange={(e) => aoMudarTermo(e.target.value)} placeholder="Ex.: caderno" />
      <label htmlFor="categoria">Categoria</label>
      <select
        id="categoria"
        value={categoria}
        onChange={(e) => aoMudarCategoria(e.target.value as Categoria | "todas")}
      >
        <option value="todas">Todas</option>
        <option value="cadernos">Cadernos</option>
        <option value="escrita">Escrita</option>
        <option value="mochilas">Mochilas</option>
      </select>
    </div>
  );
}
```

### `src/components/CartaoProduto.tsx`

```tsx
import type { Produto } from "../tipos";
import { useCarrinho } from "../carrinho/useCarrinho";
import { brl } from "../formatar";

export default function CartaoProduto({ produto }: { produto: Produto }) {
  const { adicionar } = useCarrinho();
  return (
    <article className="cartao">
      <h3>{produto.nome}</h3>
      <p className="preco">{brl(produto.preco)}</p>
      <button type="button" onClick={() => adicionar(produto)}>
        Adicionar ao carrinho
      </button>
    </article>
  );
}
```

### `src/components/Carrinho.tsx`

```tsx
import { useCarrinho } from "../carrinho/useCarrinho";
import { brl } from "../formatar";

export default function Carrinho() {
  const { itens, totalItens, totalValor, alterar, limpar } = useCarrinho();

  return (
    <aside className="carrinho" aria-labelledby="titulo-carrinho">
      <h2 id="titulo-carrinho">Carrinho ({totalItens})</h2>
      {itens.length === 0 ? (
        <p>Seu carrinho está vazio.</p>
      ) : (
        <>
          <ul>
            {itens.map(({ produto, quantidade }) => (
              <li key={produto.id}>
                <span>{produto.nome}</span>
                <span className="qtd">
                  <button type="button" onClick={() => alterar(produto.id, -1)} aria-label={`Tirar um ${produto.nome}`}>
                    −
                  </button>
                  {quantidade}
                  <button type="button" onClick={() => alterar(produto.id, +1)} aria-label={`Pôr mais um ${produto.nome}`}>
                    +
                  </button>
                </span>
                <span>{brl(produto.preco * quantidade)}</span>
              </li>
            ))}
          </ul>
          <p className="total">
            Total: <strong>{brl(totalValor)}</strong>
          </p>
          <button type="button" className="secundario" onClick={limpar}>
            Esvaziar carrinho
          </button>
        </>
      )}
    </aside>
  );
}
```

### `src/App.tsx`

```tsx
import { useState } from "react";
import type { Categoria } from "./tipos";
import { PRODUTOS } from "./dados";
import CarrinhoProvider from "./carrinho/CarrinhoProvider";
import Busca from "./components/Busca";
import CartaoProduto from "./components/CartaoProduto";
import Carrinho from "./components/Carrinho";

export default function App() {
  const [termo, setTermo] = useState("");
  const [categoria, setCategoria] = useState<Categoria | "todas">("todas");

  const visiveis = PRODUTOS.filter(
    (p) =>
      (categoria === "todas" || p.categoria === categoria) &&
      p.nome.toLowerCase().includes(termo.trim().toLowerCase()),
  );

  return (
    <CarrinhoProvider>
      <header className="topo">
        <h1>Papelaria Ponto Final</h1>
      </header>
      <div className="layout">
        <main>
          <Busca termo={termo} categoria={categoria} aoMudarTermo={setTermo} aoMudarCategoria={setCategoria} />
          {visiveis.length === 0 ? (
            <p>Nenhum produto encontrado.</p>
          ) : (
            <div className="grade">
              {visiveis.map((p) => (
                <CartaoProduto key={p.id} produto={p} />
              ))}
            </div>
          )}
        </main>
        <Carrinho />
      </div>
    </CarrinhoProvider>
  );
}
```

### `src/index.css`

```css
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; background: #f7f5ff; color: #222; }
.topo { background: #4f35b5; color: white; padding: 16px 24px; }
.topo h1 { margin: 0; font-size: 1.5rem; }
.layout { display: grid; gap: 24px; max-width: 1100px; margin: 0 auto; padding: 24px 16px; }
@media (min-width: 900px) { .layout { grid-template-columns: 1fr 320px; align-items: start; } }
.busca { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 16px; }
.busca input { flex: 1; min-width: 160px; padding: 8px; }
.busca select { padding: 8px; }
.grade { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
.cartao { background: white; padding: 16px; border-radius: 12px; display: flex; flex-direction: column; gap: 8px; }
.cartao h3 { margin: 0; font-size: 1rem; }
.preco { font-weight: 700; color: #4f35b5; margin: 0; }
button { padding: 8px 12px; border: 0; border-radius: 8px; background: #4f35b5; color: white; cursor: pointer; }
.secundario { background: #eee; color: #222; }
.carrinho { background: white; padding: 16px; border-radius: 12px; }
.carrinho h2 { margin-top: 0; }
.carrinho ul { list-style: none; padding: 0; }
.carrinho li { display: grid; grid-template-columns: 1fr auto auto; gap: 8px; align-items: center; padding: 6px 0; border-bottom: 1px solid #eee; }
.qtd { display: flex; align-items: center; gap: 6px; }
.qtd button { padding: 2px 8px; }
.total { font-size: 1.1rem; }
```

| Detalhe | Por quê |
|---|---|
| `adicionar` com `some` + `map` | O mesmo produto duas vezes **soma a quantidade**, sem criar outra linha |
| `alterar` com `map` + `filter` | A quantidade que chega a 0 tira o item do carrinho |
| `ehItem` | O carrinho salvo no navegador é conferido antes de usar |
| `@media (min-width: 900px)` | No computador, o carrinho fica ao lado da grade; no celular, embaixo |
| `aria-labelledby` no carrinho | O leitor de tela anuncia a região pelo título “Carrinho (n)” |

### Publicar

1. `vite.config.ts` com `base: "/catalogo/"` (aula 03).
2. `npm run build` e `npm run preview` para testar.
3. Envie o conteúdo de `dist/` para o repositório `catalogo` e ligue o GitHub Pages.

---

## Entrega (requisito do certificado)

1. O **link** do catálogo publicado (`https://seu-usuario.github.io/catalogo/`).
2. A pasta `src/` compactada e a saída do `npm run build` sem erros.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Publicado | O link abre e tudo funciona no celular |
| Estado | Busca e categoria no `App`; lista calculada; carrinho em Context com hook próprio |
| Funciona | Busca, filtro, adicionar (somando), alterar, esvaziar e total corretos |
| Qualidade | Build sem erros de tipo; Console sem erros; acessível pelo teclado |

---

## Exercícios extras

### Básico (fixação)

Acrescente mais três produtos em uma categoria nova, **artes**. O que precisa mudar além do `dados.ts`?

<!-- gabarito -->
??? success "Gabarito — Básico"
    O tipo `Categoria` (acrescente `"artes"`) e uma `<option value="artes">Artes</option>` no `Busca`. Se você esquecer o tipo, o TypeScript acusa erro nos produtos novos: a regra está no tipo.

### Intermediário (aplicação)

Mostre o número de itens do carrinho no topo da página, ao lado do nome da papelaria.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Um componente `IconeCarrinho` com `const { totalItens } = useCarrinho();` (aula 02), colocado no `<header>`. O `header` já está dentro do `<CarrinhoProvider>` no `App`, então funciona sem passar nenhuma prop.

### Avançado (desafio)

Acrescente um botão **Finalizar pedido** que monta uma mensagem com os itens e o total e abre o WhatsApp (`https://wa.me/5511900000000?text=…`).

<!-- gabarito -->
??? success "Gabarito — Avançado"
    No `Carrinho`:
    ```tsx
    const linhas = itens.map((i) => `${i.quantidade}x ${i.produto.nome} — ${brl(i.produto.preco * i.quantidade)}`);
    const texto = ["Olá! Quero fazer este pedido:", ...linhas, `Total: ${brl(totalValor)}`].join("\n");
    const link = `https://wa.me/5511900000000?text=${encodeURIComponent(texto)}`;
    <a href={link} target="_blank" rel="noopener">Finalizar pedido pelo WhatsApp</a>
    ```
    O `encodeURIComponent` transforma quebras de linha, acentos e espaços no formato de endereço. O número é inventado: use o da loja de verdade.

---

## 💡 Resumo

- Estado no lugar certo: busca no `App`, carrinho em Context; listas calculadas.
- Hook próprio (`useCarrinho`) deixa o uso simples e seguro.
- `base` + `build` + `preview` + GitHub Pages = app no ar.

## ➡️ Próximo passo

Parabéns, você terminou o curso de **React** e a trilha **Web ➔ TypeScript ➔ React**! Volte ao [índice do módulo](index.md) e confira o checklist. Daqui, bons próximos passos são o **GitHub Actions** para publicar sozinho, uma biblioteca de rotas (como o React Router) para apps com várias páginas e um *back-end* para guardar os pedidos de verdade.
