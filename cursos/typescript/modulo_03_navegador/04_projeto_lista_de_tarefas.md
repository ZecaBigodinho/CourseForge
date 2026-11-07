# 04 — Projeto final: lista de tarefas em TypeScript

> **Curso:** TypeScript
> **Módulo:** 03 — TypeScript no navegador
> **Tempo estimado:** 2 h

---

## Objetivos

Ao final deste projeto, você terá:

- A **lista de tarefas** do curso de Web reescrita em TypeScript, dividida em **módulos**.
- Elementos do DOM com tipos conferidos, sem `as` nem `!`.
- Os dados do `localStorage` **validados** ao carregar.
- O projeto compilando sem erros com `strict: true` (requisito do certificado).

## Pré-requisitos

- Aulas [01](01_modulos_e_tsconfig.md) a [03](03_fetch_tipado.md) deste módulo e o [projeto em JavaScript](../../desenvolvimento_web/modulo_03_javascript/05_projeto_lista_de_tarefas.md).

---

## O que muda em relação à versão em JavaScript

| Na versão JS | Na versão TS |
|---|---|
| Um `script.js` | Três módulos: `tipos.ts`, `armazenamento.ts`, `main.ts` |
| Tarefas identificadas pela **posição** no array | Cada tarefa tem um **`id`**: apagar ou marcar mexe sempre na tarefa certa |
| `JSON.parse` confiado | Dados do `localStorage` validados com uma **guarda de tipo** |
| Elementos pegos com `querySelector` | Função `pegar(seletor, Tipo)` com `instanceof` |
| Array alterado no lugar (`push`, `splice`) | Um **array novo** a cada ação (`map`, `filter`, `...`), o estilo que o React usa |

---

## Estrutura

```text
tarefas-ts/
├── index.html
├── style.css            ← o mesmo do projeto em JavaScript
├── tsconfig.json
├── package.json
├── src/
│   ├── tipos.ts
│   ├── armazenamento.ts
│   └── main.ts
└── dist/                ← gerado pelo npx tsc
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "es2020",
    "module": "es2020",
    "lib": ["es2020", "dom"],
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "skipLibCheck": true
  }
}
```

### `index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minhas tarefas</title>
  <link rel="stylesheet" href="style.css">
  <script type="module" src="dist/main.js"></script>
</head>
<body>
  <main class="app">
    <h1>Minhas tarefas</h1>
    <form id="form-tarefa">
      <label for="nova">Nova tarefa</label>
      <input type="text" id="nova" maxlength="80" required>
      <button type="submit">Adicionar</button>
    </form>
    <ul id="lista"></ul>
    <p id="resumo"></p>
  </main>
</body>
</html>
```

O `style.css` é o mesmo do [projeto em JavaScript](../../desenvolvimento_web/modulo_03_javascript/05_projeto_lista_de_tarefas.md).

### `src/tipos.ts`

```ts
export type Tarefa = {
  id: number;
  texto: string;
  feita: boolean;
};
```

### `src/armazenamento.ts`

```ts
import type { Tarefa } from "./tipos.js";

const CHAVE = "tarefas";

function ehTarefa(valor: unknown): valor is Tarefa {
  if (typeof valor !== "object" || valor === null) return false;
  const v = valor as Record<string, unknown>;
  return typeof v.id === "number" && typeof v.texto === "string" && typeof v.feita === "boolean";
}

export function carregar(): Tarefa[] {
  try {
    const dados: unknown = JSON.parse(localStorage.getItem(CHAVE) ?? "[]");
    return Array.isArray(dados) ? dados.filter(ehTarefa) : [];
  } catch {
    return [];
  }
}

export function salvar(tarefas: Tarefa[]): void {
  localStorage.setItem(CHAVE, JSON.stringify(tarefas));
}
```

### `src/main.ts`

```ts
import type { Tarefa } from "./tipos.js";
import { carregar, salvar } from "./armazenamento.js";

function pegar<T extends HTMLElement>(seletor: string, tipo: { new (): T }): T {
  const el = document.querySelector(seletor);
  if (!(el instanceof tipo)) {
    throw new Error(`Elemento ${seletor} não encontrado`);
  }
  return el;
}

const form = pegar("#form-tarefa", HTMLFormElement);
const campo = pegar("#nova", HTMLInputElement);
const lista = pegar("#lista", HTMLUListElement);
const resumo = pegar("#resumo", HTMLParagraphElement);

let tarefas: Tarefa[] = carregar();

function atualizar(novas: Tarefa[]): void {
  tarefas = novas;
  salvar(tarefas);
  desenhar();
}

function criarItem(tarefa: Tarefa): HTMLLIElement {
  const li = document.createElement("li");
  li.classList.toggle("feita", tarefa.feita);

  const caixa = document.createElement("input");
  caixa.type = "checkbox";
  caixa.checked = tarefa.feita;
  caixa.setAttribute("aria-label", `Marcar "${tarefa.texto}" como feita`);
  caixa.addEventListener("change", () => {
    atualizar(tarefas.map((t) => (t.id === tarefa.id ? { ...t, feita: !t.feita } : t)));
  });

  const texto = document.createElement("span");
  texto.textContent = tarefa.texto;

  const botao = document.createElement("button");
  botao.type = "button";
  botao.textContent = "Apagar";
  botao.classList.add("apagar");
  botao.addEventListener("click", () => {
    atualizar(tarefas.filter((t) => t.id !== tarefa.id));
  });

  li.append(caixa, texto, botao);
  return li;
}

function desenhar(): void {
  lista.replaceChildren(...tarefas.map(criarItem));
  const feitas = tarefas.filter((t) => t.feita).length;
  resumo.textContent = `${feitas} de ${tarefas.length} tarefas feitas`;
}

form.addEventListener("submit", (evento: SubmitEvent) => {
  evento.preventDefault();
  const texto = campo.value.trim();
  if (texto === "") return;
  atualizar([...tarefas, { id: Date.now(), texto, feita: false }]);
  campo.value = "";
  campo.focus();
});

desenhar();
```

Rode `npx tsc` (ou `npx tsc --watch`) e abra o `index.html` com o **Live Server**.

| Detalhe | Por quê |
|---|---|
| `ehTarefa` + `filter` | Se algo estranho foi salvo no `localStorage`, os itens inválidos são descartados em vez de quebrar a página |
| `atualizar(novas)` | Toda mudança passa por um só lugar: troca o array, salva e redesenha |
| `{ ...t, feita: !t.feita }` | Cria uma cópia da tarefa com `feita` invertido, sem alterar a original |
| `replaceChildren(...)` | Troca todo o conteúdo da lista de uma vez, sem `innerHTML` |
| `id: Date.now()` | Um número diferente a cada milissegundo: serve de identificador simples |

---

## Entrega (requisito do certificado)

1. A pasta do projeto compactada, **sem** `node_modules/` (ela é recriada com `npm install`).
2. Um print do terminal com `npx tsc` **sem erros** e um da lista funcionando no navegador.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Compila | `strict: true`, zero erros, nenhum `any`, `as HTML…` ou `!` para elementos |
| Módulos | Pelo menos três arquivos com `import`/`export` |
| Funciona | Acrescenta, marca, apaga e guarda entre visitas |
| Validação | Dados do `localStorage` conferidos com guarda de tipo |

---

## Exercícios extras

### Básico (fixação)

Acrescente o botão **Limpar feitas** (como no projeto JS), agora com a função `pegar` e `atualizar`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    No HTML: `<button type="button" id="limpar">Limpar feitas</button>`. No `main.ts`:
    ```ts
    const limpar = pegar("#limpar", HTMLButtonElement);
    limpar.addEventListener("click", () => atualizar(tarefas.filter((t) => !t.feita)));
    ```

### Intermediário (aplicação)

Acrescente ao tipo `Tarefa` a data de criação (`criadaEm: string`) e mostre-a ao lado do texto. O que acontece com as tarefas já salvas sem esse campo?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Acrescente `criadaEm: string` ao tipo, preencha com `new Date().toISOString()` ao criar e mostre com `new Date(tarefa.criadaEm).toLocaleDateString("pt-BR")`. Se você atualizar a guarda `ehTarefa` para exigir `criadaEm`, as tarefas antigas **somem** ao carregar, porque não passam na validação. Para mantê-las, torne o campo opcional (`criadaEm?: string`) ou “migre” os dados antigos acrescentando uma data padrão.

### Avançado (desafio)

Implemente os filtros **Todas / A fazer / Feitas** com um tipo literal para o filtro atual.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    type Filtro = "todas" | "afazer" | "feitas";
    let filtro: Filtro = "todas";

    function visiveis(): Tarefa[] {
      switch (filtro) {
        case "todas": return tarefas;
        case "afazer": return tarefas.filter((t) => !t.feita);
        case "feitas": return tarefas.filter((t) => t.feita);
      }
    }
    ```
    Em `desenhar()`, use `visiveis().map(criarItem)`. Como cada tarefa tem `id`, marcar e apagar continuam certos mesmo com a lista filtrada, um problema que a versão por posição tinha.

---

## 💡 Resumo

- Módulos separam tipos, armazenamento e tela.
- `pegar(seletor, Tipo)` e guardas de tipo eliminam `as`, `!` e `any`.
- Um `id` por tarefa e arrays novos a cada ação deixam o código previsível.
- `npx tsc` sem erros no `strict`: o compilador revisou o seu código inteiro.

## ➡️ Próximo passo

Parabéns, você terminou o curso de **TypeScript**! Volte ao [índice do módulo](index.md) e confira o checklist. O próximo passo da trilha é o curso de **[React](../../react/docs/index.md)**.
