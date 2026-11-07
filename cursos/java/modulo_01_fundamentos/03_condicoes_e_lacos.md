# 03 — Condições e laços

> **Curso:** Java  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Tomar decisões com `if`, `else if` e `else`.
- Usar o `switch` moderno (com `->`).
- Comparar textos corretamente com `equals`.
- Repetir com `for`, `while` e `do…while`, e sair com `break`.

## Pré-requisitos

- [Aula 02](02_variaveis_e_tipos.md) deste módulo.

---

## `if`, `else if`, `else`

```java
double media = 6.5;
int frequencia = 90;

if (frequencia < 75) {
    System.out.println("Reprovado por falta");
} else if (media >= 7) {
    System.out.println("Aprovado");
} else if (media >= 5) {
    System.out.println("Recuperação");
} else {
    System.out.println("Reprovado");
}
```

| Operador | Significa |
|---|---|
| `==` / `!=` | Igual / diferente (para **números**, `char` e `boolean`) |
| `>`, `<`, `>=`, `<=` | Comparações |
| `&&` / `\|\|` / `!` | E / OU / NÃO |

!!! danger "Textos se comparam com `equals`"
    `nome == "Ana"` compara se são o **mesmo objeto** na memória, e pode dar `false` mesmo com o mesmo texto. Para comparar o **conteúdo** de `String`s, use `nome.equals("Ana")` (ou `nome.equalsIgnoreCase("ana")` para ignorar maiúsculas).

---

## `switch`

Quando há várias opções para um mesmo valor, o `switch` com seta (`->`, Java 14+) é mais limpo:

```java
int opcao = 2;
String acao = switch (opcao) {
    case 1 -> "Cadastrar";
    case 2 -> "Listar";
    case 3 -> "Sair";
    default -> "Opção inválida";
};
System.out.println(acao); // Listar
```

Com a seta, não é preciso `break` e o `switch` pode **devolver um valor**. Ele funciona com `int`, `char`, `String` e `enum` (Módulo 02).

---

## Laços

### `for`: quantidade conhecida

```java
for (int i = 1; i <= 10; i++) {
    System.out.println("7 x " + i + " = " + (7 * i));
}
```

As três partes: **começo** (`int i = 1`), **condição** para continuar (`i <= 10`) e **passo** (`i++`).

### `while`: enquanto uma condição for verdadeira

```java
double saldo = 100;
int saques = 0;
while (saldo >= 30) {
    saldo -= 30;
    saques++;
}
System.out.println(saques + " saques, sobrou " + saldo); // 3 saques, sobrou 10.0
```

### `do…while`: roda pelo menos uma vez

```java
int tentativa = 0;
do {
    tentativa++;
    System.out.println("Tentativa " + tentativa);
} while (tentativa < 3);
```

Ótimo para menus: o menu aparece **antes** de testar se é para sair.

`break` sai do laço na hora; `continue` pula para a próxima volta.

---

## Exercícios

### Básico (fixação)

Dada uma idade, mostre “criança” (até 12), “adolescente” (13 a 17) ou “adulto” (18 ou mais).

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    int idade = 15;
    if (idade <= 12) {
        System.out.println("criança");
    } else if (idade <= 17) {
        System.out.println("adolescente");
    } else {
        System.out.println("adulto");
    }
    ```

### Intermediário (aplicação)

Some os números de 1 a 100 com um `for` e mostre o resultado.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    int soma = 0;
    for (int i = 1; i <= 100; i++) {
        soma += i;
    }
    System.out.println(soma); // 5050
    ```

### Avançado (desafio)

Mostre os 10 primeiros números da sequência de Fibonacci (0, 1, 1, 2, 3, 5…), em que cada número é a soma dos dois anteriores.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    int a = 0, b = 1;
    for (int i = 0; i < 10; i++) {
        System.out.print(a + " ");
        int proximo = a + b;
        a = b;
        b = proximo;
    }
    System.out.println();
    // 0 1 1 2 3 5 8 13 21 34
    ```

---

## 💡 Resumo

- `if`/`else if`/`else` com `&&`, `||` e `!`.
- `switch` com `->` não precisa de `break` e pode devolver valor.
- `String` se compara com **`equals`**, nunca com `==`.
- `for` (quantidade conhecida), `while` (condição), `do…while` (pelo menos uma vez).

## ➡️ Próximo passo

Na **[aula 04](04_metodos_e_scanner.md)** você divide o código em métodos e lê o teclado.
