# 05 — Projeto do módulo: boletim de notas

> **Curso:** TypeScript  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final deste projeto, você terá:

- Um programa de terminal em TypeScript que calcula a **média** e a **situação** de cada aluno.
- Os dados num array de objetos com `type`.
- Funções pequenas e tipadas, compilando sem erros no modo `strict`.

## Pré-requisitos

- Aulas [01](01_primeiro_programa.md) a [04](04_funcoes_tipadas.md) deste módulo.

---

## O pedido

> *“Quero um programa que mostre o boletim da turma: média de cada aluno, situação e a média geral.”*

Os alunos e as notas são inventados.

---

## O código (`src/boletim.ts`)

```ts
type Aluno = {
  nome: string;
  notas: number[];
  frequencia: number; // em %
};

type Situacao = "Aprovado" | "Recuperação" | "Reprovado";

const turma: Aluno[] = [
  { nome: "Ana", notas: [8, 9, 7.5, 9], frequencia: 95 },
  { nome: "Bruno", notas: [6, 5.5, 7, 6], frequencia: 88 },
  { nome: "Carla", notas: [4, 5, 3.5, 6], frequencia: 90 },
  { nome: "Diego", notas: [9, 8, 9.5, 10], frequencia: 70 },
];

function media(notas: number[]): number {
  if (notas.length === 0) return 0;
  const soma = notas.reduce((s, n) => s + n, 0);
  return soma / notas.length;
}

function situacao(aluno: Aluno): Situacao {
  if (aluno.frequencia < 75) return "Reprovado";
  const m = media(aluno.notas);
  if (m >= 7) return "Aprovado";
  if (m >= 5) return "Recuperação";
  return "Reprovado";
}

function linhaDoBoletim(aluno: Aluno): string {
  const m = media(aluno.notas).toFixed(1).padStart(4);
  return `${aluno.nome.padEnd(8)} média ${m}  freq. ${String(aluno.frequencia).padStart(3)}%  ${situacao(aluno)}`;
}

console.log("BOLETIM — 1º A");
for (const aluno of turma) {
  console.log(linhaDoBoletim(aluno));
}

const mediaGeral = media(turma.map((a) => media(a.notas)));
const aprovados = turma.filter((a) => situacao(a) === "Aprovado").length;
console.log(`\nMédia geral: ${mediaGeral.toFixed(1)} · Aprovados: ${aprovados} de ${turma.length}`);
```

Compile e rode:

```bash
npx tsc
node dist/boletim.js
```

Saída:

```text
BOLETIM — 1º A
Ana      média  8.4  freq.  95%  Aprovado
Bruno    média  6.1  freq.  88%  Recuperação
Carla    média  4.6  freq.  90%  Reprovado
Diego    média  9.1  freq.  70%  Reprovado

Média geral: 7.1 · Aprovados: 1 de 4
```

| Detalhe | Por quê |
|---|---|
| `type Situacao = "Aprovado" \| "Recuperação" \| "Reprovado"` | Só esses três textos são aceitos: um erro de digitação como `"Aprovada"` vira erro de compilação (Módulo 02) |
| `if (notas.length === 0) return 0;` | Evita dividir por zero |
| `padEnd` / `padStart` | Completam com espaços para alinhar as colunas |
| Diego reprovado com média 9,1 | A frequência abaixo de 75% reprova, conforme a regra |

---

## Entrega

1. O arquivo `src/boletim.ts` com a **sua** turma inventada (pelo menos 5 alunos).
2. Um print do terminal com `npx tsc` **sem erros** e a saída do `node`.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Compila | `npx tsc` sem nenhum erro, com `strict: true` |
| Tipos | `type` para o aluno; funções com parâmetros e retorno tipados; nenhum `any` |
| Regras | Média, frequência e situação corretas |
| Organização | Funções pequenas com nomes claros |

---

## Exercícios extras

### Básico (fixação)

Acrescente uma aluna com notas e frequência que a deixem em **Recuperação** e confira a saída.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Por exemplo `{ nome: "Elisa", notas: [6, 6, 6, 6], frequencia: 80 }`: média 6,0 e frequência acima de 75% ➔ Recuperação. A média geral e a contagem mudam automaticamente.

### Intermediário (aplicação)

Mostre também o **melhor aluno** (maior média), tratando o caso de turma vazia.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    function melhorAluno(alunos: Aluno[]): Aluno | undefined {
      let melhor: Aluno | undefined;
      for (const a of alunos) {
        if (!melhor || media(a.notas) > media(melhor.notas)) melhor = a;
      }
      return melhor;
    }
    const destaque = melhorAluno(turma);
    console.log(destaque ? `Destaque: ${destaque.nome}` : "Turma vazia.");
    ```

### Avançado (desafio)

Escreva por engano `return "Aprovada";` dentro de `situacao`. O que o compilador diz, e por que isso não aconteceria se o retorno fosse só `string`?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    O `tsc` acusa o erro TS2820: “Type '"Aprovada"' is not assignable to type 'Situacao'. Did you mean '"Aprovado"'?”. Ele até sugere a palavra certa. Com retorno `string`, qualquer texto seria aceito, e o filtro `situacao(a) === "Aprovado"` deixaria de contar essa aluna sem nenhum aviso. Tipos literais transformam erros de digitação em erros de compilação.

---

## 💡 Resumo

- Dados com `type`; regras em funções pequenas e tipadas.
- Tipos literais (`"Aprovado" | …`) limitam os valores possíveis.
- Trate os casos-limite: lista vazia, frequência baixa.
- `npx tsc` sem erros antes de rodar.

## ➡️ Próximo passo

Você terminou o **Módulo 01**. Volte ao [índice do módulo](index.md) e confira o checklist. Depois, siga para o **[Módulo 02 — Modelando dados](../modulo_02_modelando_dados/index.md)**.
