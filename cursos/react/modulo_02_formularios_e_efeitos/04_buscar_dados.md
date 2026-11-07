# 04 — Buscar dados de uma API

> **Curso:** React  
> **Módulo:** 02 — Listas, formulários e efeitos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Buscar dados ao abrir a tela com `useEffect` + `fetch`.
- Representar **carregando**, **erro** e **sucesso** no estado.
- Cancelar um pedido que ficou velho com `AbortController`.
- Buscar dados a partir de uma ação do usuário (envio de formulário).

## Pré-requisitos

- [Aula 03](03_useeffect_e_localstorage.md) deste módulo e a [aula de fetch com tipos](../../typescript/modulo_03_navegador/03_fetch_tipado.md).

---

## Três estados possíveis

Buscar dados leva tempo e pode falhar. Uma **união discriminada** (curso de TypeScript) deixa os três casos claros:

```tsx
type Feriado = { date: string; name: string };

type Estado =
  | { situacao: "carregando" }
  | { situacao: "erro"; mensagem: string }
  | { situacao: "ok"; feriados: Feriado[] };
```

## Buscar ao abrir a tela

```tsx
import { useEffect, useState } from "react";

function ehFeriado(v: unknown): v is Feriado {
  if (typeof v !== "object" || v === null) return false;
  const o = v as Record<string, unknown>;
  return typeof o.date === "string" && typeof o.name === "string";
}

export default function Feriados({ ano }: { ano: number }) {
  const [estado, setEstado] = useState<Estado>({ situacao: "carregando" });

  useEffect(() => {
    const controle = new AbortController();
    setEstado({ situacao: "carregando" });

    async function buscar() {
      try {
        const r = await fetch(`https://brasilapi.com.br/api/feriados/v1/${ano}`, {
          signal: controle.signal,
        });
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const dados: unknown = await r.json();
        const feriados = Array.isArray(dados) ? dados.filter(ehFeriado) : [];
        setEstado({ situacao: "ok", feriados });
      } catch (erro) {
        if (controle.signal.aborted) return;
        setEstado({ situacao: "erro", mensagem: "Não foi possível carregar os feriados." });
      }
    }

    buscar();
    return () => controle.abort();
  }, [ano]);

  if (estado.situacao === "carregando") return <p>Carregando…</p>;
  if (estado.situacao === "erro") return <p role="alert">{estado.mensagem}</p>;

  return (
    <ul>
      {estado.feriados.map((f) => (
        <li key={f.date}>
          {f.date.split("-").reverse().join("/")} — {f.name}
        </li>
      ))}
    </ul>
  );
}
```

| Parte | Por quê |
|---|---|
| `useEffect(…, [ano])` | Busca ao aparecer e de novo quando o `ano` mudar |
| `async function buscar()` dentro do efeito | A função do `useEffect` não pode ser `async` (ela só pode devolver a limpeza) |
| `AbortController` + `return () => controle.abort()` | Se o `ano` mudar (ou o componente sair) antes da resposta, o pedido antigo é **cancelado** e não sobrescreve o novo |
| `if (controle.signal.aborted) return;` | Um pedido cancelado “dá erro”, mas não é um erro para mostrar |
| Guarda `ehFeriado` | Os dados de fora são `unknown` até serem conferidos |
| `role="alert"` | O leitor de tela anuncia a mensagem de erro |

!!! info "Bibliotecas para buscar dados"
    Em projetos maiores, bibliotecas como o **TanStack Query** cuidam de carregamento, erro, cache e cancelamento. Entender a versão “na mão” mostra o que elas fazem por você.

---

## Buscar a partir de uma ação

Quando a busca depende de um clique ou envio, ela **não** precisa de `useEffect`: faça direto no evento.

```tsx
async function buscarCep(evento: FormEvent<HTMLFormElement>) {
  evento.preventDefault();
  setResultado("Buscando…");
  try {
    const r = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    const dados: unknown = await r.json();
    // validar e mostrar, como no curso de TypeScript
  } catch {
    setResultado("Sem conexão.");
  }
}
```

Regra: **o dado deve aparecer porque a tela abriu ou um valor mudou?** Use efeito. **Porque alguém clicou?** Faça no evento.

---

## Exercícios

### Básico (fixação)

Use o componente `Feriados` com o ano 2026 e conte quantos feriados aparecem.

<!-- gabarito -->
??? success "Gabarito — Básico"
    `<Feriados ano={2026} />`. A BrasilAPI devolve 14 feriados nacionais para 2026 (testado em novembro de 2026; o número pode mudar se a lista oficial mudar).

### Intermediário (aplicação)

Acrescente um `<select>` com os anos 2025, 2026 e 2027 que troca os feriados mostrados.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    const [ano, setAno] = useState(2026);
    <select value={ano} onChange={(e) => setAno(Number(e.target.value))}>
      {[2025, 2026, 2027].map((a) => <option key={a} value={a}>{a}</option>)}
    </select>
    <Feriados ano={ano} />
    ```
    Como `ano` está nas dependências do efeito, mudar o `<select>` dispara uma nova busca.

### Avançado (desafio)

No `F12` ➔ **Rede**, ative a limitação de velocidade (*3G lento*) e troque o ano rapidamente várias vezes. O que acontece com os pedidos? E se você apagar a linha `return () => controle.abort();`?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Com o `abort`, cada troca **cancela** o pedido anterior (aparece como *cancelado* na guia Rede) e a tela termina sempre com o ano escolhido por último. Sem ele, os pedidos chegam fora de ordem: uma resposta antiga, mais lenta, pode chegar por último e mostrar os feriados do ano **errado**. Esse problema tem nome: *condição de corrida*.

---

## 💡 Resumo

- Represente carregando, erro e sucesso com uma união discriminada.
- `useEffect` + função `async` interna + `AbortController` na limpeza.
- Valide os dados de fora; mostre erros com `role="alert"`.
- Busca por ação do usuário vai no evento, não num efeito.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_lista_de_tarefas.md)** você monta a lista de tarefas em React.
