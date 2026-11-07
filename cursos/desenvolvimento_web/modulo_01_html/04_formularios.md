# 04 — Formulários

> **Curso:** Desenvolvimento Web  
> **Módulo:** 01 — HTML  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Montar um **formulário** com campos de texto, e-mail, número, data e mensagem.
- Ligar cada campo ao seu **rótulo** (`<label>`).
- Usar caixas de seleção, botões de opção e listas.
- Pedir ao navegador para **validar** os campos (`required`, `type="email"`, `min`/`max`).

## Pré-requisitos

- [Aula 03](03_listas_e_tabelas.md) deste módulo.

---

## A estrutura de um formulário

```html
<form action="#" method="post">
  <label for="nome">Nome</label>
  <input type="text" id="nome" name="nome" required>

  <label for="email">E-mail</label>
  <input type="email" id="email" name="email" placeholder="voce@exemplo.com" required>

  <label for="mensagem">Mensagem</label>
  <textarea id="mensagem" name="mensagem" rows="4"></textarea>

  <button type="submit">Enviar</button>
</form>
```

| Parte | Para quê |
|---|---|
| `<form action method>` | Junta os campos. `action` diz **para onde** os dados vão; `method` diz **como** (`get` ou `post`) |
| `<label for="...">` | O **rótulo**: o `for` tem de ser igual ao `id` do campo |
| `<input>` | Campo de uma linha; o `type` muda o tipo |
| `name` | O nome com que o dado é enviado |
| `<textarea>` | Texto de várias linhas |
| `<button type="submit">` | Envia o formulário |

!!! info "Para onde vão os dados?"
    HTML sozinho só **monta** o formulário. Quem recebe e guarda os dados é um programa no servidor (em Python, por exemplo) ou um serviço de formulários. Por enquanto, use `action="#"`: o formulário funciona e valida, mas não envia para lugar nenhum. No Módulo 03, o JavaScript vai ler os campos.

!!! tip "Por que o `<label>` é obrigatório"
    Com o `for` ligado ao `id`, **clicar no rótulo coloca o cursor no campo** (ótimo no celular), e o leitor de tela anuncia “Nome, campo de texto”. Um `placeholder` **não substitui** o rótulo: ele some quando a pessoa começa a digitar.

---

## Tipos de campo

| `type` | Campo | Vantagem |
|---|---|---|
| `text` | Texto comum | — |
| `email` | E-mail | Confere se tem `@`; no celular, abre o teclado com `@` |
| `tel` | Telefone | Teclado numérico no celular |
| `number` | Número | Setinhas; aceita `min`, `max` e `step` |
| `date` | Data | Abre um calendário |
| `password` | Senha | Esconde o que é digitado |
| `checkbox` | Caixa de seleção | Marcar várias opções |
| `radio` | Botão de opção | Escolher **uma** entre várias |

### Opções

```html
<fieldset>
  <legend>Turno</legend>
  <input type="radio" id="manha" name="turno" value="manha" checked>
  <label for="manha">Manhã</label>
  <input type="radio" id="tarde" name="turno" value="tarde">
  <label for="tarde">Tarde</label>
</fieldset>

<input type="checkbox" id="novidades" name="novidades">
<label for="novidades">Quero receber novidades por e-mail</label>

<label for="curso">Curso</label>
<select id="curso" name="curso">
  <option value="">Escolha…</option>
  <option value="web">Desenvolvimento Web</option>
  <option value="python">Python</option>
</select>
```

- Botões `radio` do mesmo grupo têm o **mesmo `name`**: assim só um fica marcado.
- `<fieldset>` com `<legend>` agrupa as opções sob um título.
- `checked` deixa uma opção marcada de início.

---

## Validação do navegador

| Atributo | Efeito |
|---|---|
| `required` | Não deixa enviar vazio |
| `type="email"` | Exige um e-mail com formato válido |
| `min` / `max` | Limites para números e datas |
| `minlength` / `maxlength` | Tamanho mínimo e máximo do texto |

Ao clicar em **Enviar** com algo errado, o navegador mostra um aviso e não envia.

!!! warning "Validação no navegador não basta"
    Ela ajuda quem preenche, mas qualquer pessoa pode desligá-la. Quando houver um servidor recebendo os dados, ele **também** precisa conferir tudo.

---

## Exercícios

### Básico (fixação)

Faça um formulário de **inscrição** com nome, e-mail e data de nascimento, todos obrigatórios.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```html
    <form action="#">
      <label for="nome">Nome</label>
      <input type="text" id="nome" name="nome" required>
      <label for="email">E-mail</label>
      <input type="email" id="email" name="email" required>
      <label for="nascimento">Data de nascimento</label>
      <input type="date" id="nascimento" name="nascimento" required>
      <button type="submit">Inscrever</button>
    </form>
    ```
    Teste: clique em **Inscrever** com um campo vazio e veja o aviso do navegador.

### Intermediário (aplicação)

Acrescente a escolha do **turno** (manhã, tarde ou noite, só uma) e uma caixa “Li e aceito o regulamento” obrigatória.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Três `<input type="radio">` com o **mesmo** `name="turno"` dentro de `<fieldset><legend>Turno</legend>…</fieldset>`, cada um com seu `<label>`. A caixa: `<input type="checkbox" id="regulamento" name="regulamento" required> <label for="regulamento">Li e aceito o regulamento</label>`. Sem marcar, o formulário não envia.

### Avançado (desafio)

Crie um campo **Quantidade de ingressos** que aceite só de 1 a 4, e um campo **Telefone** que abra o teclado numérico no celular. Explique por que o servidor também precisaria conferir a quantidade.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```html
    <label for="qtd">Quantidade de ingressos</label>
    <input type="number" id="qtd" name="qtd" min="1" max="4" value="1" required>
    <label for="tel">Telefone</label>
    <input type="tel" id="tel" name="tel" placeholder="(11) 90000-0000">
    ```
    O navegador impede 5 ingressos, mas alguém pode abrir o `F12`, apagar o `max` e enviar 50. Por isso o servidor tem de recusar valores fora de 1 a 4.

---

## 💡 Resumo

- `<form>` junta os campos; cada campo tem `id`, `name` e um `<label for>`.
- O `type` do `<input>` muda o campo e o teclado do celular.
- `radio` com o mesmo `name` = uma escolha; `checkbox` = várias; `<select>` = lista.
- `required`, `min`, `max`: validação do navegador, que ajuda mas não substitui a do servidor.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_pagina_de_apresentacao.md)** você junta tudo na sua página de apresentação.
