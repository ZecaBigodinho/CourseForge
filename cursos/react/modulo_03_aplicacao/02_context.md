# 02 — Context: dados para o app inteiro

> **Curso:** React  
> **Módulo:** 03 — Aplicação completa  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar quando usar **Context** (e quando não usar).
- Criar um Context tipado com `createContext`.
- Escrever um **Provider** que guarda o estado e as funções.
- Criar um hook próprio (`useCarrinho`) que avisa quando está fora do Provider.

## Pré-requisitos

- [Aula 01](01_elevar_o_estado.md) deste módulo.

---

## A ideia

O **Context** é um “canal” por onde um componente lá em cima entrega um valor a **qualquer** componente abaixo dele, sem passar por props em cada nível. Bons candidatos: carrinho, usuário logado, tema claro ou escuro, idioma.

!!! warning "Não use Context para tudo"
    Se o dado é usado por um ou dois componentes próximos, **props** são mais simples e mais fáceis de entender. Context é para dados que o app inteiro (ou boa parte dele) usa.

---

## As três peças

### 1. O contexto e o tipo do valor (`carrinho/contexto.ts`)

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

O valor começa `null`: fora de um Provider, não há carrinho.

### 2. O hook que usa o contexto (`carrinho/useCarrinho.ts`)

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

Com esse hook, quem usa o carrinho recebe sempre um `CarrinhoValor` (nunca `null`), e um esquecimento do Provider vira uma mensagem clara em vez de um erro misterioso.

### 3. O Provider, dono do estado (`carrinho/CarrinhoProvider.tsx`)

```tsx
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
  // alterar, limpar, totalItens e totalValor: veja o projeto completo na aula 04

  return (
    <CarrinhoContext.Provider value={{ itens, totalItens, totalValor, adicionar, alterar, limpar }}>
      {children}
    </CarrinhoContext.Provider>
  );
}
```

É o mesmo estado e as mesmas funções que você já sabe escrever, só que guardados num componente que **envolve** o app.

---

## Usar

No `App`, envolva quem precisa do carrinho:

```tsx
<CarrinhoProvider>
  <Topo />
  <Catalogo />
  <Carrinho />
</CarrinhoProvider>
```

Em qualquer componente lá dentro, em qualquer nível:

```tsx
function CartaoProduto({ produto }: { produto: Produto }) {
  const { adicionar } = useCarrinho();
  return <button type="button" onClick={() => adicionar(produto)}>Adicionar</button>;
}

function IconeCarrinho() {
  const { totalItens } = useCarrinho();
  return <span aria-label={`${totalItens} itens no carrinho`}>🛒 {totalItens}</span>;
}
```

Quando o carrinho muda, **todos** os componentes que usam `useCarrinho()` são redesenhados.

!!! info "Por que três arquivos?"
    O modelo do Vite traz uma regra do ESLint (`react-refresh/only-export-components`) que pede que arquivos de componente exportem **só** componentes, para a atualização instantânea funcionar bem. Por isso o contexto e o hook ficam em arquivos `.ts` separados do Provider.

---

## Exercícios

### Básico (fixação)

Crie o componente `IconeCarrinho` da aula e coloque-o no topo do catálogo.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Crie o arquivo com o código da aula e use `<IconeCarrinho />` dentro do `<header>`. Ele precisa estar **dentro** do `<CarrinhoProvider>`; ao clicar em “Adicionar”, o número do topo e o do carrinho mudam juntos.

### Intermediário (aplicação)

Tire o `<IconeCarrinho />` de dentro do Provider (coloque-o antes de `<CarrinhoProvider>`). O que acontece?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    A página quebra e o Console mostra `Error: useCarrinho precisa estar dentro de <CarrinhoProvider>`. O `useContext` devolveu `null` porque não há Provider acima, e o hook transformou isso numa mensagem clara.

### Avançado (desafio)

Crie um `TemaProvider` com o tema `"claro" | "escuro"` e uma função `alternar`, e um botão que troca o tema aplicando a classe `escuro` no `<body>`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```tsx
    // tema/contexto.ts
    export type Tema = "claro" | "escuro";
    export const TemaContext = createContext<{ tema: Tema; alternar: () => void } | null>(null);

    // tema/TemaProvider.tsx
    export default function TemaProvider({ children }: { children: ReactNode }) {
      const [tema, setTema] = useState<Tema>("claro");
      useEffect(() => {
        document.body.classList.toggle("escuro", tema === "escuro");
      }, [tema]);
      const alternar = () => setTema((t) => (t === "claro" ? "escuro" : "claro"));
      return <TemaContext.Provider value={{ tema, alternar }}>{children}</TemaContext.Provider>;
    }
    ```
    Mais um hook `useTema()` no mesmo formato do `useCarrinho`. Mexer no `<body>` é um efeito, porque está fora do React.

---

## 💡 Resumo

- Context = canal para dados que o app inteiro usa; props continuam sendo a primeira escolha.
- `createContext<Tipo | null>(null)`, um Provider com o estado e um hook `useAlgo()` que confere o `null`.
- Envolva o app com o Provider; use o hook em qualquer nível.

## ➡️ Próximo passo

Na **[aula 03](03_build_e_publicacao.md)** você gera o build e publica o app.
