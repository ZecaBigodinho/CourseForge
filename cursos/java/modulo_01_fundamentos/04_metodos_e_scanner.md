# 04 — Métodos e entrada com Scanner

> **Curso:** Java  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar **métodos** com parâmetros e retorno.
- Usar `void` para métodos que não devolvem nada.
- Ler textos e números do teclado com **`Scanner`**.
- Evitar as duas armadilhas do `Scanner`: a **vírgula decimal** e o **`nextLine` pulado**.

## Pré-requisitos

- [Aula 03](03_condicoes_e_lacos.md) deste módulo.

---

## Métodos

Um **método** é um bloco de código com nome, que recebe valores (**parâmetros**) e pode devolver um resultado:

```java
public class Notas {

    static double media(double n1, double n2) {
        return (n1 + n2) / 2;
    }

    static String situacao(double media) {
        if (media >= 7) return "Aprovado";
        if (media >= 5) return "Recuperação";
        return "Reprovado";
    }

    static void linha() {
        System.out.println("----------------");
    }

    public static void main(String[] args) {
        double m = media(8, 6.5);
        linha();
        System.out.printf("Média %.2f: %s%n", m, situacao(m));
        linha();
    }
}
```

| Parte | Significa |
|---|---|
| `static` | O método pertence à classe e pode ser chamado direto do `main` (o Módulo 02 explica) |
| `double` antes do nome | O **tipo do retorno** |
| `(double n1, double n2)` | Os parâmetros, cada um com seu tipo |
| `return` | Devolve o valor e encerra o método |
| `void` | O método não devolve nada |

---

## Ler o teclado com `Scanner`

```java
import java.util.Scanner;

public class Saudacao {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);

        System.out.print("Seu nome: ");
        String nome = entrada.nextLine();

        System.out.print("Sua idade: ");
        int idade = entrada.nextInt();

        System.out.println("Olá, " + nome + "! Daqui a 10 anos você terá " + (idade + 10) + ".");
    }
}
```

- `import java.util.Scanner;` fica no começo do arquivo, antes da classe.
- `nextLine()` lê a linha inteira (texto); `nextInt()` lê um inteiro; `nextDouble()`, um decimal.

### Armadilha 1: vírgula ou ponto?

O `Scanner` segue o **idioma do computador**. Num Windows em português, `nextDouble()` espera **`7,5`**; se a pessoa digitar `7.5`, o programa quebra com `InputMismatchException`. Em computadores em inglês, é o contrário.

A solução mais segura é ler como **texto** e converter, aceitando os dois:

```java
static double lerDecimal(Scanner entrada) {
    String texto = entrada.nextLine().trim().replace(",", ".");
    return Double.parseDouble(texto);
}
```

`Double.parseDouble` sempre usa **ponto**; o `replace` troca a vírgula, se houver.

### Armadilha 2: o `nextLine` que “pula”

```java
int idade = entrada.nextInt();      // lê "17" e deixa o Enter na fila
String cidade = entrada.nextLine(); // lê o Enter que sobrou: cidade fica vazia!
```

`nextInt` e `nextDouble` não consomem o **Enter**. O `nextLine` seguinte lê esse Enter e devolve um texto vazio. Duas soluções: chamar um `entrada.nextLine();` extra depois do `nextInt`, ou, mais simples, **ler sempre com `nextLine`** e converter (`Integer.parseInt(entrada.nextLine().trim())`), como no `lerDecimal`.

!!! tip "Regra deste curso"
    Leia **tudo** com `nextLine()` e converta com `Integer.parseInt` ou com o `lerDecimal`. Assim as duas armadilhas desaparecem.

---

## Exercícios

### Básico (fixação)

Escreva o método `static double areaRetangulo(double base, double altura)` e mostre a área de um retângulo 5 × 3.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    static double areaRetangulo(double base, double altura) {
        return base * altura;
    }
    // no main:
    System.out.println(areaRetangulo(5, 3)); // 15.0
    ```

### Intermediário (aplicação)

Leia o preço de um produto (aceitando vírgula ou ponto) e mostre o valor com 10% de desconto.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    Scanner entrada = new Scanner(System.in);
    System.out.print("Preço: ");
    double preco = lerDecimal(entrada);
    System.out.printf("Com desconto: R$ %.2f%n", preco * 0.9);
    ```
    Digitando `50,00` ou `50.00`, a saída é `R$ 45,00` (num Windows em português).

### Avançado (desafio)

Faça um menu que se repete até a pessoa escolher **3 — Sair**: **1** mostra a tabuada de um número lido; **2** diz se um número lido é par ou ímpar.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    Scanner entrada = new Scanner(System.in);
    int opcao;
    do {
        System.out.println("1 - Tabuada | 2 - Par ou ímpar | 3 - Sair");
        opcao = Integer.parseInt(entrada.nextLine().trim());
        switch (opcao) {
            case 1 -> {
                System.out.print("Número: ");
                int n = Integer.parseInt(entrada.nextLine().trim());
                for (int i = 1; i <= 10; i++) System.out.println(n + " x " + i + " = " + n * i);
            }
            case 2 -> {
                System.out.print("Número: ");
                int n = Integer.parseInt(entrada.nextLine().trim());
                System.out.println(n % 2 == 0 ? "par" : "ímpar");
            }
            case 3 -> System.out.println("Até logo!");
            default -> System.out.println("Opção inválida");
        }
    } while (opcao != 3);
    ```
    Lendo tudo com `nextLine`, o menu nunca “pula” uma pergunta.

---

## 💡 Resumo

- Métodos: tipo de retorno, nome, parâmetros com tipo; `return` devolve; `void` não devolve.
- `Scanner entrada = new Scanner(System.in);` com `import java.util.Scanner;`.
- `nextDouble` segue o idioma (vírgula no Brasil): prefira ler texto e converter.
- `nextInt` deixa o Enter na fila: leia tudo com `nextLine()`.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_calculadora.md)** você monta a calculadora de médias.
