# 04 — Funções tipadas

> **Curso:** TypeScript  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Tipar **parâmetros** e **retorno** de funções.
- Usar parâmetros **opcionais** e com **valor padrão**.
- Usar `void` para funções que não devolvem nada.
- Tipar funções passadas como valor (*callbacks*).

## Pré-requisitos

- [Aula 03](03_arrays_tuplas_e_objetos.md) deste módulo.

---

## Parâmetros e retorno

```ts
function calcularMedia(n1: number, n2: number): number {
  return (n1 + n2) / 2;
}

calcularMedia(8, 9);       // 8.5
// calcularMedia(8);       // erro: 2 argumentos eram esperados, mas 1 foram obtidos
// calcularMedia("8", 9);  // erro: 'string' não pode ser atribuído a 'number'
```

- Os **parâmetros sempre levam tipo**: o TypeScript não tem como adivinhar o que vão receber.
- O **retorno** (`: number` depois dos parênteses) pode ser inferido, mas escrevê-lo documenta a função e pega erros dentro dela, como esquecer um `return`.

A mesma função como arrow function:

```ts
const calcularMedia = (n1: number, n2: number): number => (n1 + n2) / 2;
```

---

## Opcionais, padrão e `void`

```ts
function saudar(nome: string, titulo?: string): string {
  return titulo ? `Olá, ${titulo} ${nome}!` : `Olá, ${nome}!`;
}
saudar("Ana");             // Olá, Ana!
saudar("Souza", "Profa."); // Olá, Profa. Souza!

function aplicarDesconto(preco: number, percentual = 10): number {
  return preco * (1 - percentual / 100);
}
aplicarDesconto(100);      // 90
aplicarDesconto(100, 25);  // 75

function registrar(mensagem: string): void {
  console.log(`[log] ${mensagem}`);
}
```

| Sintaxe | Significa |
|---|---|
| `titulo?: string` | Opcional: dentro da função, o tipo é `string \| undefined` |
| `percentual = 10` | Valor padrão; o tipo (`number`) é inferido do valor |
| `: void` | A função não devolve nada útil |

Os parâmetros opcionais e com padrão vêm **depois** dos obrigatórios.

---

## Funções como valor

Funções que recebem outras funções (como `map` e `filter`) também são tipadas:

```ts
type Operacao = (a: number, b: number) => number;

const somar: Operacao = (a, b) => a + b;
const multiplicar: Operacao = (a, b) => a * b;

function calcular(a: number, b: number, op: Operacao): number {
  return op(a, b);
}

calcular(3, 4, somar);        // 7
calcular(3, 4, multiplicar);  // 12
```

Repare que, em `somar`, não foi preciso escrever o tipo de `a` e `b`: o tipo `Operacao` já diz.

!!! tip "Funções pequenas e com nome claro"
    Com os tipos na assinatura, o VS Code mostra `calcularMedia(n1: number, n2: number): number` quando você começa a digitar. Funções bem tipadas são autoexplicativas.

---

## Exercícios

### Básico (fixação)

Escreva `formatarPreco(valor: number): string` que devolve, por exemplo, `"R$ 18,00"`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```ts
    function formatarPreco(valor: number): string {
      return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
    }
    console.log(formatarPreco(18)); // R$ 18,00
    ```
    O espaço depois de `R$` pode ser um espaço especial (não separável), que aparece igual na tela.

### Intermediário (aplicação)

Escreva `situacao(media: number, frequencia = 100): string` que devolve “Aprovado” (média ≥ 7 e frequência ≥ 75), “Recuperação” (média ≥ 5 e frequência ≥ 75) ou “Reprovado”.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```ts
    function situacao(media: number, frequencia = 100): string {
      if (frequencia < 75) return "Reprovado";
      if (media >= 7) return "Aprovado";
      if (media >= 5) return "Recuperação";
      return "Reprovado";
    }
    situacao(8);       // Aprovado
    situacao(8, 60);   // Reprovado
    situacao(6);       // Recuperação
    ```

### Avançado (desafio)

Escreva `aplicarATodos(lista: number[], f: (n: number) => number): number[]`, uma versão sua do `map`, sem usar `map`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```ts
    function aplicarATodos(lista: number[], f: (n: number) => number): number[] {
      const resultado: number[] = [];
      for (const n of lista) {
        resultado.push(f(n));
      }
      return resultado;
    }
    console.log(aplicarATodos([1, 2, 3], (n) => n * 10)); // [10, 20, 30]
    ```

---

## 💡 Resumo

- Parâmetros **sempre** tipados; retorno tipado documenta e protege.
- `?` = opcional; `= valor` = padrão; ambos depois dos obrigatórios.
- `void` = não devolve nada.
- `type Operacao = (a: number, b: number) => number` tipa funções passadas como valor.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_boletim.md)** você junta tudo num boletim de notas.
