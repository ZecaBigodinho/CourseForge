# 01 — Por que React e o primeiro projeto

> **Curso:** React  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar a diferença entre mexer no DOM “na mão” e o jeito do React.
- Criar um projeto com **Vite** no modelo React + TypeScript.
- Rodar o servidor de desenvolvimento e entender a estrutura de pastas.
- Fazer a primeira alteração e ver a página atualizar sozinha.

## Pré-requisitos

- [Desenvolvimento Web](../../desenvolvimento_web/docs/index.md) e [TypeScript](../../typescript/docs/index.md) (Módulos 01 e 02); **Node.js** (LTS) instalado.

---

## O jeito do React

Na lista de tarefas do curso de Web, cada mudança exigia **dois passos**: mudar o array e redesenhar a lista com `createElement`, `append`, `remove`… Era fácil esquecer de atualizar alguma parte da tela.

No React, você só escreve **como a tela deve ficar para os dados atuais**. Quando os dados mudam, o React compara a tela nova com a anterior e atualiza **só o que mudou** no DOM.

| | DOM “na mão” (curso de Web) | React |
|---|---|---|
| Você escreve | Os **passos** para mudar a tela | **Como a tela fica** para cada estado |
| Mudou um dado | Lembrar de atualizar cada elemento | O React redesenha sozinho |
| Organização | Um arquivo de script | **Componentes** reaproveitáveis |

!!! info "Biblioteca, não linguagem"
    React é uma **biblioteca** de JavaScript. Tudo o que você aprendeu (arrays, `map`, objetos, tipos) continua valendo: o React só organiza a construção da interface.

---

## Criar o projeto com Vite

O **Vite** cria a estrutura do projeto e roda um servidor de desenvolvimento rápido. No terminal, na pasta onde quer guardar os projetos:

```bash
npm create vite@latest meu-app -- --template react-ts
cd meu-app
npm install
npm run dev
```

1. `npm create vite@latest meu-app -- --template react-ts`: cria a pasta `meu-app` com React + TypeScript.
2. `npm install`: baixa o React e as ferramentas para a pasta `node_modules/` (leva um minuto, precisa de internet).
3. `npm run dev`: liga o servidor. O terminal mostra um endereço como `http://localhost:5173/`: abra no navegador.

Para parar o servidor: `Ctrl + C` no terminal.

---

## A estrutura do projeto

```text
meu-app/
├── index.html          ← a única página: tem um <div id="root">
├── package.json        ← nome, scripts (dev, build) e dependências
├── tsconfig*.json      ← configuração do TypeScript (já com strict)
├── vite.config.ts
└── src/
    ├── main.tsx        ← liga o React ao <div id="root">
    ├── App.tsx         ← o componente principal
    ├── App.css
    └── index.css
```

O `main.tsx` é curto e quase nunca muda:

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

Ele pega o `<div id="root">` do `index.html` e desenha dentro dele o componente `App`. Arquivos `.tsx` são TypeScript **com JSX**, o “HTML dentro do código” da próxima aula.

!!! tip "O `StrictMode`"
    Em desenvolvimento, o `StrictMode` roda algumas partes do seu código **duas vezes** de propósito, para revelar erros cedo. Se um `console.log` aparecer duplicado, é ele. No site publicado isso não acontece.

---

## A primeira alteração

Apague todo o conteúdo do `src/App.tsx` e escreva:

```tsx
export default function App() {
  return (
    <main>
      <h1>Olá, React!</h1>
      <p>Meu primeiro componente.</p>
    </main>
  );
}
```

Salve: o navegador atualiza **sozinho**, sem recarregar a página. Isso é o *Hot Module Replacement* do Vite.

---

## Exercícios

### Básico (fixação)

Crie o projeto `meu-app`, rode com `npm run dev` e troque o texto do `<h1>` para o seu nome.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Os quatro comandos da aula, depois `<h1>Olá, Ana!</h1>` no `App.tsx`. Ao salvar, o navegador mostra o texto novo na hora. Se aparecer “`npm` não é reconhecido”, o Node.js não está instalado (ou o terminal foi aberto antes da instalação: feche e abra de novo).

### Intermediário (aplicação)

Pare o servidor e rode `npm run build`. O que aparece na pasta `dist/`?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    O `build` confere os tipos e gera a versão final do site em `dist/`: um `index.html` e uma pasta `assets/` com um `.js` e um `.css` juntos e compactados. É essa pasta que vai para a internet (Módulo 03).

### Avançado (desafio)

Abra o `dist/index.html` com dois cliques. A página aparece? Explique e diga como testar a versão final corretamente.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    A página fica em branco: o `index.html` aponta para `/assets/…` (a raiz de um site), e aberto do disco esse caminho não existe; além disso, módulos são bloqueados em `file://` (como no curso de TypeScript). Teste com `npm run preview`, que serve a pasta `dist/` como um site de verdade.

---

## 💡 Resumo

- React: você descreve a tela para os dados atuais; ele atualiza o DOM.
- `npm create vite@latest meu-app -- --template react-ts`, `npm install`, `npm run dev`.
- `main.tsx` liga o React ao `#root`; `App.tsx` é o componente principal.
- `npm run build` gera a versão final em `dist/`; `npm run preview` testa essa versão.

## ➡️ Próximo passo

Na **[aula 02](02_jsx_e_componentes.md)** você escreve JSX e cria componentes.
