# 04 — Interfaces, enum e record

> **Curso:** Java  
> **Módulo:** 02 — Orientação a objetos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Definir um **contrato** com `interface` e implementá-lo com `implements`.
- Criar um **`enum`** para valores fixos, com atributos e métodos.
- Criar um **`record`** para dados imutáveis em uma linha.
- Escolher entre classe, interface, `enum` e `record`.

## Pré-requisitos

- [Aula 03](03_heranca_e_polimorfismo.md) deste módulo.

---

## Interfaces: “sabe fazer”

Uma **interface** diz **o que** uma classe sabe fazer, sem dizer **como**. Classes diferentes, sem parentesco, podem cumprir o mesmo contrato:

```java
public interface FormaDePagamento {
    double total(double valor);
    String descricao();
}
```

```java
public class Pix implements FormaDePagamento {
    @Override
    public double total(double valor) {
        return valor * 0.95;   // 5% de desconto
    }

    @Override
    public String descricao() {
        return "Pix (5% de desconto)";
    }
}
```

```java
public class Cartao implements FormaDePagamento {
    private final int parcelas;

    public Cartao(int parcelas) {
        this.parcelas = parcelas;
    }

    @Override
    public double total(double valor) {
        return parcelas > 1 ? valor * 1.05 : valor;   // 5% de juros se parcelar
    }

    @Override
    public String descricao() {
        return "Cartão em " + parcelas + "x";
    }
}
```

```java
FormaDePagamento[] formas = { new Pix(), new Cartao(1), new Cartao(3) };
for (FormaDePagamento f : formas) {
    System.out.printf("%s: R$ %.2f%n", f.descricao(), f.total(200));
}
```

Saída (num Windows em português):

```text
Pix (5% de desconto): R$ 190,00
Cartão em 1x: R$ 200,00
Cartão em 3x: R$ 210,00
```

| | Herança (`extends`) | Interface (`implements`) |
|---|---|---|
| Relação | “**é um**” | “**sabe fazer**” |
| Quantas | Uma classe mãe só | **Várias** interfaces |
| Traz código pronto | Sim | Não (só o contrato; *default methods* são exceção) |

---

## `enum`: um conjunto fechado de valores

```java
public enum Situacao {
    APROVADO("Aprovado"),
    RECUPERACAO("Recuperação"),
    REPROVADO("Reprovado");

    private final String rotulo;

    Situacao(String rotulo) {
        this.rotulo = rotulo;
    }

    public String getRotulo() {
        return rotulo;
    }

    public static Situacao para(double media) {
        if (media >= 7) return APROVADO;
        if (media >= 5) return RECUPERACAO;
        return REPROVADO;
    }
}
```

```java
Situacao s = Situacao.para(6.2);
System.out.println(s.getRotulo());   // Recuperação

String aviso = switch (s) {
    case APROVADO -> "Parabéns!";
    case RECUPERACAO -> "Prova de recuperação na sexta.";
    case REPROVADO -> "Converse com a coordenação.";
};
```

Com um `enum`, só existem esses três valores: um texto digitado errado como `"Aprovada"` simplesmente não compila. O `switch` com seta sobre um `enum` exige **todos** os casos.

---

## `record`: dados em uma linha

Para objetos que só **carregam dados** e não mudam:

```java
public record Endereco(String rua, String cidade, String uf) {}
```

```java
Endereco e = new Endereco("Praça da Sé", "São Paulo", "SP");
System.out.println(e.cidade());   // São Paulo
System.out.println(e);            // Endereco[rua=Praça da Sé, cidade=São Paulo, uf=SP]
```

Uma linha gera: atributos `private final`, construtor, métodos de leitura (`e.cidade()`, sem `get`), `toString`, `equals` e `hashCode`.

---

## Qual usar?

| Use | Quando |
|---|---|
| **Classe** | O objeto tem regras e estado que muda (conta bancária, aluno com notas) |
| **Interface** | Várias classes precisam cumprir o mesmo contrato (formas de pagamento) |
| **`enum`** | Um conjunto fixo e conhecido de valores (situação, turno, tamanho) |
| **`record`** | Só dados, sem mudar (endereço, coordenada, item de relatório) |

---

## Exercícios

### Básico (fixação)

Crie o `enum Turno` com `MANHA`, `TARDE` e `NOITE` e mostre todos com `Turno.values()`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    public enum Turno { MANHA, TARDE, NOITE }
    // no main:
    for (Turno t : Turno.values()) {
        System.out.println(t);
    }
    ```

### Intermediário (aplicação)

Crie a forma de pagamento `Boleto`, com 2% de desconto, e acrescente-a ao array da aula.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    public class Boleto implements FormaDePagamento {
        @Override public double total(double valor) { return valor * 0.98; }
        @Override public String descricao() { return "Boleto (2% de desconto)"; }
    }
    ```
    O `for` não muda: `Boleto (2% de desconto): R$ 196,00`.

### Avançado (desafio)

Crie `record Nota(String disciplina, double valor)` que recusa valores fora de 0 a 10.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    public record Nota(String disciplina, double valor) {
        public Nota {
            if (valor < 0 || valor > 10) {
                throw new IllegalArgumentException("Nota deve estar entre 0 e 10.");
            }
        }
    }
    ```
    Esse é o **construtor compacto** do `record`: valida antes de guardar os valores.

---

## 💡 Resumo

- `interface` = contrato (“sabe fazer”); uma classe pode implementar várias.
- `enum` = valores fixos, com atributos e métodos; ótimo no `switch`.
- `record` = dados imutáveis numa linha, com construtor, leitura e `toString` prontos.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_cadastro.md)** você monta o cadastro de alunos.
