# 03 — Arrays, tuplas e objetos

> **Curso:** TypeScript  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Tipar **arrays** (`number[]`) e entender o que os métodos devolvem.
- Usar **tuplas** para pares de valores com posição fixa.
- Descrever o formato de **objetos**, com propriedades opcionais e somente leitura.
- Dar nome a um formato com `type`.

## Pré-requisitos

- [Aula 02](02_tipos_basicos.md) deste módulo.

---

## Arrays

```ts
const notas: number[] = [8, 6.5, 9];
const nomes = ["Ana", "Bruno"];   // inferido: string[]

notas.push(7);        // ok
// notas.push("dez"); // erro: 'string' não pode ser atribuído a 'number'

const dobradas = notas.map((n) => n * 2);   // number[]
const altas = notas.filter((n) => n >= 8);  // number[]
```

O TypeScript sabe o tipo de cada item, então dentro do `map` o `n` já é `number`, sem você escrever.

!!! info "`find` pode não achar"
    `notas.find((n) => n > 10)` tem o tipo `number | undefined`: se nada passar no teste, o resultado é `undefined`. Com `strict`, o TypeScript obriga você a tratar esse caso antes de usar o valor.

---

## Tuplas

Uma **tupla** é um array com **tamanho e tipos fixos por posição**:

```ts
const ponto: [number, number] = [10, 20];
const aluno: [string, number] = ["Ana", 8.5];

const [nome, nota] = aluno;   // nome: string, nota: number
```

Use tuplas para pares curtos e óbvios (coordenadas, chave e valor). Quando houver mais de dois ou três valores, prefira um objeto com nomes.

---

## Objetos

O tipo de um objeto descreve o **nome** e o **tipo** de cada propriedade:

```ts
const lanche: { nome: string; preco: number } = {
  nome: "X-Salada",
  preco: 18,
};
```

Escrever esse formato toda vez cansa. Dê um nome a ele com **`type`**:

```ts
type Lanche = {
  nome: string;
  preco: number;
  vegetariano?: boolean;      // ? = opcional
  readonly codigo: number;    // não pode ser alterado depois
};

const xSalada: Lanche = { codigo: 1, nome: "X-Salada", preco: 18 };
xSalada.preco = 19;       // ok
// xSalada.codigo = 2;    // erro: somente leitura
```

Arrays de objetos ficam assim:

```ts
const cardapio: Lanche[] = [
  { codigo: 1, nome: "X-Salada", preco: 18 },
  { codigo: 2, nome: "X-Bacon", preco: 22 },
  { codigo: 3, nome: "Salada verde", preco: 15, vegetariano: true },
];

const total = cardapio.reduce((soma, item) => soma + item.preco, 0); // 55
```

!!! tip "O autocompletar agora sabe tudo"
    Digite `cardapio[0].` no VS Code: aparecem `codigo`, `nome`, `preco` e `vegetariano`. Errar o nome de uma propriedade vira erro na hora.

---

## Exercícios

### Básico (fixação)

Declare um array de notas, acrescente uma nota e calcule a média com `reduce`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    const notas: number[] = [7, 8.5, 6];
    notas.push(9.5);
    const media = notas.reduce((s, n) => s + n, 0) / notas.length;
    console.log(media.toFixed(1)); // 7.8
    ```

### Intermediário (aplicação)

Crie o `type Aluno` com `nome`, `turma` e `notas` (array de números) e um array com dois alunos. Mostre o nome e a média de cada um.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    type Aluno = { nome: string; turma: string; notas: number[] };
    const alunos: Aluno[] = [
      { nome: "Ana", turma: "1A", notas: [8, 9] },
      { nome: "Bruno", turma: "1A", notas: [6, 7] },
    ];
    for (const a of alunos) {
      const media = a.notas.reduce((s, n) => s + n, 0) / a.notas.length;
      console.log(`${a.nome}: ${media}`); // Ana: 8.5 / Bruno: 6.5
    }
    ```

### Avançado (desafio)

No `cardapio` da aula, procure o lanche de código 4 e mostre o nome dele. O que o TypeScript exige e por quê?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    const achado = cardapio.find((item) => item.codigo === 4);
    if (achado) {
      console.log(achado.nome);
    } else {
      console.log("Lanche não encontrado.");
    }
    ```
    `find` devolve `Lanche | undefined`. Sem o `if`, `achado.nome` dá o erro TS18048: “'achado' is possibly 'undefined'.” (com `--locale pt-br`: “'achado' é possivelmente 'indefinido'.”). O TypeScript obriga a tratar o caso em que nada foi encontrado, o mesmo erro que em JavaScript só apareceria rodando.

---

## 💡 Resumo

- Arrays: `number[]`, `string[]`, `Lanche[]`; os métodos mantêm o tipo.
- `find` devolve `Tipo | undefined`: trate o caso de não achar.
- Tuplas: `[string, number]`, posição e tipo fixos.
- Objetos: `type Nome = { … }`, com `?` (opcional) e `readonly`.

## ➡️ Próximo passo

Na **[aula 04](04_funcoes_tipadas.md)** você tipa funções.
