# 01 — Formulários controlados

> **Curso:** React  
> **Módulo:** 02 — Listas, formulários e efeitos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar campos **controlados** (`value` + `onChange`).
- Tratar o envio com `onSubmit` e `preventDefault`.
- Controlar vários campos com um único objeto no estado.
- Usar `select`, `checkbox` e validar antes de enviar.

## Pré-requisitos

- [Módulo 01](../modulo_01_fundamentos/index.md) completo.

---

## Campo controlado

No curso de Web, você lia o campo na hora do envio (`campo.value`). No React, o valor fica **no estado** o tempo todo:

```tsx
import { useState } from "react";

export default function Busca() {
  const [termo, setTermo] = useState("");

  return (
    <>
      <label htmlFor="busca">Buscar</label>
      <input id="busca" value={termo} onChange={(e) => setTermo(e.target.value)} />
      <p>Você digitou: {termo}</p>
    </>
  );
}
```

- `value={termo}`: o campo mostra o que está no estado.
- `onChange`: a cada tecla, o estado recebe o novo texto, e o React redesenha.

Assim o valor está sempre disponível para mostrar, filtrar ou validar, sem `querySelector`.

!!! warning "Campo que não deixa digitar"
    Se você puser `value={termo}` e esquecer o `onChange`, o campo fica **travado**: o React sempre volta a mostrar o valor do estado. O Console avisa.

---

## Enviar o formulário

```tsx
import { useState } from "react";
import type { FormEvent } from "react";

export default function Inscricao() {
  const [nome, setNome] = useState("");
  const [enviado, setEnviado] = useState(false);

  function enviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();          // não recarrega a página
    if (nome.trim() === "") return;
    setEnviado(true);
  }

  if (enviado) return <p>Inscrição recebida, {nome}!</p>;

  return (
    <form onSubmit={enviar}>
      <label htmlFor="nome">Nome</label>
      <input id="nome" value={nome} onChange={(e) => setNome(e.target.value)} required />
      <button type="submit" disabled={nome.trim() === ""}>Inscrever</button>
    </form>
  );
}
```

Como no curso de Web, escute o **`onSubmit` do formulário**, e não o clique do botão: assim o `Enter` também funciona e o `required` do HTML continua valendo.

---

## Vários campos num objeto

```tsx
type Dados = { nome: string; turno: "manha" | "tarde"; novidades: boolean };

const [dados, setDados] = useState<Dados>({ nome: "", turno: "manha", novidades: false });

<input
  value={dados.nome}
  onChange={(e) => setDados((d) => ({ ...d, nome: e.target.value }))}
/>

<select
  value={dados.turno}
  onChange={(e) => setDados((d) => ({ ...d, turno: e.target.value as Dados["turno"] }))}
>
  <option value="manha">Manhã</option>
  <option value="tarde">Tarde</option>
</select>

<input
  type="checkbox"
  checked={dados.novidades}
  onChange={(e) => setDados((d) => ({ ...d, novidades: e.target.checked }))}
/>
```

- Cada campo copia o objeto (`...d`) e troca só a sua propriedade.
- Checkbox usa **`checked`** e `e.target.checked`, e não `value`.
- O `as Dados["turno"]` avisa ao TypeScript que o valor do `<select>` é uma das opções (o navegador entrega sempre `string`). É seguro aqui porque as opções do `<select>` são exatamente essas.

---

## Exercícios

### Básico (fixação)

Faça um campo de nome e um parágrafo que mostra “Olá, (nome)!”, ou “Olá, visitante!” com o campo vazio.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```tsx
    const [nome, setNome] = useState("");
    <input value={nome} onChange={(e) => setNome(e.target.value)} />
    <p>Olá, {nome.trim() || "visitante"}!</p>
    ```

### Intermediário (aplicação)

Faça um formulário de contato (nome, e-mail, mensagem) com um único objeto no estado e o botão **Enviar** desabilitado enquanto algum campo estiver vazio.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```tsx
    type Contato = { nome: string; email: string; mensagem: string };
    const [c, setC] = useState<Contato>({ nome: "", email: "", mensagem: "" });
    const incompleto = Object.values(c).some((v) => v.trim() === "");
    // cada campo: value={c.nome} onChange={(e) => setC((d) => ({ ...d, nome: e.target.value }))}
    <button type="submit" disabled={incompleto}>Enviar</button>
    ```
    `incompleto` é **calculado** a partir do estado, sem outro `useState`.

### Avançado (desafio)

Mostre embaixo do campo de e-mail um aviso em vermelho “E-mail inválido” só **depois** que a pessoa sair do campo (evento `onBlur`) e se o texto não tiver `@`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```tsx
    const [email, setEmail] = useState("");
    const [tocado, setTocado] = useState(false);
    const invalido = tocado && !email.includes("@");
    <input
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      onBlur={() => setTocado(true)}
      aria-invalid={invalido}
      aria-describedby="erro-email"
    />
    {invalido && <p id="erro-email" style={{ color: "#c62828" }}>E-mail inválido</p>}
    ```
    Mostrar o erro só depois do `onBlur` evita “brigar” com quem ainda está digitando. O `aria-invalid` avisa o leitor de tela.

---

## 💡 Resumo

- Campo controlado: `value` do estado + `onChange` que atualiza o estado.
- `onSubmit` no formulário, com `preventDefault()`.
- Vários campos: um objeto no estado, copiando com `...` e trocando uma propriedade.
- Checkbox: `checked` e `e.target.checked`.

## ➡️ Próximo passo

Na **[aula 02](02_listas.md)** você filtra, edita e remove itens de listas.
