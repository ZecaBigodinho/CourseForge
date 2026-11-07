# 03 — Exceções

> **Curso:** Java  
> **Módulo:** 03 — Coleções, exceções e arquivos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Entender o que é uma **exceção** e ler o *stack trace*.
- Capturar exceções com `try`, `catch` e `finally`.
- Diferenciar exceções **verificadas** (`IOException`) das **não verificadas** (`IllegalArgumentException`).
- Criar uma **exceção própria** e decidir entre tratar ou repassar com `throws`.

## Pré-requisitos

- [Aula 02](02_streams.md) deste módulo.

---

## O que é uma exceção

Uma **exceção** é um objeto que representa um erro durante a execução. Se ninguém a trata, o programa para e mostra o *stack trace*:

```text
Exception in thread "main" java.lang.NumberFormatException: For input string: "sete"
	at java.base/java.lang.Integer.parseInt(Integer.java:...)
	at Teste.main(Teste.java:5)
```

Leia de cima para baixo: o **tipo** (`NumberFormatException`), a **mensagem** (`For input string: "sete"`) e, nas linhas `at`, o caminho até o erro. Procure a primeira linha com um arquivo **seu** (`Teste.java:5`).

---

## `try`, `catch`, `finally`

```java
import java.util.Scanner;

public class Divisao {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        try {
            System.out.print("Dividendo: ");
            int a = Integer.parseInt(entrada.nextLine().trim());
            System.out.print("Divisor: ");
            int b = Integer.parseInt(entrada.nextLine().trim());
            System.out.println("Resultado: " + (a / b));
        } catch (NumberFormatException e) {
            System.out.println("Digite só números inteiros.");
        } catch (ArithmeticException e) {
            System.out.println("Não dá para dividir por zero.");
        } finally {
            System.out.println("Fim do cálculo.");
        }
    }
}
```

- O código “arriscado” vai no `try`. Se uma linha lançar uma exceção, o resto do `try` é **pulado** e o `catch` do tipo certo roda.
- Vários `catch`: o primeiro que combinar com o tipo é usado. Também dá para juntar: `catch (NumberFormatException | ArithmeticException e)`.
- `finally` roda **sempre**, com erro ou sem. Serve para liberar recursos.
- `e.getMessage()` traz a mensagem do erro.

!!! warning "Nunca engula exceções"
    Um `catch (Exception e) { }` vazio esconde o erro: o programa continua errado e ninguém fica sabendo. No mínimo, mostre uma mensagem ou registre o erro.

---

## Verificadas × não verificadas

| | Não verificadas (`RuntimeException`) | Verificadas |
|---|---|---|
| Exemplos | `IllegalArgumentException`, `NumberFormatException`, `NullPointerException`, `ArithmeticException` | `IOException` (arquivos, rede) |
| Causa típica | Erro de programação ou dado inválido | Algo **fora** do programa que pode falhar |
| O compilador obriga a tratar? | Não | **Sim**: `try`/`catch` ou `throws` |

Para uma exceção verificada, você **escolhe**: trata ali com `try`/`catch`, ou declara `throws` e deixa quem chamou tratar:

```java
static String lerPrimeiraLinha(Path arquivo) throws IOException {
    return Files.readAllLines(arquivo).get(0);
}
```

---

## Exceção própria

Quando um erro tem significado no seu sistema, dê um nome a ele:

```java
public class AlunoNaoEncontradoException extends RuntimeException {
    public AlunoNaoEncontradoException(int matricula) {
        super("Não existe aluno com a matrícula " + matricula + ".");
    }
}
```

```java
public Aluno buscar(int matricula) {
    Aluno a = alunos.get(matricula);
    if (a == null) {
        throw new AlunoNaoEncontradoException(matricula);
    }
    return a;
}
```

Quem chama `buscar` não precisa conferir `null`: se o aluno não existe, a exceção diz exatamente o quê, e o menu a mostra num único `catch`.

---

## Exercícios

### Básico (fixação)

Rode o programa `Divisao` com `10` e `0`, depois com `10` e `dois`. Que mensagens aparecem?

<!-- gabarito -->
??? success "Gabarito — Básico"
    Com `10` e `0`: “Não dá para dividir por zero.” e “Fim do cálculo.”. Com `dois`: “Digite só números inteiros.” e “Fim do cálculo.”. O `finally` aparece nos dois casos.

### Intermediário (aplicação)

Escreva `static int lerIdade(String texto)` que lança `IllegalArgumentException("Idade inválida")` se o texto não for número ou se a idade for negativa ou maior que 130.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    static int lerIdade(String texto) {
        int idade;
        try {
            idade = Integer.parseInt(texto.trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Idade inválida");
        }
        if (idade < 0 || idade > 130) {
            throw new IllegalArgumentException("Idade inválida");
        }
        return idade;
    }
    ```
    O `catch` **traduz** um erro técnico (`NumberFormatException`) num erro com significado para o sistema.

### Avançado (desafio)

Crie a exceção verificada `SaldoInsuficienteException` (que estende `Exception`) e use-a no `sacar` da `ContaBancaria` do Módulo 02. O que o compilador passa a exigir?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    public class SaldoInsuficienteException extends Exception {
        public SaldoInsuficienteException(double saldo, double valor) {
            super(String.format("Saldo de %.2f insuficiente para sacar %.2f.", saldo, valor));
        }
    }
    // na ContaBancaria:
    public void sacar(double valor) throws SaldoInsuficienteException {
        if (valor > saldo) throw new SaldoInsuficienteException(saldo, valor);
        saldo -= valor;
    }
    ```
    Por ser **verificada**, todo código que chama `sacar` precisa de `try`/`catch` ou de `throws`; senão, dá o erro `unreported exception SaldoInsuficienteException; must be caught or declared to be thrown`.

---

## 💡 Resumo

- Exceção = erro em forma de objeto; leia o tipo, a mensagem e a primeira linha `at` com arquivo seu.
- `try`/`catch` trata; `finally` sempre roda; nunca deixe um `catch` vazio.
- Verificadas (`IOException`) o compilador obriga a tratar ou declarar com `throws`.
- Exceções próprias dão nome aos erros do seu sistema.

## ➡️ Próximo passo

Na **[aula 04](04_arquivos.md)** você lê e grava arquivos.
