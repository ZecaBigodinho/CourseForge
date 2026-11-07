# Módulo 03 — TypeScript no navegador

> **Curso:** TypeScript  
> **Módulo:** 03 · TypeScript no navegador  
> **Descrição:** Levar o TypeScript para a página: módulos, DOM com tipos, dados de APIs conferidos e a lista de tarefas reescrita.

---

## 📋 Visão Geral do Módulo

Os Módulos 01 e 02 rodaram no terminal. Agora o TypeScript vai para o **navegador**: você divide o código em **módulos**, configura o `tsconfig` para gerar JavaScript que a página entende, usa o DOM com tipos (o editor passa a saber que `campo.value` existe) e busca dados de APIs conferindo o que chega. No projeto, reescreve a **lista de tarefas** do curso de Web, agora com o compilador do seu lado.

---

## 📚 Capítulos

- [01. Módulos e tsconfig para o navegador](01_modulos_e_tsconfig.md)
- [02. DOM com tipos](02_dom_tipado.md)
- [03. fetch com tipos](03_fetch_tipado.md)
- [04. Projeto final: lista de tarefas em TypeScript](04_projeto_lista_de_tarefas.md)

---

## 🎯 Objetivos do Módulo

Ao final deste módulo, você será capaz de:

- Dividir o código em módulos com `export` e `import` e carregá-los com `<script type="module">`.
- Configurar o `tsconfig.json` para o navegador (`module`, `lib: ["dom"]`).
- Usar `querySelector`, eventos e elementos do DOM com os tipos certos.
- Buscar dados com `fetch` e **validar** o que chegou antes de usar.

---

## 🧭 Antes de começar

- **Pré-requisitos:** Módulos [01](../modulo_01_fundamentos/index.md) e [02](../modulo_02_modelando_dados/index.md); a [lista de tarefas do curso de Web](../../desenvolvimento_web/modulo_03_javascript/05_projeto_lista_de_tarefas.md).
- **Tempo estimado:** ~6 h (estimativa, ajuste ao ritmo da turma)
- **Ao final você terá:** a lista de tarefas em TypeScript, dividida em módulos, compilando sem erros no modo `strict`.

## ✅ Checklist do módulo

- [ ] Abrir uma página que usa `<script type="module">` pelo Live Server.
- [ ] Explicar por que o `import` usa `.js` mesmo no arquivo `.ts`.
- [ ] Pegar um `<input>` com o tipo `HTMLInputElement` sem usar `!`.
- [ ] Validar um JSON `unknown` antes de tratá-lo como um tipo meu.

## ➡️ Próximo passo

Comece pela **[aula 01 — Módulos e tsconfig para o navegador](01_modulos_e_tsconfig.md)**.
