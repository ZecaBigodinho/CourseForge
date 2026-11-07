# 05 — Projeto do módulo: cadastro de alunos

> **Curso:** Java
> **Módulo:** 02 — Orientação a objetos
> **Tempo estimado:** 2 h

---

## Objetivos

Ao final deste projeto, você terá:

- Um **cadastro de alunos** com menu: cadastrar, lançar notas, listar e ver o resumo da turma.
- A classe `Aluno` **encapsulada**, com matrícula automática e validação.
- Um **`enum`** para a situação e uma classe `Cadastro` que guarda os alunos.

## Pré-requisitos

- Aulas [01](01_classes_e_objetos.md) a [04](04_interfaces_enum_record.md) deste módulo.

---

## As quatro classes

| Arquivo | Responsabilidade |
|---|---|
| `Situacao.java` | O `enum` com as três situações e a regra da média |
| `Aluno.java` | Os dados de um aluno e as regras das notas |
| `Cadastro.java` | Guarda os alunos, gera as matrículas, busca e conta |
| `Main.java` | O menu: conversa com o usuário e chama as outras classes |

Cada classe cuida de **uma** coisa. O `Main` não sabe calcular média; o `Aluno` não sabe ler o teclado.

!!! info "Uma prévia do Módulo 03"
    O `Cadastro` guarda os alunos numa **`List`** (`ArrayList`), uma lista que cresce sozinha, e o `Aluno` guarda as notas num **array** (`double[]`), de tamanho fixo. As listas e o `try`/`catch` são o assunto do Módulo 03; aqui, basta entender o que cada linha faz.

---

## O código

Crie a pasta `cadastro` com os quatro arquivos.

### `Situacao.java`

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

### `Aluno.java`

```java
public class Aluno {
    private static final int MAX_NOTAS = 4;

    private final int matricula;
    private String nome;
    private final double[] notas = new double[MAX_NOTAS];
    private int quantidadeNotas = 0;

    public Aluno(int matricula, String nome) {
        if (nome == null || nome.isBlank()) {
            throw new IllegalArgumentException("O nome não pode ficar vazio.");
        }
        this.matricula = matricula;
        this.nome = nome.trim();
    }

    public int getMatricula() {
        return matricula;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        if (nome == null || nome.isBlank()) {
            throw new IllegalArgumentException("O nome não pode ficar vazio.");
        }
        this.nome = nome.trim();
    }

    public boolean adicionarNota(double nota) {
        if (nota < 0 || nota > 10 || quantidadeNotas == MAX_NOTAS) {
            return false;
        }
        notas[quantidadeNotas] = nota;
        quantidadeNotas++;
        return true;
    }

    public double getMedia() {
        if (quantidadeNotas == 0) return 0;
        double soma = 0;
        for (int i = 0; i < quantidadeNotas; i++) {
            soma += notas[i];
        }
        return soma / quantidadeNotas;
    }

    public Situacao getSituacao() {
        return Situacao.para(getMedia());
    }

    @Override
    public String toString() {
        String notasTexto = quantidadeNotas == 1 ? "1 nota" : quantidadeNotas + " notas";
        return String.format("%d - %-12s média %4.1f  %s (%s)",
                matricula, nome, getMedia(), getSituacao().getRotulo(), notasTexto);
    }
}
```

### `Cadastro.java`

```java
import java.util.ArrayList;
import java.util.List;

public class Cadastro {
    private final List<Aluno> alunos = new ArrayList<>();
    private int proximaMatricula = 1001;

    public Aluno cadastrar(String nome) {
        Aluno novo = new Aluno(proximaMatricula, nome);
        alunos.add(novo);
        proximaMatricula++;
        return novo;
    }

    public Aluno buscar(int matricula) {
        for (Aluno a : alunos) {
            if (a.getMatricula() == matricula) {
                return a;
            }
        }
        return null;
    }

    public List<Aluno> listar() {
        return List.copyOf(alunos);
    }

    public int contar(Situacao situacao) {
        int total = 0;
        for (Aluno a : alunos) {
            if (a.getSituacao() == situacao) {
                total++;
            }
        }
        return total;
    }
}
```

### `Main.java`

```java
import java.util.Scanner;

public class Main {
    static Scanner entrada = new Scanner(System.in);

    static String ler(String pergunta) {
        System.out.print(pergunta);
        return entrada.nextLine().trim();
    }

    static int lerInteiro(String pergunta) {
        while (true) {
            try {
                return Integer.parseInt(ler(pergunta));
            } catch (NumberFormatException e) {
                System.out.println("  Digite um número inteiro.");
            }
        }
    }

    static double lerDecimal(String pergunta) {
        while (true) {
            try {
                return Double.parseDouble(ler(pergunta).replace(",", "."));
            } catch (NumberFormatException e) {
                System.out.println("  Digite um número, como 7,5.");
            }
        }
    }

    public static void main(String[] args) {
        Cadastro cadastro = new Cadastro();
        int opcao;
        do {
            System.out.println("\n1 - Cadastrar  2 - Lançar nota  3 - Listar  4 - Resumo  0 - Sair");
            opcao = lerInteiro("Opção: ");
            switch (opcao) {
                case 1 -> {
                    try {
                        Aluno a = cadastro.cadastrar(ler("Nome: "));
                        System.out.println("  Cadastrado com a matrícula " + a.getMatricula());
                    } catch (IllegalArgumentException e) {
                        System.out.println("  " + e.getMessage());
                    }
                }
                case 2 -> {
                    Aluno a = cadastro.buscar(lerInteiro("Matrícula: "));
                    if (a == null) {
                        System.out.println("  Aluno não encontrado.");
                    } else if (a.adicionarNota(lerDecimal("Nota: "))) {
                        System.out.printf("  Nota lançada. Média de %s: %.1f%n", a.getNome(), a.getMedia());
                    } else {
                        System.out.println("  Nota inválida (0 a 10) ou o aluno já tem 4 notas.");
                    }
                }
                case 3 -> {
                    if (cadastro.listar().isEmpty()) {
                        System.out.println("  Nenhum aluno cadastrado.");
                    }
                    for (Aluno a : cadastro.listar()) {
                        System.out.println("  " + a);
                    }
                }
                case 4 -> {
                    for (Situacao s : Situacao.values()) {
                        System.out.println("  " + s.getRotulo() + ": " + cadastro.contar(s));
                    }
                }
                case 0 -> System.out.println("Até logo!");
                default -> System.out.println("  Opção inválida.");
            }
        } while (opcao != 0);
    }
}
```

Compile tudo e rode:

```bash
javac *.java
java -Dstdout.encoding=UTF-8 Main
```

Um exemplo de uso, resumido:

```text
Opção: 1
Nome: Ana Souza
  Cadastrado com a matrícula 1001
Opção: 1
Nome: (vazio)
  O nome não pode ficar vazio.
Opção: 2
Matrícula: 1001
Nota: 9,5
  Nota lançada. Média de Ana Souza: 8,8
Opção: 2
Matrícula: 1002
Nota: 11
  Nota inválida (0 a 10) ou o aluno já tem 4 notas.
Opção: 3
  1001 - Ana Souza    média  8,8  Aprovado (2 notas)
  1002 - Bruno Lima   média  5,0  Recuperação (1 nota)
Opção: 4
  Aprovado: 1
  Recuperação: 1
  Reprovado: 0
```

| Detalhe | Por quê |
|---|---|
| `matricula` e `notas` são `final` | A matrícula nunca muda; o **array** nunca é trocado (o conteúdo dele, sim) |
| `adicionarNota` devolve `boolean` | O `Main` decide a mensagem; o `Aluno` só diz se deu certo |
| Construtor e `setNome` recusam nome vazio | Um aluno sem nome nunca existe |
| `getSituacao()` usa `Situacao.para(...)` | A regra da média fica num só lugar, o `enum` |
| `listar()` devolve `List.copyOf(...)` | Uma **cópia** que não pode ser alterada: ninguém de fora apaga alunos sem passar pelo `Cadastro` |
| `%-12s` no `toString` | Ocupa 12 caracteres alinhados à esquerda, para as colunas ficarem retas |

---

## Entrega

1. A pasta com os quatro arquivos `.java`.
2. Um print do terminal com pelo menos 3 alunos, notas lançadas, a listagem e o resumo.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Encapsulamento | Atributos `private`; só os métodos do `Aluno` mudam as notas |
| Validação | Nome vazio e notas fora de 0 a 10 recusados |
| Organização | Uma responsabilidade por classe; `enum` para a situação |
| Funciona | Matrícula automática, médias, listagem e resumo corretos |

---

## Exercícios extras

### Básico (fixação)

Acrescente ao menu a opção **5 — Renomear aluno**, usando `setNome`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    case 5 -> {
        Aluno a = cadastro.buscar(lerInteiro("Matrícula: "));
        if (a == null) {
            System.out.println("  Aluno não encontrado.");
        } else {
            try {
                a.setNome(ler("Novo nome: "));
                System.out.println("  Nome alterado.");
            } catch (IllegalArgumentException e) {
                System.out.println("  " + e.getMessage());
            }
        }
    }
    ```
    E acrescente `5 - Renomear` ao texto do menu.

### Intermediário (aplicação)

Acrescente ao `Cadastro` o método `double mediaDaTurma()` e mostre-o no resumo.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    public double mediaDaTurma() {
        if (alunos.isEmpty()) return 0;
        double soma = 0;
        for (Aluno a : alunos) soma += a.getMedia();
        return soma / alunos.size();
    }
    ```
    No `case 4`: `System.out.printf("  Média da turma: %.1f%n", cadastro.mediaDaTurma());`.

### Avançado (desafio)

Crie a interface `Avaliavel` com `double getMedia()` e `Situacao getSituacao()`, faça o `Aluno` implementá-la e mude o `contar` do `Cadastro` para trabalhar com `Avaliavel`.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    public interface Avaliavel {
        double getMedia();
        Situacao getSituacao();
    }
    ```
    `public class Aluno implements Avaliavel` (os dois métodos já existem: acrescente `@Override` neles). No `Cadastro`, o laço de `contar` pode usar `Avaliavel a : alunos`. Assim, no futuro, uma classe `Turma` ou `Disciplina` que também seja `Avaliavel` pode ser contada pelo mesmo código.

---

## 💡 Resumo

- Uma responsabilidade por classe: dados e regras no `Aluno`, coleção no `Cadastro`, conversa no `Main`.
- Encapsulamento com `private`, `final`, validação no construtor e métodos que devolvem se deu certo.
- `enum` concentra a regra da situação.

## ➡️ Próximo passo

Você terminou o **Módulo 02**. Volte ao [índice do módulo](index.md) e confira o checklist. O **Módulo 03 — Coleções, exceções e arquivos** está em produção.
