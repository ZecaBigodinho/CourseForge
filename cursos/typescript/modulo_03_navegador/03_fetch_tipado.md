# 03 — fetch com tipos

> **Curso:** TypeScript  
> **Módulo:** 03 — TypeScript no navegador  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Tipar funções `async` com `Promise<T>`.
- Entender por que o resultado de `response.json()` deve ser tratado como `unknown`.
- Escrever **guardas de tipo** (`valor is Tipo`) para validar dados de fora.
- Combinar `fetch`, validação e o tipo `Resposta<T>` do Módulo 02.

## Pré-requisitos

- [Aula 02](02_dom_tipado.md) deste módulo e a [aula de fetch do curso de Web](../../desenvolvimento_web/modulo_04_publicar/01_fetch_e_apis.md).

---

## `async` e `Promise<T>`

Uma função `async` sempre devolve uma **promessa**. O tipo do retorno diz o que a promessa vai entregar:

```ts
async function esperar(ms: number): Promise<string> {
  await new Promise((resolver) => setTimeout(resolver, ms));
  return `Esperei ${ms} ms`;
}
```

---

## Os dados de fora são `unknown`

```ts
const resposta = await fetch("https://viacep.com.br/ws/01001000/json/");
const dados = await resposta.json();   // tipo: any
```

O `json()` devolve `any`: o TypeScript **não tem como saber** o que o servidor mandou. Uma API pode mudar, cair ou devolver um erro. Se você escrever `const dados: Endereco = await resposta.json()`, está só **prometendo** ao compilador, sem conferir.

O jeito seguro: tratar como `unknown` e **validar**.

### Guarda de tipo

```ts
type Endereco = {
  cep: string;
  logradouro: string;
  bairro: string;
  localidade: string;
  uf: string;
};

function ehEndereco(valor: unknown): valor is Endereco {
  if (typeof valor !== "object" || valor === null) return false;
  const v = valor as Record<string, unknown>;
  return (
    typeof v.cep === "string" &&
    typeof v.logradouro === "string" &&
    typeof v.bairro === "string" &&
    typeof v.localidade === "string" &&
    typeof v.uf === "string"
  );
}
```

O retorno `valor is Endereco` diz ao TypeScript: “se esta função devolver `true`, trate `valor` como `Endereco`”. Depois de um `if (ehEndereco(x))`, o tipo é estreitado, como com `typeof` no Módulo 02.

---

## Juntando tudo

```ts
type Resposta<T> = { ok: true; dados: T } | { ok: false; erro: string };

async function buscarCep(cep: string): Promise<Resposta<Endereco>> {
  try {
    const r = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    if (!r.ok) return { ok: false, erro: `Erro HTTP ${r.status}` };
    const dados: unknown = await r.json();
    if (!ehEndereco(dados)) return { ok: false, erro: "CEP não encontrado" };
    return { ok: true, dados };
  } catch {
    return { ok: false, erro: "Sem conexão" };
  }
}

const resultado = await buscarCep("01001000");
if (resultado.ok) {
  console.log(`${resultado.dados.logradouro} — ${resultado.dados.localidade}/${resultado.dados.uf}`);
} else {
  console.log(resultado.erro);
}
```

Quem chama `buscarCep` é **obrigado** a conferir `ok` antes de usar `dados`. Erro de rede, CEP inexistente (a ViaCEP devolve `{"erro": "true"}`, que não passa na guarda) e mudança na API caem todos no caminho do erro, com mensagem.

!!! info "`await` fora de função"
    O `await resultado…` solto no arquivo funciona em **módulos** (`type="module"`) com `"target": "es2017"` ou mais novo e `"module": "es2022"` ou `"esnext"`. Com `"module": "es2020"`, coloque o código dentro de uma função `async`.

!!! tip "Bibliotecas de validação"
    Em projetos grandes, escrever guardas à mão cansa. Bibliotecas como o **Zod** geram a validação e o tipo juntos. Para aprender, escrever a guarda à mão mostra o que está acontecendo.

---

## Exercícios

### Básico (fixação)

Escreva `async function dobroDepois(n: number): Promise<number>` que espera 500 ms e devolve o dobro.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    async function dobroDepois(n: number): Promise<number> {
      await new Promise((r) => setTimeout(r, 500));
      return n * 2;
    }
    dobroDepois(21).then((v) => console.log(v)); // 42, depois de meio segundo
    ```

### Intermediário (aplicação)

Escreva a guarda `ehFeriado(valor: unknown): valor is Feriado` para os itens da BrasilAPI (`{ date: string; name: string; type: string }`).

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    type Feriado = { date: string; name: string; type: string };
    function ehFeriado(valor: unknown): valor is Feriado {
      if (typeof valor !== "object" || valor === null) return false;
      const v = valor as Record<string, unknown>;
      return typeof v.date === "string" && typeof v.name === "string" && typeof v.type === "string";
    }
    ```

### Avançado (desafio)

Escreva `buscarFeriados(ano: number): Promise<Feriado[]>` que devolve só os itens válidos da lista (ou `[]` se algo falhar).

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    async function buscarFeriados(ano: number): Promise<Feriado[]> {
      try {
        const r = await fetch(`https://brasilapi.com.br/api/feriados/v1/${ano}`);
        if (!r.ok) return [];
        const dados: unknown = await r.json();
        return Array.isArray(dados) ? dados.filter(ehFeriado) : [];
      } catch {
        return [];
      }
    }
    ```
    `dados.filter(ehFeriado)` usa a guarda como filtro: o resultado já sai com o tipo `Feriado[]`.

---

## 💡 Resumo

- `async function f(): Promise<T>` diz o que a promessa entrega.
- `response.json()` não garante nada: trate como `unknown`.
- Guardas `valor is Tipo` validam e estreitam o tipo.
- `fetch` + guarda + `Resposta<T>` = erros sempre tratados.

## ➡️ Próximo passo

Na **[aula 04](04_projeto_lista_de_tarefas.md)** você reescreve a lista de tarefas em TypeScript.
