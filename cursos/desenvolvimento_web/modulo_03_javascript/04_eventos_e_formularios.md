# 04 — Eventos e formulários

> **Curso:** Desenvolvimento Web  
> **Módulo:** 03 — JavaScript  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Reagir a **eventos** com `addEventListener` (clique, digitação, envio).
- Ler os valores de um **formulário** e impedir o recarregamento com `preventDefault`.
- Validar dados e mostrar mensagens na página.
- Guardar e recuperar dados com **`localStorage`**.

## Pré-requisitos

- [Aula 03](03_dom.md) deste módulo.

---

## Eventos

Um **evento** é algo que acontece na página: um clique, uma tecla, o envio de um formulário. Você “escuta” o evento e diz o que fazer:

```html
<button id="curtir">Curtir</button>
<p id="contador">0 curtidas</p>
```

```js
const botao = document.querySelector("#curtir");
const contador = document.querySelector("#contador");
let curtidas = 0;

botao.addEventListener("click", () => {
  curtidas++;
  contador.textContent = `${curtidas} curtidas`;
});
```

| Evento | Acontece quando |
|---|---|
| `click` | Clica (ou toca, no celular) |
| `input` | O valor de um campo muda, a cada tecla |
| `change` | Um campo muda e perde o foco (selects, caixas) |
| `submit` | Um formulário é enviado |
| `keydown` | Uma tecla é pressionada |

---

## Formulários

```html
<form id="form-imc">
  <label for="peso">Peso (kg)</label>
  <input type="number" id="peso" step="0.1" required>
  <label for="altura">Altura (m)</label>
  <input type="number" id="altura" step="0.01" required>
  <button type="submit">Calcular</button>
</form>
<p id="resultado"></p>
```

```js
const form = document.querySelector("#form-imc");

form.addEventListener("submit", (evento) => {
  evento.preventDefault();  // não recarrega a página

  const peso = Number(document.querySelector("#peso").value);
  const altura = Number(document.querySelector("#altura").value);

  if (altura <= 0) {
    document.querySelector("#resultado").textContent = "Altura inválida.";
    return;
  }

  const imc = peso / (altura * altura);
  document.querySelector("#resultado").textContent = `Seu IMC é ${imc.toFixed(1)}.`;
});
```

- Escute o **`submit` do formulário**, e não o clique do botão: assim o `Enter` também funciona e o `required` do HTML continua valendo.
- `preventDefault()` impede o comportamento padrão (enviar e recarregar).
- `.value` é **sempre texto**: converta com `Number()`.

---

## `localStorage`: guardar no navegador

O `localStorage` guarda textos no navegador, **mesmo depois de fechar a aba**:

```js
localStorage.setItem("nome", "Ana");
console.log(localStorage.getItem("nome")); // Ana
localStorage.removeItem("nome");
```

Para guardar arrays e objetos, converta para texto com **JSON**:

```js
const tarefas = [{ texto: "Estudar CSS", feita: true }];
localStorage.setItem("tarefas", JSON.stringify(tarefas));   // array ➔ texto

const salvas = JSON.parse(localStorage.getItem("tarefas")) || [];  // texto ➔ array
```

O `|| []` garante uma lista vazia quando ainda não há nada salvo (`getItem` devolve `null`).

!!! warning "O que não guardar"
    O `localStorage` fica **no computador** de quem usa, e qualquer script da página consegue ler. Não guarde senhas nem dados sensíveis. Ele é ótimo para preferências e listas pessoais.

---

## Exercícios

### Básico (fixação)

Faça um botão “Modo escuro” que alterna a classe `escuro` no `<body>`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```js
    document.querySelector("#modo").addEventListener("click", () => {
      document.body.classList.toggle("escuro");
    });
    ```
    No CSS: `body.escuro { background-color: #121212; color: #eee; }`.

### Intermediário (aplicação)

Mostre, embaixo de um `<textarea>`, quantos caracteres ainda restam de um limite de 140, atualizando a cada tecla.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```js
    const texto = document.querySelector("#mensagem");
    const resta = document.querySelector("#resta");
    texto.addEventListener("input", () => {
      resta.textContent = `${140 - texto.value.length} caracteres restantes`;
    });
    ```
    Acrescente `maxlength="140"` no `<textarea>` para o navegador impedir passar do limite.

### Avançado (desafio)

Faça o modo escuro do exercício básico ser **lembrado**: ao reabrir a página, ela já aparece escura se foi assim que a pessoa deixou.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```js
    if (localStorage.getItem("tema") === "escuro") {
      document.body.classList.add("escuro");
    }
    document.querySelector("#modo").addEventListener("click", () => {
      const escuro = document.body.classList.toggle("escuro");
      localStorage.setItem("tema", escuro ? "escuro" : "claro");
    });
    ```
    `classList.toggle` devolve `true` quando a classe ficou, e isso decide o que salvar.

---

## 💡 Resumo

- `elemento.addEventListener("evento", () => { … })`.
- Formulário: escute o `submit`, chame `preventDefault()` e converta `.value` com `Number()`.
- `localStorage` guarda textos; arrays e objetos com `JSON.stringify` e `JSON.parse`.
- Nada de senhas ou dados sensíveis no `localStorage`.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_lista_de_tarefas.md)** você junta tudo numa lista de tarefas.
