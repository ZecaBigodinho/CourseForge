# 01 — Módulos e tsconfig para o navegador

> **Curso:** TypeScript  
> **Módulo:** 03 — TypeScript no navegador  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Dividir o código em **módulos** com `export` e `import`.
- Configurar o `tsconfig.json` para gerar JavaScript que o navegador entende.
- Carregar o código na página com `<script type="module">`.
- Organizar o projeto em `src/` (TypeScript) e `dist/` (JavaScript gerado).

## Pré-requisitos

- [Módulo 02](../modulo_02_modelando_dados/index.md) completo.

---

## Módulos

Um **módulo** é um arquivo que **exporta** coisas para outros arquivos **importarem**. Assim cada arquivo cuida de um assunto.

`src/tipos.ts`:

```ts
export type Tarefa = {
  id: number;
  texto: string;
  feita: boolean;
};
```

`src/formatar.ts`:

```ts
export function formatarData(d: Date): string {
  return d.toLocaleDateString("pt-BR");
}
```

`src/main.ts`:

```ts
import type { Tarefa } from "./tipos.js";
import { formatarData } from "./formatar.js";

const exemplo: Tarefa = { id: 1, texto: "Estudar módulos", feita: false };
console.log(exemplo.texto, formatarData(new Date()));
```

!!! warning "Por que `.js` no `import` de um arquivo `.ts`?"
    O navegador vai rodar os arquivos **compilados**, que são `.js`. O TypeScript não troca a extensão no `import`, então você já escreve o nome que existirá depois: `"./tipos.js"`. O editor entende e encontra o `tipos.ts`.

- `import type` importa só um **tipo**: some no JavaScript gerado.
- Cada arquivo com `import` ou `export` tem as suas variáveis **isoladas**: nada vaza para os outros arquivos sem ser exportado.

---

## O `tsconfig.json` para o navegador

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

| Opção | Por quê |
|---|---|
| `"module": "es2020"` | Mantém os `import`/`export` no JavaScript gerado, que os navegadores atuais entendem |
| `"lib": ["es2020", "dom"]` | Inclui os tipos do navegador: `document`, `HTMLInputElement`, `localStorage`… |
| `rootDir` / `outDir` | `.ts` em `src/`, `.js` gerado em `dist/` |

No Módulo 01 usamos `"module": "commonjs"` porque o código rodava no **Node**. Para o navegador, o formato é o dos módulos ES.

---

## A página

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Módulos em TypeScript</title>
  <script type="module" src="dist/main.js"></script>
</head>
<body>
  <h1>Abra o Console (F12)</h1>
</body>
</html>
```

- `type="module"` permite `import` e já se comporta como `defer` (roda depois do HTML).
- A página carrega o **`dist/main.js`**, nunca o `.ts`.

!!! danger "Abra pelo Live Server, não com dois cliques"
    Por segurança, os navegadores **bloqueiam módulos** em páginas abertas direto do disco (`file:///…`). O Console mostra um erro de CORS. Abra com o **Live Server** do VS Code, que serve a página como um site (`http://127.0.0.1:5500/…`).

### O fluxo de trabalho

1. Num terminal: `npx tsc --watch` (recompila a cada salvamento).
2. Abra o `index.html` com o **Live Server**.
3. Edite o `.ts`, salve: o `tsc` gera o `.js` e o Live Server recarrega a página.

---

## Exercícios

### Básico (fixação)

Monte o projeto da aula (os três arquivos, o `tsconfig` e a página) e confira no Console a mensagem do `main.ts`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Estrutura: `index.html`, `tsconfig.json`, `src/tipos.ts`, `src/formatar.ts`, `src/main.ts`. Rode `npx tsc` (aparece `dist/` com três `.js`) e abra com o Live Server. O Console mostra “Estudar módulos” e a data de hoje.

### Intermediário (aplicação)

Abra a página com dois cliques no arquivo, em vez do Live Server. O que aparece no Console e por quê?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Um erro dizendo que o script foi bloqueado pela política de **CORS** (origem `null`). Páginas `file://` não podem carregar módulos. Com o Live Server, a página tem um endereço `http://` e os módulos carregam.

### Avançado (desafio)

Abra `dist/main.js` e compare com `src/main.ts`. O que sumiu e o que ficou?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Sumiram a linha `import type { Tarefa } …` e a anotação `: Tarefa` (tipos não existem no JavaScript). Ficaram o `import { formatarData } from "./formatar.js"` e o resto do código, quase igual ao que você escreveu, porque o `target` é moderno.

---

## 💡 Resumo

- Módulos: `export` num arquivo, `import { … } from "./arquivo.js"` no outro; `import type` para tipos.
- `tsconfig`: `"module": "es2020"` e `"lib": ["es2020", "dom"]` para o navegador.
- `<script type="module" src="dist/main.js">` e sempre pelo **Live Server**.
- `npx tsc --watch` + Live Server = recompila e recarrega sozinho.

## ➡️ Próximo passo

Na **[aula 02](02_dom_tipado.md)** você mexe na página com tipos.
