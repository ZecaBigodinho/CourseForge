# 03 — Build e publicação

> **Curso:** React  
> **Módulo:** 03 — Aplicação completa  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar a diferença entre o modo de **desenvolvimento** e o **build**.
- Configurar a opção **`base`** do Vite para publicar numa subpasta.
- Testar o build com `npm run preview`.
- Publicar o app no **GitHub Pages**.

## Pré-requisitos

- [Aula 02](02_context.md) deste módulo e a [aula de GitHub Pages do curso de Web](../../desenvolvimento_web/modulo_04_publicar/03_github_pages.md).

---

## Desenvolvimento × build

| | `npm run dev` | `npm run build` |
|---|---|---|
| Para quê | Programar | Publicar |
| Arquivos | Servidos direto do `src/`, com atualização instantânea | Gerados em `dist/`, juntos e compactados |
| TypeScript | O editor mostra os erros | O build **para** se houver erro de tipo (`tsc -b`) |
| `StrictMode` | Roda efeitos duas vezes | Não roda nada duas vezes |

A pasta **`dist/`** é o site pronto: só HTML, CSS e JavaScript, que qualquer servidor de arquivos consegue entregar.

---

## A opção `base`

No GitHub Pages, um repositório `catalogo` vira `https://seu-usuario.github.io/catalogo/`: o site fica numa **subpasta**. Por padrão, o Vite gera caminhos a partir da raiz (`/assets/…`), que nesse endereço apontam para o lugar errado, e a página fica em branco.

Diga ao Vite qual é a subpasta, no `vite.config.ts`:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/catalogo/",   // o nome do repositório, entre barras
});
```

Agora o build gera `/catalogo/assets/…`.

!!! warning "Prefira o `vite.config.ts` à linha de comando"
    Também dá para usar `npx vite build --base=/catalogo/`, mas no **Git Bash** do Windows o terminal converte `/catalogo/` num caminho de disco (`C:/Program Files/Git/catalogo/`) e o site quebra. No `vite.config.ts` isso não acontece. Se o repositório for o `seu-usuario.github.io`, o site fica na raiz e o `base` não é necessário.

### Testar o build antes de publicar

```bash
npm run build
npm run preview
```

O `preview` serve a pasta `dist/` como um site de verdade, já com o `base` (o terminal mostra o endereço, como `http://localhost:4173/catalogo/`). Se funcionar aqui, vai funcionar no GitHub Pages.

---

## Publicar no GitHub Pages

### Caminho simples: enviar a pasta `dist/`

1. `npm run build`.
2. No GitHub, crie o repositório `catalogo` (público).
3. **Add file ➔ Upload files** e envie **o conteúdo** da pasta `dist/` (o `index.html` precisa ficar na raiz do repositório).
4. **Settings ➔ Pages** ➔ *Deploy from a branch* ➔ **main**, pasta **/ (root)** ➔ **Save**.
5. Em um ou dois minutos: `https://seu-usuario.github.io/catalogo/`.

Para atualizar: `npm run build` de novo e envie os arquivos novos de `dist/`. Apague os antigos de `assets/`, que mudam de nome a cada build.

!!! tip "O caminho profissional: GitHub Actions"
    Em projetos de verdade, o código-fonte fica no repositório e um **GitHub Actions** roda o `npm run build` e publica sozinho a cada `git push`. Na documentação do Vite (página *Deploying a Static Site*), há um modelo pronto para o GitHub Pages. É um ótimo passo seguinte depois deste curso.

---

## Exercícios

### Básico (fixação)

Rode `npm run build` no projeto do cardápio (Módulo 01) e veja o tamanho dos arquivos que o terminal informa. Qual é o maior?

<!-- gabarito -->
??? success "Gabarito — Básico"
    O `.js` em `dist/assets/` é o maior (algo como 200 KB, ou uns 70 KB compactado com *gzip*): ele contém o React e o seu código. O `.css` e o `index.html` são pequenos. O terminal mostra os dois tamanhos.

### Intermediário (aplicação)

Configure `base: "/cardapio/"`, rode `npm run build` e `npm run preview`. Em que endereço o app abre? E se você acessar sem o `/cardapio/`?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    O `preview` abre em `http://localhost:4173/cardapio/`. Sem a subpasta, a página não encontra os arquivos, exatamente como aconteceria no GitHub Pages com o `base` errado. Por isso testar com o `preview` evita surpresas.

### Avançado (desafio)

Publique o cardápio do Módulo 01 no GitHub Pages e mande o link para alguém abrir no celular.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Repositório `cardapio`, `base: "/cardapio/"`, `npm run build`, envio do conteúdo de `dist/`, **Settings ➔ Pages ➔ main / (root)**. O endereço fica `https://seu-usuario.github.io/cardapio/`. Página em branco? Confira o `base` (deve ser igual ao nome do repositório) e abra o `F12` ➔ **Console** e **Rede** para ver qual arquivo não foi encontrado.

---

## 💡 Resumo

- `npm run dev` para programar; `npm run build` gera o site pronto em `dist/`.
- Publicando numa subpasta? `base: "/nome-do-repositorio/"` no `vite.config.ts`.
- Teste com `npm run preview` antes de publicar.
- GitHub Pages: envie o conteúdo de `dist/` e ligue o Pages na branch `main`.

## ➡️ Próximo passo

Na **[aula 04](04_projeto_catalogo.md)** você monta e publica o projeto final.
