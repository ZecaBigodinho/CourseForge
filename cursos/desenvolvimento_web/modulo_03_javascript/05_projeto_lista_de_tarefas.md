# 05 — Projeto do módulo: lista de tarefas

> **Curso:** Desenvolvimento Web  
> **Módulo:** 03 — JavaScript  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final deste projeto, você terá:

- Uma **lista de tarefas** em que dá para acrescentar, marcar como feita e apagar.
- Os dados **guardados** no `localStorage`: a lista volta ao reabrir a página.
- O código organizado em **funções**, com os dados num array de objetos.

## Pré-requisitos

- Aulas [01](01_variaveis_condicoes_e_lacos.md) a [04](04_eventos_e_formularios.md) deste módulo.

---

## A ideia central: dados ➔ tela

O segredo de apps como este é ter **uma fonte de verdade**: o array `tarefas`. Toda ação (acrescentar, marcar, apagar) muda o **array**, salva e chama `desenhar()`, que refaz a lista na tela a partir dele. A tela nunca é mexida “na mão”. É a mesma ideia que o React vai usar mais à frente.

---

## O HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minhas tarefas</title>
  <link rel="stylesheet" href="style.css">
  <script src="script.js" defer></script>
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

## O CSS (`style.css`)

```css
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; background: #f7f5ff; color: #222; }
.app { max-width: 480px; margin: 40px auto; padding: 24px; background: white; border-radius: 12px; }
#form-tarefa { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
#form-tarefa label { width: 100%; font-weight: 600; }
#nova { flex: 1; padding: 8px; }
button { padding: 8px 12px; border: 0; border-radius: 8px; background: #4f35b5; color: white; cursor: pointer; }
#lista { list-style: none; padding: 0; }
#lista li { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid #eee; }
#lista li span { flex: 1; }
#lista li.feita span { text-decoration: line-through; color: #888; }
.apagar { background: #c62828; }
```

## O JavaScript (`script.js`)

```js
const form = document.querySelector("#form-tarefa");
const campo = document.querySelector("#nova");
const lista = document.querySelector("#lista");
const resumo = document.querySelector("#resumo");

let tarefas = JSON.parse(localStorage.getItem("tarefas")) || [];

function salvar() {
  localStorage.setItem("tarefas", JSON.stringify(tarefas));
}

function desenhar() {
  lista.innerHTML = "";
  tarefas.forEach((tarefa, indice) => {
    const li = document.createElement("li");
    if (tarefa.feita) li.classList.add("feita");

    const caixa = document.createElement("input");
    caixa.type = "checkbox";
    caixa.checked = tarefa.feita;
    caixa.setAttribute("aria-label", `Marcar "${tarefa.texto}" como feita`);
    caixa.addEventListener("change", () => alternar(indice));

    const texto = document.createElement("span");
    texto.textContent = tarefa.texto;

    const botao = document.createElement("button");
    botao.textContent = "Apagar";
    botao.classList.add("apagar");
    botao.addEventListener("click", () => apagar(indice));

    li.append(caixa, texto, botao);
    lista.append(li);
  });

  const feitas = tarefas.filter((t) => t.feita).length;
  resumo.textContent = `${feitas} de ${tarefas.length} tarefas feitas`;
}

function adicionar(texto) {
  tarefas.push({ texto, feita: false });
  salvar();
  desenhar();
}

function alternar(indice) {
  tarefas[indice].feita = !tarefas[indice].feita;
  salvar();
  desenhar();
}

function apagar(indice) {
  tarefas.splice(indice, 1);
  salvar();
  desenhar();
}

form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  const texto = campo.value.trim();
  if (texto === "") return;
  adicionar(texto);
  campo.value = "";
  campo.focus();
});

desenhar();
```

| Parte | O que faz |
|---|---|
| `JSON.parse(… ) \|\| []` | Carrega as tarefas salvas ou começa vazio |
| `desenhar()` | Apaga a lista da tela e a refaz a partir do array |
| `adicionar` / `alternar` / `apagar` | Mudam o array, salvam e redesenham |
| `splice(indice, 1)` | Remove 1 item na posição `indice` |
| `trim()` | Tira espaços do começo e do fim (impede tarefa “em branco”) |
| `aria-label` | Diz ao leitor de tela o que cada caixa marca |

!!! tip "Usar `innerHTML = \"\"` aqui é seguro"
    Ele só **apaga** a lista. O texto das tarefas entra com `textContent`, que nunca vira código.

---

## Entrega

1. A pasta do projeto compactada (`index.html`, `style.css`, `script.js`).
2. Um print com pelo menos 4 tarefas, 2 marcadas como feitas.
3. Teste: feche e reabra a página. A lista continua lá?

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Funciona | Acrescenta, marca, desmarca e apaga, sem erros no Console |
| Guarda os dados | A lista volta ao reabrir a página |
| Organização | Dados num array de objetos; funções com nomes claros |
| Segurança e acessibilidade | Texto com `textContent`; `label` no campo; `aria-label` nas caixas |

---

## Exercícios extras

### Básico (fixação)

Acrescente um botão **Limpar feitas** que apaga todas as tarefas marcadas.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```js
    document.querySelector("#limpar").addEventListener("click", () => {
      tarefas = tarefas.filter((t) => !t.feita);
      salvar();
      desenhar();
    });
    ```
    `filter` fica só com as **não** feitas. Por isso `tarefas` foi declarada com `let`.

### Intermediário (aplicação)

Impeça tarefas **repetidas** (mesmo texto, sem diferenciar maiúsculas e minúsculas) e avise na página.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    No `submit`, antes de `adicionar(texto)`:
    ```js
    const repetida = tarefas.some((t) => t.texto.toLowerCase() === texto.toLowerCase());
    if (repetida) {
      resumo.textContent = "Essa tarefa já está na lista.";
      return;
    }
    ```

### Avançado (desafio)

Crie três botões de filtro, **Todas**, **A fazer** e **Feitas**, que mudam o que aparece na tela sem apagar nada do array.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Guarde o filtro numa variável (`let filtro = "todas";`) e, em `desenhar()`, percorra só as tarefas que passam:
    ```js
    const visiveis = tarefas
      .map((tarefa, indice) => ({ tarefa, indice }))
      .filter(({ tarefa }) =>
        filtro === "todas" || (filtro === "feitas" ? tarefa.feita : !tarefa.feita));
    ```
    Use `visiveis.forEach(({ tarefa, indice }) => …)` no lugar do `tarefas.forEach`. Guardar o **índice original** garante que marcar ou apagar mexe na tarefa certa do array. Cada botão muda `filtro` e chama `desenhar()`.

---

## 💡 Resumo

- Uma fonte de verdade (o array) e uma função que desenha a tela a partir dela.
- Cada ação: muda o array ➔ `salvar()` ➔ `desenhar()`.
- `localStorage` + JSON guardam a lista entre visitas.
- Texto do usuário sempre com `textContent`.

## ➡️ Próximo passo

Você terminou o **Módulo 03**. Volte ao [índice do módulo](index.md) e confira o checklist. Depois, siga para o **[Módulo 04 — Publicar](../modulo_04_publicar/index.md)**, que vai pôr seus projetos na internet.
