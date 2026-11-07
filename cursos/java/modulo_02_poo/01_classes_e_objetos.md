# 01 — Classes e objetos

> **Curso:** Java  
> **Módulo:** 02 — Orientação a objetos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que são **classe**, **objeto**, **atributo** e **método**.
- Criar uma classe e **instanciar** objetos com `new`.
- Escrever métodos que usam os atributos do próprio objeto (`this`).
- Entender, enfim, o que significa o `static` do `main`.

## Pré-requisitos

- [Módulo 01](../modulo_01_fundamentos/index.md) completo.

---

## Classe é a forma, objeto é o bolo

Uma **classe** é um molde: descreve **quais dados** (atributos) e **quais ações** (métodos) algo tem. Um **objeto** é uma coisa concreta feita a partir do molde.

| Classe `Produto` | Objetos |
|---|---|
| tem `nome` e `preco` | caderno: "Caderno", 24,90 |
| sabe `precoComDesconto(…)` | caneta: "Caneta", 2,50 |

## A primeira classe

`Produto.java`:

```java
public class Produto {
    String nome;
    double preco;

    double precoComDesconto(double percentual) {
        return preco * (1 - percentual / 100);
    }

    void mostrar() {
        System.out.printf("%s: R$ %.2f%n", nome, preco);
    }
}
```

`Loja.java`, na mesma pasta:

```java
public class Loja {
    public static void main(String[] args) {
        Produto caderno = new Produto();
        caderno.nome = "Caderno";
        caderno.preco = 24.9;

        Produto caneta = new Produto();
        caneta.nome = "Caneta";
        caneta.preco = 2.5;

        caderno.mostrar();
        caneta.mostrar();
        System.out.printf("Caderno com 10%%: R$ %.2f%n", caderno.precoComDesconto(10));
    }
}
```

Compile os dois e rode:

```bash
javac Produto.java Loja.java
java Loja
```

- `new Produto()` cria um objeto novo; cada um tem **os seus** valores de `nome` e `preco`.
- `caderno.mostrar()` chama o método **daquele** objeto: o `preco` usado é o do caderno.
- No `printf`, `%%` mostra o símbolo `%`.

!!! info "`this`"
    Dentro de um método, `this` é “o objeto que está rodando este método”. `preco` e `this.preco` são a mesma coisa; o `this` fica obrigatório quando um parâmetro tem o mesmo nome do atributo (aula 02).

---

## E o `static`?

- Um método **sem** `static` pertence a cada **objeto**: precisa de um objeto para ser chamado (`caderno.mostrar()`).
- Um método **com** `static` pertence à **classe**: é chamado sem objeto (`Math.round(…)`, `Integer.parseInt(…)`).

O `main` é `static` porque a JVM precisa chamá-lo **antes** de existir qualquer objeto. Por isso, no Módulo 01, todos os métodos eram `static`: eram chamados direto do `main`.

---

## Exercícios

### Básico (fixação)

Crie a classe `Aluno` com `nome` e `nota`, e um `main` que cria dois alunos e mostra os dados de cada um.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    public class Aluno {
        String nome;
        double nota;
    }
    // no main de outra classe:
    Aluno a = new Aluno();
    a.nome = "Ana";
    a.nota = 9;
    Aluno b = new Aluno();
    b.nome = "Bruno";
    b.nota = 6.5;
    System.out.println(a.nome + ": " + a.nota);
    System.out.println(b.nome + ": " + b.nota);
    ```

### Intermediário (aplicação)

Acrescente ao `Aluno` o método `boolean aprovado()`, verdadeiro com nota a partir de 7, e use-o.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    boolean aprovado() {
        return nota >= 7;
    }
    // no main:
    System.out.println(a.nome + (a.aprovado() ? " passou" : " não passou"));
    ```

### Avançado (desafio)

Crie a classe `ContaBancaria` com `titular` e `saldo` e os métodos `depositar(double valor)` e `boolean sacar(double valor)`, que não deixa o saldo ficar negativo.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    public class ContaBancaria {
        String titular;
        double saldo;

        void depositar(double valor) {
            if (valor > 0) saldo += valor;
        }

        boolean sacar(double valor) {
            if (valor <= 0 || valor > saldo) return false;
            saldo -= valor;
            return true;
        }
    }
    ```
    Mas ainda dá para fazer `conta.saldo = -1000;` direto, burlando a regra. A aula 02 resolve isso com **encapsulamento**.

---

## 💡 Resumo

- Classe = molde (atributos + métodos); objeto = coisa concreta criada com `new`.
- Cada objeto tem os seus próprios valores; `this` é o objeto atual.
- Sem `static`: método do objeto; com `static`: método da classe (como o `main`).

## ➡️ Próximo passo

Na **[aula 02](02_encapsulamento.md)** você protege os dados dos objetos.
