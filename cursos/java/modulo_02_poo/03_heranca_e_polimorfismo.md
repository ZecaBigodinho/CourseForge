# 03 — Herança e polimorfismo

> **Curso:** Java  
> **Módulo:** 02 — Orientação a objetos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Criar uma classe **filha** com `extends` e chamar o construtor da mãe com `super`.
- **Sobrescrever** métodos com `@Override`.
- Usar **polimorfismo**: tratar objetos diferentes pelo tipo da classe mãe.
- Criar classes **abstratas** e entender o `protected`.

## Pré-requisitos

- [Aula 02](02_encapsulamento.md) deste módulo.

---

## Herança: “é um”

Na escola, um **aluno** é uma pessoa e um **professor** também é. Os dois têm nome e e-mail, mas cada um tem coisas próprias. A **herança** põe o que é comum na classe mãe:

```java
public abstract class Pessoa {
    private final String nome;
    private final String email;

    protected Pessoa(String nome, String email) {
        this.nome = nome;
        this.email = email;
    }

    public String getNome() { return nome; }
    public String getEmail() { return email; }

    public abstract String descricao();
}
```

```java
public class Aluno extends Pessoa {
    private final String turma;

    public Aluno(String nome, String email, String turma) {
        super(nome, email);           // chama o construtor de Pessoa
        this.turma = turma;
    }

    @Override
    public String descricao() {
        return getNome() + " — aluno(a) da turma " + turma;
    }
}
```

```java
public class Professor extends Pessoa {
    private final String disciplina;

    public Professor(String nome, String email, String disciplina) {
        super(nome, email);
        this.disciplina = disciplina;
    }

    @Override
    public String descricao() {
        return getNome() + " — professor(a) de " + disciplina;
    }
}
```

| Palavra | Significa |
|---|---|
| `extends Pessoa` | `Aluno` **herda** tudo o que `Pessoa` tem de público e protegido |
| `super(nome, email)` | Chama o construtor da mãe (deve ser a primeira linha) |
| `abstract class` | Classe que serve só de base: não dá para fazer `new Pessoa(…)` |
| `abstract String descricao();` | Método sem corpo que **toda** filha é obrigada a escrever |
| `protected` | Visível na própria classe e nas filhas |
| `@Override` | Avisa que o método substitui um da mãe: o compilador confere se o nome e os parâmetros batem |

---

## Polimorfismo

“Muitas formas”: uma variável do tipo da **mãe** pode guardar qualquer **filha**, e cada uma responde do seu jeito:

```java
public class Escola {
    public static void main(String[] args) {
        Pessoa[] pessoas = {
            new Aluno("Ana Souza", "ana.souza@example.com", "1º A"),
            new Professor("Carlos Melo", "carlos@example.com", "Matemática"),
            new Aluno("Bruno Lima", "bruno@example.com", "2º B"),
        };

        for (Pessoa p : pessoas) {
            System.out.println(p.descricao());
        }
    }
}
```

Saída:

```text
Ana Souza — aluno(a) da turma 1º A
Carlos Melo — professor(a) de Matemática
Bruno Lima — aluno(a) da turma 2º B
```

O `for` não precisa saber quem é aluno e quem é professor: chama `descricao()`, e o Java escolhe a versão certa **na hora de rodar**. Para acrescentar um `Coordenador`, basta criar a classe; o `for` continua igual.

!!! tip "Herança com moderação"
    Use herança só quando a relação é de verdade “**é um**” (um aluno **é uma** pessoa). Para “**tem um**” (um aluno **tem** notas), use um atributo. Hierarquias muito longas ficam difíceis de mudar; muitas vezes, **interfaces** (próxima aula) resolvem melhor.

---

## Exercícios

### Básico (fixação)

Crie a classe `Coordenador extends Pessoa`, com o atributo `setor`, e acrescente um coordenador ao array da aula.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    public class Coordenador extends Pessoa {
        private final String setor;
        public Coordenador(String nome, String email, String setor) {
            super(nome, email);
            this.setor = setor;
        }
        @Override
        public String descricao() {
            return getNome() + " — coordenação de " + setor;
        }
    }
    ```
    O `for` do `main` não muda: é o polimorfismo funcionando.

### Intermediário (aplicação)

Tente escrever `new Pessoa("X", "x@example.com")`. E tire o método `descricao()` do `Coordenador`. O que o compilador diz em cada caso?

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    `new Pessoa(…)` dá `Pessoa is abstract; cannot be instantiated`: classe abstrata não vira objeto. Sem `descricao()`, o `Coordenador` dá `Coordenador is not abstract and does not override abstract method descricao() in Pessoa`: a filha é **obrigada** a escrever o método abstrato.

### Avançado (desafio)

Conte quantos alunos há no array usando `instanceof`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    int alunos = 0;
    for (Pessoa p : pessoas) {
        if (p instanceof Aluno) {
            alunos++;
        }
    }
    System.out.println(alunos + " alunos");
    ```
    `instanceof` confere o tipo real do objeto. Use com moderação: se você precisa perguntar o tipo o tempo todo, talvez o comportamento devesse estar num método sobrescrito.

---

## 💡 Resumo

- `extends` herda; `super(…)` chama o construtor da mãe.
- `abstract`: classe que não vira objeto e métodos que as filhas devem escrever.
- `@Override` sobrescreve com conferência do compilador.
- Polimorfismo: variável do tipo da mãe, comportamento da filha, escolhido ao rodar.

## ➡️ Próximo passo

Na **[aula 04](04_interfaces_enum_record.md)** você conhece interfaces, `enum` e `record`.
