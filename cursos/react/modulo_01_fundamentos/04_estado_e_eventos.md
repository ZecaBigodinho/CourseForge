# 04 — Estado e eventos

> **Curso:** React  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Guardar dados que mudam com **`useState`**.
- Responder a **eventos** (`onClick`, `onChange`).
- Atualizar o estado com a **forma funcional** quando o novo valor depende do anterior.
- Atualizar objetos e arrays no estado **sem alterá-los no lugar**.

## Pré-requisitos

- [Aula 03](03_props.md) deste módulo.

---

## `useState`

Variáveis comuns não fazem a tela mudar: o React não fica sabendo. Para dados que mudam, use o **estado**:

```tsx
import { useState } from "react";

export default function Contador() {
  const [curtidas, setCurtidas] = useState(0);

  return (
    <div>
      <p>{curtidas} curtidas</p>
      <button type="button" onClick={() => setCurtidas(curtidas + 1)}>
        Curtir
      </button>
    </div>
  );
}
```

- `useState(0)` cria o estado com valor inicial `0` e devolve um par: o **valor atual** e a **função que o troca**.
- Chamar `setCurtidas(novoValor)` guarda o valor e faz o React **redesenhar** o componente.
- Funções que começam com `use` são **hooks**. Chame-as sempre no começo do componente, nunca dentro de `if` ou laços.

---

## Eventos

```tsx
<button type="button" onClick={() => alert("Clicou!")}>Clique</button>
```

Passe uma **função** para `onClick`, e não o resultado de uma chamada: `onClick={salvar}` ou `onClick={() => salvar(id)}`, nunca `onClick={salvar()}` (isso rodaria a função na hora de desenhar).

Para campos de formulário, `onChange` recebe o evento:

```tsx
const [nome, setNome] = useState("");

<input value={nome} onChange={(e) => setNome(e.target.value)} />
<p>Olá, {nome || "visitante"}!</p>
```

---

## A forma funcional: quando o novo valor depende do anterior

Este código parece certo, mas tem uma armadilha:

```tsx
function somarDois() {
  setCurtidas(curtidas + 1);
  setCurtidas(curtidas + 1); // continua usando o MESMO valor antigo
}
```

Dentro da função, `curtidas` é o valor **daquela renderização**. As duas linhas calculam `0 + 1`, e o resultado é **1**, não 2. Quando o novo valor depende do anterior, passe uma **função** para o `set`:

```tsx
function somarDois() {
  setCurtidas((atual) => atual + 1);
  setCurtidas((atual) => atual + 1); // agora dá 2
}
```

O React chama cada função com o valor **mais recente**.

!!! info "Isso aconteceu de verdade neste curso"
    Ao testar o projeto da aula 05, cliques muito rápidos em sequência perdiam itens do pedido, porque o código usava o valor antigo do estado. A correção foi exatamente a forma funcional. Regra: **o novo valor depende do anterior? Use `set(atual => …)`.**

---

## Objetos e arrays no estado: sempre um novo

O React só percebe a mudança se você entregar um **objeto ou array novo**. Alterar o existente não redesenha a tela:

```tsx
type Pedido = { cliente: string; itens: string[] };
const [pedido, setPedido] = useState<Pedido>({ cliente: "Ana", itens: [] });

// ERRADO: altera o objeto que já existe
// pedido.itens.push("X-Salada"); setPedido(pedido);

// CERTO: cria cópias com o espalhamento (...)
setPedido((atual) => ({ ...atual, itens: [...atual.itens, "X-Salada"] }));
```

| Para… | Faça |
|---|---|
| Acrescentar ao array | `[...lista, novo]` |
| Remover do array | `lista.filter((x) => x.id !== id)` |
| Trocar um item | `lista.map((x) => (x.id === id ? { ...x, feita: true } : x))` |
| Mudar uma propriedade | `{ ...objeto, nome: "Bia" }` |

---

## Exercícios

### Básico (fixação)

Faça um contador com botões **−** e **+** que nunca fica negativo.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```tsx
    const [n, setN] = useState(0);
    <button type="button" onClick={() => setN((a) => Math.max(0, a - 1))} disabled={n === 0}>−</button>
    <span>{n}</span>
    <button type="button" onClick={() => setN((a) => a + 1)}>+</button>
    ```

### Intermediário (aplicação)

Crie um campo de texto e mostre embaixo quantos caracteres foram digitados e o texto em maiúsculas.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    const [texto, setTexto] = useState("");
    <label htmlFor="t">Mensagem</label>
    <input id="t" value={texto} onChange={(e) => setTexto(e.target.value)} />
    <p>{texto.length} caracteres · {texto.toUpperCase()}</p>
    ```
    Valores calculados a partir do estado (o tamanho, as maiúsculas) **não** precisam de outro `useState`: calcule direto no corpo do componente.

### Avançado (desafio)

Guarde no estado uma lista de nomes. Um campo e um botão **Adicionar** acrescentam um nome; cada nome tem um botão **×** que o remove.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```tsx
    type Pessoa = { id: number; nome: string };
    const [pessoas, setPessoas] = useState<Pessoa[]>([]);
    const [novo, setNovo] = useState("");

    function adicionar() {
      if (novo.trim() === "") return;
      setPessoas((atual) => [...atual, { id: Date.now(), nome: novo.trim() }]);
      setNovo("");
    }
    // JSX:
    <input value={novo} onChange={(e) => setNovo(e.target.value)} />
    <button type="button" onClick={adicionar}>Adicionar</button>
    <ul>
      {pessoas.map((p) => (
        <li key={p.id}>
          {p.nome}{" "}
          <button type="button" onClick={() => setPessoas((atual) => atual.filter((x) => x.id !== p.id))}>×</button>
        </li>
      ))}
    </ul>
    ```

---

## 💡 Resumo

- `const [valor, setValor] = useState(inicial)`; o `set` redesenha a tela.
- Eventos recebem **funções**: `onClick={() => …}`.
- Novo valor depende do anterior? `setValor((atual) => …)`.
- Objetos e arrays no estado: sempre uma **cópia nova** (`...`, `map`, `filter`).

## ➡️ Próximo passo

Na **[aula 05](05_projeto_cardapio.md)** você junta tudo num cardápio com pedido.
