# 01 — Buscar dados com fetch

> **Curso:** Desenvolvimento Web  
> **Módulo:** 04 — Publicar  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que é uma **API** e o formato **JSON**.
- Buscar dados com `fetch`, `async` e `await`.
- Mostrar os dados na página com o DOM.
- Tratar **erros** com `try`/`catch` e mostrar “carregando…”.

## Pré-requisitos

- [Módulo 03](../modulo_03_javascript/index.md) completo.

---

## API e JSON

Uma **API** é um endereço na internet que, em vez de uma página, devolve **dados**, quase sempre em **JSON** (o formato de objetos e arrays da aula 02 do Módulo 03). Um exemplo público e gratuito é a **ViaCEP**: o endereço `https://viacep.com.br/ws/01001000/json/` devolve:

```json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP"
}
```

Abra esse endereço no navegador e veja: são só dados.

---

## `fetch`, `async` e `await`

Buscar algo na internet **demora**. Para o código esperar sem travar a página, usamos uma função `async` e a palavra `await`:

```js
async function buscarCep(cep) {
  const resposta = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
  const dados = await resposta.json();
  return dados;
}

buscarCep("01001000").then((dados) => {
  console.log(`${dados.logradouro}, ${dados.localidade} - ${dados.uf}`);
});
```

1. `fetch(endereço)` faz o pedido; `await` espera a resposta.
2. `resposta.json()` transforma o texto JSON em objeto (também com `await`).
3. Uma função `async` sempre devolve uma **promessa**: quem a chama usa `await` (dentro de outra `async`) ou `.then()`.

---

## Na página, com erros tratados

```html
<form id="form-cep">
  <label for="cep">CEP</label>
  <input type="text" id="cep" inputmode="numeric" maxlength="9" required>
  <button type="submit">Buscar</button>
</form>
<p id="endereco" aria-live="polite"></p>
```

```js
const saida = document.querySelector("#endereco");

document.querySelector("#form-cep").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const cep = document.querySelector("#cep").value.replace(/\D/g, "");

  if (cep.length !== 8) {
    saida.textContent = "Digite um CEP com 8 números.";
    return;
  }

  saida.textContent = "Buscando…";
  try {
    const resposta = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    const dados = await resposta.json();
    if (dados.erro) {
      saida.textContent = "CEP não encontrado.";
      return;
    }
    saida.textContent = `${dados.logradouro}, ${dados.bairro} — ${dados.localidade}/${dados.uf}`;
  } catch (erro) {
    saida.textContent = "Não foi possível buscar agora. Confira a internet e tente de novo.";
    console.error(erro);
  }
});
```

| Parte | Para quê |
|---|---|
| `replace(/\D/g, "")` | Tira tudo o que não é número (aceita `01001-000`) |
| “Buscando…” | Mostra que algo está acontecendo |
| `try`/`catch` | Se a internet cair, mostra um aviso em vez de quebrar |
| `resposta.ok` | `false` quando o servidor respondeu com erro (404, 500) |
| `aria-live="polite"` | O leitor de tela anuncia o resultado quando ele muda |

!!! info "Nem toda API aceita pedidos do navegador"
    Algumas APIs exigem uma **chave** ou bloqueiam pedidos vindos de outros sites (o erro de **CORS** aparece no Console). Para estudar, prefira APIs públicas e abertas, como ViaCEP, IBGE e a de feriados da BrasilAPI. Nunca coloque chaves secretas no JavaScript da página: qualquer visitante consegue ver.

---

## Exercícios

### Básico (fixação)

No Console, busque o CEP `20040020` com a função `buscarCep` e mostre a cidade.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```js
    buscarCep("20040020").then((dados) => console.log(dados.localidade));
    ```
    Deve aparecer **Rio de Janeiro**.

### Intermediário (aplicação)

No formulário da aula, preencha automaticamente campos separados de rua, bairro e cidade.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Crie `<input id="rua">`, `<input id="bairro">` e `<input id="cidade">` (com seus `<label>`) e, no lugar do `saida.textContent` final:
    ```js
    document.querySelector("#rua").value = dados.logradouro;
    document.querySelector("#bairro").value = dados.bairro;
    document.querySelector("#cidade").value = `${dados.localidade}/${dados.uf}`;
    ```

### Avançado (desafio)

Teste o tratamento de erro: com a página aberta, desligue a internet (ou use `F12` ➔ **Rede** ➔ *Offline*) e busque um CEP. O que aparece? E com o CEP `00000000`?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    **Offline:** o `fetch` falha, o `catch` mostra “Não foi possível buscar agora…” e o erro aparece no Console. **CEP 00000000:** a ViaCEP responde normalmente (status 200), mas com `{"erro": "true"}`, e a página mostra “CEP não encontrado.”. A internet funcionou, mas o dado não existe: por isso é importante tratar os dois casos.

---

## 💡 Resumo

- API = endereço que devolve dados em JSON.
- `const r = await fetch(url); const dados = await r.json();` dentro de uma função `async`.
- Mostre “carregando…”, confira `r.ok` e use `try`/`catch`.
- Chave secreta nunca vai no JavaScript da página.

## ➡️ Próximo passo

Na **[aula 02](02_organizar_o_projeto.md)** você organiza os arquivos do projeto.
