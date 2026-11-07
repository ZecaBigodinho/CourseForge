# 02 — JSX e componentes

> **Curso:** React  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Escrever **JSX** e conhecer as diferenças para o HTML.
- Encaixar valores e expressões com `{}`.
- Criar **componentes** como funções e combiná-los.
- Organizar componentes em arquivos com `export` e `import`.

## Pré-requisitos

- [Aula 01](01_primeiro_projeto.md) deste módulo.

---

## JSX

**JSX** é a sintaxe que parece HTML dentro do JavaScript. O Vite a transforma em chamadas de função que o React entende.

```tsx
const nome = "Ana";
const pontos = 120;

export default function App() {
  return (
    <main className="app">
      <h1>Olá, {nome}!</h1>
      <p>Você tem {pontos} pontos. Faltam {500 - pontos} para o prêmio.</p>
      <img src="/logo.png" alt="Logotipo da escola" />
    </main>
  );
}
```

| HTML | JSX | Por quê |
|---|---|---|
| `class="app"` | `className="app"` | `class` é palavra reservada do JavaScript |
| `for="nome"` | `htmlFor="nome"` | O mesmo motivo |
| `<img>`, `<br>`, `<input>` | `<img />`, `<br />`, `<input />` | Toda tag precisa fechar |
| `onclick="..."` | `onClick={...}` | Eventos em *camelCase*, recebendo uma função (aula 04) |
| `style="color: red"` | `style={{ color: "red" }}` | O estilo é um objeto |

### Chaves `{}`: JavaScript dentro do JSX

Entre `{}` vai qualquer **expressão** (algo que produz um valor): variáveis, contas, chamadas de função, o operador ternário.

```tsx
<p>{pontos >= 100 ? "Cliente ouro" : "Cliente prata"}</p>
<p>{nome.toUpperCase()}</p>
```

`if`, `for` e declarações **não** vão dentro das chaves: elas ficam antes do `return`.

### Um único elemento “pai”

Um componente devolve **um** elemento. Para agrupar sem criar uma `<div>` extra, use o **fragmento** `<>…</>`:

```tsx
return (
  <>
    <h1>Título</h1>
    <p>Texto</p>
  </>
);
```

---

## Componentes

Um **componente** é uma função que devolve JSX. O nome **começa com letra maiúscula**:

```tsx
function Cabecalho() {
  return (
    <header>
      <h1>Lanchonete do Bairro</h1>
      <p>Aberto das 11h às 22h</p>
    </header>
  );
}

function Rodape() {
  return <footer>Pedidos: (11) 90000-0000</footer>;
}

export default function App() {
  return (
    <>
      <Cabecalho />
      <main>Cardápio em breve.</main>
      <Rodape />
    </>
  );
}
```

`<Cabecalho />` “chama” o componente e põe o JSX dele ali. Com letra minúscula, o React acharia que é uma tag HTML.

### Um componente por arquivo

Quando o projeto cresce, cada componente vai para o seu arquivo em `src/components/`:

```tsx
// src/components/Rodape.tsx
export default function Rodape() {
  return <footer>Pedidos: (11) 90000-0000</footer>;
}
```

```tsx
// src/App.tsx
import Rodape from "./components/Rodape";
```

No Vite, o `import` pode ficar **sem** a extensão.

---

## Exercícios

### Básico (fixação)

Crie um componente `Cartao` que mostra um título e um parágrafo fixos e use-o três vezes no `App`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```tsx
    function Cartao() {
      return (
        <article className="cartao">
          <h2>Promoção</h2>
          <p>Combo X-Salada + suco por R$ 24,00.</p>
        </article>
      );
    }
    export default function App() {
      return (
        <main>
          <Cartao />
          <Cartao />
          <Cartao />
        </main>
      );
    }
    ```
    Os três cartões são iguais: na aula 03, as **props** vão deixá-los diferentes.

### Intermediário (aplicação)

Mostre “Bom dia”, “Boa tarde” ou “Boa noite” conforme a hora, calculando o texto antes do `return`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    export default function App() {
      const hora = new Date().getHours();
      let saudacao = "Boa noite";
      if (hora >= 5 && hora < 12) saudacao = "Bom dia";
      else if (hora >= 12 && hora < 18) saudacao = "Boa tarde";
      return <h1>{saudacao}, Ana!</h1>;
    }
    ```

### Avançado (desafio)

Encontre os quatro erros deste JSX:

```tsx
function app() {
  return (
    <h1 class="titulo">Olá</h1>
    <img src="foto.jpg">
  );
}
```

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. O nome do componente deve começar com maiúscula: `App`.
    2. `class` ➔ `className`.
    3. Dois elementos soltos: envolva em `<>…</>` (ou numa `<main>`).
    4. `<img>` precisa fechar e precisa de `alt`: `<img src="foto.jpg" alt="…" />`.

---

## 💡 Resumo

- JSX: `className`, `htmlFor`, tags sempre fechadas, `style` como objeto.
- `{}` encaixa expressões; `if`/`for` ficam antes do `return`.
- Um elemento pai por componente; `<>…</>` agrupa sem criar tag.
- Componentes são funções com nome em maiúscula; um por arquivo em `src/components/`.

## ➡️ Próximo passo

Na **[aula 03](03_props.md)** os componentes passam a receber dados.
