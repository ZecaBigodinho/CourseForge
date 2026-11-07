# 05 — Projeto do módulo: calculadora de médias

> **Curso:** Java
> **Módulo:** 01 — Fundamentos
> **Tempo estimado:** 1 h 30 min

---

## Objetivos

Ao final deste projeto, você terá:

- Um programa de terminal que lê as notas de vários alunos e mostra a **média** e a **situação** de cada um.
- A leitura do teclado **à prova de erros**: aceita vírgula ou ponto e recusa notas fora de 0 a 10.
- O código dividido em **métodos** com constantes para as regras.

## Pré-requisitos

- Aulas [01](01_primeiro_programa.md) a [04](04_metodos_e_scanner.md) deste módulo.

---

## O pedido

> *“Quero digitar as quatro notas de cada aluno e ver na hora a média e se passou. No fim, a média da turma.”*

Os alunos são inventados.

---

## O código (`CalculadoraMedias.java`)

```java
import java.util.Scanner;

public class CalculadoraMedias {

    static final int NOTAS_POR_ALUNO = 4;
    static final double MEDIA_APROVACAO = 7.0;
    static final double MEDIA_RECUPERACAO = 5.0;

    static double lerDecimal(Scanner entrada, String pergunta) {
        while (true) {
            System.out.print(pergunta);
            String texto = entrada.nextLine().trim().replace(",", ".");
            try {
                double valor = Double.parseDouble(texto);
                if (valor >= 0 && valor <= 10) {
                    return valor;
                }
                System.out.println("  A nota precisa estar entre 0 e 10.");
            } catch (NumberFormatException e) {
                System.out.println("  Digite um número, como 7,5.");
            }
        }
    }

    static int lerInteiro(Scanner entrada, String pergunta) {
        while (true) {
            System.out.print(pergunta);
            try {
                int valor = Integer.parseInt(entrada.nextLine().trim());
                if (valor > 0) {
                    return valor;
                }
            } catch (NumberFormatException e) {
                // cai no aviso abaixo
            }
            System.out.println("  Digite um número inteiro maior que zero.");
        }
    }

    static String situacao(double media) {
        if (media >= MEDIA_APROVACAO) return "Aprovado";
        if (media >= MEDIA_RECUPERACAO) return "Recuperação";
        return "Reprovado";
    }

    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        System.out.println("=== Calculadora de médias ===");
        int quantidade = lerInteiro(entrada, "Quantos alunos? ");

        double somaDasMedias = 0;
        int aprovados = 0;

        for (int a = 1; a <= quantidade; a++) {
            System.out.print("\nNome do aluno " + a + ": ");
            String nome = entrada.nextLine().trim();

            double soma = 0;
            for (int n = 1; n <= NOTAS_POR_ALUNO; n++) {
                soma += lerDecimal(entrada, "  Nota " + n + ": ");
            }
            double media = soma / NOTAS_POR_ALUNO;
            String resultado = situacao(media);

            System.out.printf("  %s: média %.1f — %s%n", nome, media, resultado);
            somaDasMedias += media;
            if (resultado.equals("Aprovado")) {
                aprovados++;
            }
        }

        System.out.println("\n=== Resumo da turma ===");
        System.out.printf("Média geral: %.1f%n", somaDasMedias / quantidade);
        System.out.println("Aprovados: " + aprovados + " de " + quantidade);
    }
}
```

Rode com:

```bash
java -Dstdout.encoding=UTF-8 CalculadoraMedias.java
```

Um exemplo de uso (o que está depois de cada `?` e `:` foi digitado):

```text
=== Calculadora de médias ===
Quantos alunos? 2

Nome do aluno 1: Ana
  Nota 1: 8
  Nota 2: 9,5
  Nota 3: 7.5
  Nota 4: 9
  Ana: média 8,5 — Aprovado

Nome do aluno 2: Bruno
  Nota 1: 6
  Nota 2: seis
  Digite um número, como 7,5.
  Nota 2: 5,5
  Nota 3: 11
  A nota precisa estar entre 0 e 10.
  Nota 3: 7
  Nota 4: 6
  Bruno: média 6,1 — Recuperação

=== Resumo da turma ===
Média geral: 7,3
Aprovados: 1 de 2
```

| Detalhe | Por quê |
|---|---|
| Constantes `final` no topo | As regras (4 notas, médias 7 e 5) ficam num só lugar |
| `lerDecimal` com `while (true)` | Pergunta de novo até receber uma nota válida; aceita `9,5` e `7.5` |
| `try { … } catch (NumberFormatException e)` | Se o texto não for número, `parseDouble` lança um erro; o `catch` o trata com uma mensagem. Exceções são assunto do Módulo 03: aqui, basta saber que o `catch` “segura” o erro |
| `soma / NOTAS_POR_ALUNO` | `soma` é `double`, então a divisão mantém os decimais |
| `resultado.equals("Aprovado")` | Texto se compara com `equals` (aula 03) |

---

## Entrega

1. O arquivo `CalculadoraMedias.java`.
2. Um print do terminal com pelo menos **3 alunos**, incluindo uma nota digitada errado de propósito.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Compila e roda | Sem erros; `javac` e `java` funcionando |
| Métodos | Leitura, situação e cálculo em métodos com nomes claros |
| Entrada segura | Aceita vírgula e ponto; recusa textos e notas fora de 0 a 10 |
| Resultados | Médias, situações e resumo corretos |

---

## Exercícios extras

### Básico (fixação)

Mude a regra para **6 notas por aluno** e média de aprovação **6,0**. Quantas linhas mudaram?

<!-- gabarito -->
??? success "Gabarito — Básico"
    Só as constantes: `NOTAS_POR_ALUNO = 6` e `MEDIA_APROVACAO = 6.0`. É para isso que elas servem.

### Intermediário (aplicação)

Mostre também a **maior** e a **menor** média da turma, com o nome de cada aluno.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Antes do `for` dos alunos: `double maior = -1, menor = 11; String nomeMaior = "", nomeMenor = "";`. Depois de calcular cada média:
    ```java
    if (media > maior) { maior = media; nomeMaior = nome; }
    if (media < menor) { menor = media; nomeMenor = nome; }
    ```
    No resumo: `System.out.printf("Maior: %s (%.1f) · Menor: %s (%.1f)%n", nomeMaior, maior, nomeMenor, menor);`.

### Avançado (desafio)

Leia também a **frequência** (em %) de cada aluno e reprove quem tiver menos de 75%, mesmo com média alta.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Crie `lerFrequencia` no modelo do `lerDecimal`, mas aceitando de 0 a 100. Mude a assinatura para `situacao(double media, double frequencia)` e comece com `if (frequencia < 75) return "Reprovado por falta";`. No resumo, só conta como aprovado quem passou nas duas regras.

---

## 💡 Resumo

- Constantes no topo; um método para cada tarefa.
- Leitura segura: `nextLine` + `replace(",", ".")` + `parseDouble`, repetindo até dar certo.
- `double` na soma garante a média com decimais.

## ➡️ Próximo passo

Você terminou o **Módulo 01**. Volte ao [índice do módulo](index.md) e confira o checklist. O **Módulo 02 — Orientação a objetos** está em produção.
