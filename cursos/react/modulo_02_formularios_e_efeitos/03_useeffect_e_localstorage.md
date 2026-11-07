# 03 — useEffect e localStorage

> **Curso:** React  
> **Módulo:** 02 — Listas, formulários e efeitos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que é um **efeito** e quando usar `useEffect`.
- Controlar quando o efeito roda com o **array de dependências**.
- Carregar o estado inicial do `localStorage` com uma função (**inicialização preguiçosa**).
- Salvar automaticamente sempre que o estado mudar.

## Pré-requisitos

- [Aula 02](02_listas.md) deste módulo.

---

## O que é um efeito

O componente React só deve **calcular a tela** a partir das props e do estado. Tudo o que conversa com o mundo de fora é um **efeito**: gravar no `localStorage`, buscar dados de uma API, mudar o título da aba, ligar um temporizador. Esses trabalhos vão dentro de `useEffect`, que roda **depois** que a tela foi desenhada.

```tsx
import { useEffect, useState } from "react";

export default function Contador() {
  const [n, setN] = useState(0);

  useEffect(() => {
    document.title = `Cliques: ${n}`;
  }, [n]);

  return <button type="button" onClick={() => setN((a) => a + 1)}>Clicar ({n})</button>;
}
```

---

## O array de dependências

O segundo argumento diz **quando** o efeito roda de novo:

| Escrita | Roda |
|---|---|
| `useEffect(fn, [n])` | Na primeira vez e sempre que `n` mudar |
| `useEffect(fn, [])` | Só na primeira vez (quando o componente aparece) |
| `useEffect(fn)` | Depois de **toda** renderização (raramente é o que você quer) |

!!! warning "Dependência esquecida"
    Se o efeito usa um valor (como `n`) e ele não está no array, o efeito fica com um valor antigo. O ESLint do projeto do Vite avisa com a regra `react-hooks/exhaustive-deps`: preste atenção a esse aviso.

!!! info "Por que meu efeito rodou duas vezes?"
    Em desenvolvimento, o `StrictMode` monta o componente, desmonta e monta de novo, para revelar efeitos mal escritos. Um efeito correto (como salvar no `localStorage`) não se importa em rodar duas vezes. No site publicado, roda uma só.

---

## Guardar no `localStorage`

### Carregar: inicialização preguiçosa

```tsx
function carregar(): string[] {
  try {
    const dados: unknown = JSON.parse(localStorage.getItem("nomes") ?? "[]");
    return Array.isArray(dados) ? dados.filter((x): x is string => typeof x === "string") : [];
  } catch {
    return [];
  }
}

const [nomes, setNomes] = useState<string[]>(carregar);
```

Passar a **função** `carregar` (sem os parênteses) faz o React chamá-la **só na primeira vez**. Com `useState(carregar())`, ela rodaria a cada renderização, lendo o `localStorage` à toa.

### Salvar: um efeito que depende do estado

```tsx
useEffect(() => {
  localStorage.setItem("nomes", JSON.stringify(nomes));
}, [nomes]);
```

Toda vez que `nomes` muda (acrescentar, remover, editar), o efeito salva. Você não precisa lembrar de chamar `salvar()` em cada função, como na versão do curso de Web.

!!! tip "Nem tudo precisa de efeito"
    Calcular um total, filtrar uma lista ou juntar nome e sobrenome **não** é efeito: faça no corpo do componente. Use `useEffect` só para conversar com algo **fora** do React.

---

## Exercícios

### Básico (fixação)

Mostre no título da aba quantos itens há no carrinho do projeto do Módulo 01.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```tsx
    useEffect(() => {
      document.title = itens > 0 ? `(${itens}) Lanchonete do Bairro` : "Lanchonete do Bairro";
    }, [itens]);
    ```

### Intermediário (aplicação)

Faça o cardápio do Módulo 01 **lembrar** das quantidades ao recarregar a página.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    function carregarQtd(): Record<number, number> {
      try {
        const d: unknown = JSON.parse(localStorage.getItem("pedido") ?? "{}");
        return typeof d === "object" && d !== null ? (d as Record<number, number>) : {};
      } catch {
        return {};
      }
    }
    const [quantidades, setQuantidades] = useState<Record<number, number>>(carregarQtd);
    useEffect(() => {
      localStorage.setItem("pedido", JSON.stringify(quantidades));
    }, [quantidades]);
    ```
    Para uma validação mais rigorosa, confira também se cada valor é um número (como as guardas do curso de TypeScript).

### Avançado (desafio)

Mostre um relógio que atualiza a cada segundo. Use `setInterval` dentro de um efeito e **pare** o temporizador quando o componente sair da tela.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```tsx
    const [agora, setAgora] = useState(new Date());
    useEffect(() => {
      const id = setInterval(() => setAgora(new Date()), 1000);
      return () => clearInterval(id);
    }, []);
    return <p>{agora.toLocaleTimeString("pt-BR")}</p>;
    ```
    A função devolvida pelo efeito é a **limpeza**: o React a chama antes de desmontar o componente (e antes de rodar o efeito de novo). Sem ela, o temporizador continuaria rodando para sempre.

---

## 💡 Resumo

- `useEffect` é para conversar com o mundo de fora; roda depois de desenhar.
- `[]` = só na primeira vez; `[valor]` = quando o valor muda.
- `useState(funcao)` carrega o valor inicial uma vez; o efeito com `[estado]` salva sempre.
- Devolva uma função de limpeza para temporizadores e assinaturas.

## ➡️ Próximo passo

Na **[aula 04](04_buscar_dados.md)** você busca dados de uma API.
