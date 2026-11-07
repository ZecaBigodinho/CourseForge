# 02 — Encapsulamento e construtores

> **Curso:** Java  
> **Módulo:** 02 — Orientação a objetos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Proteger atributos com `private` e expor só o necessário com *getters* e *setters*.
- Criar **construtores** que obrigam o objeto a nascer válido.
- **Validar** dados e recusar valores errados com `throw`.
- Sobrescrever `toString()` para mostrar o objeto.

## Pré-requisitos

- [Aula 01](01_classes_e_objetos.md) deste módulo.

---

## O problema

Com atributos abertos, qualquer parte do programa pode quebrar as regras:

```java
conta.saldo = -1000;   // ninguém impede
aluno.nota = 15;       // nota impossível
```

**Encapsulamento** é esconder os dados dentro do objeto e deixar que só os **métodos dele** os alterem, aplicando as regras.

---

## `private`, construtor, getters e validação

```java
public class ContaBancaria {
    private final String titular;
    private double saldo;

    public ContaBancaria(String titular, double saldoInicial) {
        if (titular == null || titular.isBlank()) {
            throw new IllegalArgumentException("O titular é obrigatório.");
        }
        if (saldoInicial < 0) {
            throw new IllegalArgumentException("O saldo inicial não pode ser negativo.");
        }
        this.titular = titular;
        this.saldo = saldoInicial;
    }

    public String getTitular() {
        return titular;
    }

    public double getSaldo() {
        return saldo;
    }

    public void depositar(double valor) {
        if (valor <= 0) {
            throw new IllegalArgumentException("O depósito deve ser positivo.");
        }
        saldo += valor;
    }

    public boolean sacar(double valor) {
        if (valor <= 0 || valor > saldo) {
            return false;
        }
        saldo -= valor;
        return true;
    }

    @Override
    public String toString() {
        return String.format("Conta de %s — saldo R$ %.2f", titular, saldo);
    }
}
```

| Recurso | Para quê |
|---|---|
| `private` | Só a própria classe enxerga o atributo |
| `final` | O atributo é definido uma vez (no construtor) e nunca muda |
| **Construtor** (mesmo nome da classe, sem tipo de retorno) | Roda no `new` e garante que o objeto já nasce válido |
| `this.titular = titular` | O `this` separa o atributo do parâmetro de mesmo nome |
| *Getter* `getSaldo()` | Permite **ler** sem permitir **mudar** |
| `throw new IllegalArgumentException(...)` | Recusa um valor errado, interrompendo a operação com uma mensagem |
| `@Override toString()` | Define como o objeto aparece num `println` |

Uso:

```java
ContaBancaria conta = new ContaBancaria("Ana Souza", 100);
conta.depositar(50);
System.out.println(conta.sacar(500));   // false: saldo insuficiente
System.out.println(conta);              // Conta de Ana Souza — saldo R$ 150,00
// conta.saldo = -1000;                 // não compila: saldo é private
```

!!! info "`throw` e exceções"
    O `throw` “lança” um erro que interrompe o programa, a menos que alguém o trate com `try`/`catch` (como no `lerDecimal` do Módulo 01). Exceções são o assunto do Módulo 03; por ora, use `throw` para recusar dados inválidos em construtores e métodos.

!!! tip "Não crie setter para tudo"
    Gerar *getters* e *setters* para todos os atributos desfaz o encapsulamento. Crie só os que fazem sentido: a conta tem `depositar` e `sacar`, e não um `setSaldo`.

---

## Exercícios

### Básico (fixação)

Torne `private` os atributos da classe `Aluno` (nome e nota) e crie um construtor e os *getters*.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    public class Aluno {
        private final String nome;
        private final double nota;

        public Aluno(String nome, double nota) {
            this.nome = nome;
            this.nota = nota;
        }

        public String getNome() { return nome; }
        public double getNota() { return nota; }
    }
    // uso: Aluno a = new Aluno("Ana", 9);
    ```

### Intermediário (aplicação)

Faça o construtor do `Aluno` recusar notas fora de 0 a 10 e teste com `new Aluno("Bia", 15)`. O que acontece?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    if (nota < 0 || nota > 10) {
        throw new IllegalArgumentException("Nota deve estar entre 0 e 10.");
    }
    ```
    O programa para com `Exception in thread "main" java.lang.IllegalArgumentException: Nota deve estar entre 0 e 10.`, apontando a linha. Um aluno com nota 15 **nunca chega a existir**.

### Avançado (desafio)

Acrescente à `ContaBancaria` o método `boolean transferir(ContaBancaria destino, double valor)`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    public boolean transferir(ContaBancaria destino, double valor) {
        if (destino == null || destino == this || !sacar(valor)) {
            return false;
        }
        destino.depositar(valor);
        return true;
    }
    ```
    A transferência **reaproveita** `sacar` e `depositar`, então as regras de cada um continuam valendo. Um objeto pode chamar métodos de outro objeto da mesma classe.

---

## 💡 Resumo

- Atributos `private`; só os métodos da classe os alteram.
- Construtor garante o objeto válido desde o `new`; `final` para o que não muda.
- `throw new IllegalArgumentException("…")` recusa dados errados.
- *Getters* para ler; *setters* só quando fizer sentido; `toString()` com `@Override`.

## ➡️ Próximo passo

Na **[aula 03](03_heranca_e_polimorfismo.md)** você reaproveita classes com herança.
