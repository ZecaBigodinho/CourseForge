# 01 — Por que TypeScript e o primeiro programa

> **Curso:** TypeScript  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que o TypeScript acrescenta ao JavaScript.
- Criar um projeto com `npm` e instalar o TypeScript nele.
- Configurar o `tsconfig.json` com o modo `strict`.
- Compilar com `tsc`, rodar com `node` e ler as **mensagens de erro**.

## Pré-requisitos

- [JavaScript do curso de Desenvolvimento Web](../../desenvolvimento_web/modulo_03_javascript/index.md) e o **Node.js** (versão LTS) instalado.

---

## O problema que o TypeScript resolve

Este JavaScript tem dois erros, mas roda sem reclamar:

```js
const lanche = { nome: "X-Salada", preco: 18 };
console.log(lanche.prco * 2);     // NaN: "prco" não existe
console.log("Total: " + 18 + 2);  // "Total: 182"
```

Você só descobre quando alguém usa o site e vê `NaN` na tela. O **TypeScript** confere o código **antes de rodar**. No VS Code, o erro aparece sublinhado em vermelho enquanto você digita:

```text
A propriedade 'prco' não existe no tipo '{ nome: string; preco: number; }'. Você quis dizer 'preco'?
```

| | JavaScript | TypeScript |
|---|---|---|
| Arquivos | `.js` | `.ts` |
| Erros de tipo | Aparecem **rodando** (para o usuário) | Aparecem **escrevendo** (para você) |
| Roda no navegador e no Node | Direto | Depois de **compilado** para `.js` |
| Autocompletar do editor | Limitado | Completo: o editor sabe o que cada objeto tem |

!!! info "TypeScript não roda sozinho"
    O navegador e o Node entendem JavaScript. O **compilador** (`tsc`) confere os tipos e gera um `.js` sem eles. Os tipos existem só para ajudar você enquanto programa.

---

## Criar o projeto

No terminal do VS Code (`Ctrl + '`), numa pasta nova `curso-ts`:

```bash
npm init -y
npm install --save-dev typescript
npx tsc --init
```

1. `npm init -y` cria o `package.json`, a “ficha” do projeto.
2. `npm install --save-dev typescript` instala o compilador **só neste projeto** (pasta `node_modules/`).
3. `npx tsc --init` cria o `tsconfig.json`, com as configurações do compilador.

### O `tsconfig.json`

O arquivo gerado tem muitas opções comentadas. Para o curso, deixe assim:

```json
{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

| Opção | O que faz |
|---|---|
| `target` | Para qual versão de JavaScript compilar |
| `rootDir` / `outDir` | Os `.ts` ficam em `src/`; os `.js` gerados vão para `dist/` |
| `strict` | Liga **todas** as conferências importantes. Sempre `true` |

---

## O primeiro programa

Crie `src/ola.ts`:

```ts
const nome: string = "Ana";
let idade: number = 17;
console.log(`${nome} tem ${idade} anos`);
```

Compile e rode:

```bash
npx tsc
node dist/ola.js
```

A saída é `Ana tem 17 anos`. Abra `dist/ola.js`: é o mesmo código, **sem** os `: string` e `: number`.

!!! tip "Compilar sozinho a cada salvamento"
    `npx tsc --watch` fica de olho nos arquivos e recompila sempre que você salva. Deixe rodando num terminal e use outro para o `node`.

---

## Ler as mensagens de erro

Troque a segunda linha por `let idade: number = "dezessete";` e rode `npx tsc`:

```text
src/ola.ts(2,5): error TS2322: Type 'string' is not assignable to type 'number'.
```

- `src/ola.ts(2,5)`: arquivo, **linha 2**, coluna 5.
- `TS2322`: o código do erro (bom para pesquisar).
- A mensagem: o tipo `string` não pode ser atribuído ao tipo `number`.

!!! tip "Mensagens em português"
    Rode `npx tsc --locale pt-br` para ver as mensagens traduzidas, como “O tipo 'string' não pode ser atribuído ao tipo 'number'.”. No VS Code, as mensagens seguem o idioma do editor.

Por padrão, o `tsc` **gera o `.js` mesmo com erros**. Corrija sempre antes de rodar.

---

## Exercícios

### Básico (fixação)

Crie `src/apresentacao.ts` com três constantes tipadas (`nome`, `cidade`, `anoNascimento`) e mostre uma frase com elas.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    const nome: string = "Ana";
    const cidade: string = "São Paulo";
    const anoNascimento: number = 2009;
    console.log(`${nome}, de ${cidade}, nasceu em ${anoNascimento}.`);
    ```
    `npx tsc` e depois `node dist/apresentacao.js`.

### Intermediário (aplicação)

Escreva de propósito três erros diferentes (tipo errado, propriedade inexistente, variável não declarada) e anote a mensagem e a linha de cada um.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Exemplos, com `--locale pt-br`: `let n: number = "5";` ➔ “O tipo 'string' não pode ser atribuído ao tipo 'number'.” (TS2322); `objeto.prco` ➔ “A propriedade 'prco' não existe… Você quis dizer 'preco'?” (TS2551); usar `totl` sem declarar ➔ “Não é possível encontrar o nome 'totl'.” (TS2304). A linha e a coluna aparecem entre parênteses depois do nome do arquivo.

### Avançado (desafio)

Mude `"strict": true` para `false` e escreva `function dobro(x) { return x * 2; }`. Compile com as duas configurações e explique a diferença.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Com `strict: true`, o `tsc` acusa “O parâmetro 'x' implicitamente tem um tipo 'any'.” (TS7006): ele não sabe o tipo de `x` e se recusa a adivinhar. Com `strict: false`, compila sem aviso, e `x` vira `any` (qualquer coisa), o que desliga a conferência e permite `dobro("oi")`. Por isso o curso usa sempre `strict: true`.

---

## 💡 Resumo

- TypeScript = JavaScript + tipos conferidos **antes** de rodar.
- `npm init -y`, `npm install --save-dev typescript`, `npx tsc --init`.
- `tsconfig.json` com `rootDir: "src"`, `outDir: "dist"` e **`strict: true`**.
- `npx tsc` compila; `node dist/arquivo.js` roda; a mensagem diz arquivo, linha e motivo.

## ➡️ Próximo passo

Na **[aula 02](02_tipos_basicos.md)** você conhece os tipos básicos e a inferência.
