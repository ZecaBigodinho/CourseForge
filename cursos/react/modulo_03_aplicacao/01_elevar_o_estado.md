# 01 — Componentizar e elevar o estado

> **Curso:** React  
> **Módulo:** 03 — Aplicação completa  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Dividir uma tela em **componentes** a partir de um rascunho.
- Decidir **onde** cada estado deve morar.
- **Elevar o estado** para o pai comum e passar dados e funções para os filhos.
- Reconhecer o problema do *prop drilling*.

## Pré-requisitos

- [Módulo 02](../modulo_02_formularios_e_efeitos/index.md) completo.

---

## Do rascunho aos componentes

Antes de programar, desenhe a tela (num papel mesmo) e circule as partes:

```text
┌──────────────── App ─────────────────────────────┐
│ Topo                                             │
│ ┌── Busca ───────────────┐   ┌── Carrinho ─────┐ │
│ │ [ texto ] [categoria]  │   │ itens, total    │ │
│ └────────────────────────┘   └─────────────────┘ │
│ ┌ CartaoProduto ┐ ┌ CartaoProduto ┐ …             │
└──────────────────────────────────────────────────┘
```

Cada retângulo vira um componente. Um bom componente tem **uma** responsabilidade e um nome que a descreve.

---

## Onde mora o estado?

Pergunte, para cada dado que muda:

1. **Quem usa** esse dado?
2. Se só **um** componente usa ➔ o estado fica **nele**.
3. Se **vários** usam ➔ o estado fica no **pai comum mais próximo**, que passa o valor por props e recebe as mudanças por funções.

No catálogo:

| Estado | Quem usa | Onde mora |
|---|---|---|
| Texto da busca e categoria | `Busca` (mostra) e a lista (filtra) | `App`, o pai dos dois |
| Itens do carrinho | `CartaoProduto` (adiciona) e `Carrinho` (mostra) | Pai comum ou **Context** (próxima aula) |
| Lista visível | — | **Calculada** no `App`, não é estado |

## Elevar o estado

```tsx
// App.tsx — dono do estado
const [termo, setTermo] = useState("");
const [categoria, setCategoria] = useState<Categoria | "todas">("todas");

const visiveis = PRODUTOS.filter(
  (p) =>
    (categoria === "todas" || p.categoria === categoria) &&
    p.nome.toLowerCase().includes(termo.trim().toLowerCase()),
);

<Busca termo={termo} categoria={categoria} aoMudarTermo={setTermo} aoMudarCategoria={setCategoria} />
```

```tsx
// Busca.tsx — só mostra e avisa
type Props = {
  termo: string;
  categoria: Categoria | "todas";
  aoMudarTermo: (termo: string) => void;
  aoMudarCategoria: (categoria: Categoria | "todas") => void;
};
```

O `Busca` não guarda nada: recebe o valor e avisa as mudanças. Por isso dá para usar a mesma busca em outra tela, ou testá-la sozinha.

!!! tip "Os dados descem, os eventos sobem"
    Props levam dados **de cima para baixo**; funções como `aoMudarTermo` levam os acontecimentos **de baixo para cima**. Esse fluxo de mão única é o que deixa um app React previsível.

---

## O problema do *prop drilling*

Quando o dado precisa descer muitos níveis, componentes do meio passam a receber props só para entregá-las adiante:

```text
App (carrinho) ➔ Pagina ➔ Grade ➔ CartaoProduto (usa adicionar)
```

`Pagina` e `Grade` não usam o carrinho, mas precisam repassá-lo. Isso se chama *prop drilling* (“furar” os componentes com props). Para dados que o app **inteiro** usa, como o carrinho, o usuário logado ou o tema, a solução é o **Context**, na próxima aula.

---

## Exercícios

### Básico (fixação)

No projeto da lista de tarefas (Módulo 02), diga onde mora cada estado: o texto da nova tarefa, a lista de tarefas e o filtro. Por quê?

<!-- gabarito -->
??? success "Gabarito — Básico"
    **Texto da nova tarefa:** no `FormTarefa`, porque só ele usa. **Lista de tarefas:** no `App`, porque o formulário acrescenta, os itens marcam e apagam, e o resumo conta. **Filtro:** no `App`, porque os `Filtros` mostram e a lista usa para calcular as visíveis.

### Intermediário (aplicação)

Extraia do catálogo um componente `Grade` que recebe `produtos: Produto[]` e mostra os cartões ou a mensagem de lista vazia.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    function Grade({ produtos }: { produtos: Produto[] }) {
      if (produtos.length === 0) return <p>Nenhum produto encontrado.</p>;
      return (
        <div className="grade">
          {produtos.map((p) => <CartaoProduto key={p.id} produto={p} />)}
        </div>
      );
    }
    // no App:
    <Grade produtos={visiveis} />
    ```

### Avançado (desafio)

Acrescente uma ordenação (**menor preço**, **maior preço**, **nome**) escolhida num `<select>` dentro do `Busca`. Onde mora esse estado?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    No **`App`**, como a busca, porque o `Busca` mostra a escolha e a lista usa para ordenar. `type Ordem = "menor" | "maior" | "nome";` com `useState<Ordem>("nome")`, passado ao `Busca` com `aoMudarOrdem`. No `App`, depois do `filter`: `.sort((a, b) => ordem === "menor" ? a.preco - b.preco : ordem === "maior" ? b.preco - a.preco : a.nome.localeCompare(b.nome))`. O `filter` já criou um array novo, então o `sort` não altera `PRODUTOS`.

---

## 💡 Resumo

- Desenhe a tela e circule os componentes antes de programar.
- Estado usado por um ➔ fica nele; usado por vários ➔ no pai comum.
- Dados descem por props; eventos sobem por funções.
- *Prop drilling* demais é sinal de que o dado é do app inteiro: Context.

## ➡️ Próximo passo

Na **[aula 02](02_context.md)** você compartilha o carrinho com Context.
