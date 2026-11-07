# 05 — Projeto final: cadastro com arquivo CSV

> **Curso:** Java
> **Módulo:** 03 — Coleções, exceções e arquivos
> **Tempo estimado:** 3 h

---

## Objetivos

Ao final deste projeto, você terá:

- O **cadastro de alunos** que **salva** em `alunos.csv` a cada mudança e **carrega** ao abrir.
- As notas numa `List`, os alunos num `Map` e relatórios feitos com **streams** (ranking e contagem por situação).
- Os erros tratados com **exceções**, inclusive uma própria, sem derrubar o programa.
- O requisito do certificado do curso.

## Pré-requisitos

- Aulas [01](01_colecoes.md) a [04](04_arquivos.md) deste módulo e o [projeto do Módulo 02](../modulo_02_poo/05_projeto_cadastro.md).

---

## O que mudou desde o Módulo 02

| Módulo 02 | Módulo 03 |
|---|---|
| Notas num array `double[4]` | Notas numa `List<Double>` |
| Alunos numa `List`, busca com `for` | Alunos num `Map<Integer, Aluno>`, busca direta pela matrícula |
| `buscar` devolve `null` | `buscar` lança `AlunoNaoEncontradoException` |
| `adicionarNota` devolve `boolean` | `adicionarNota` lança exceção com a mensagem do problema |
| Média e contagem com `for` | Média, ranking e contagem com **streams** |
| Tudo some ao fechar | `RepositorioCsv` salva e carrega `alunos.csv` |

---

## O código

Pasta `cadastro-csv` com seis arquivos.

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
import java.util.ArrayList;
import java.util.List;

public class Aluno {
    public static final int MAX_NOTAS = 4;

    private final int matricula;
    private final String nome;
    private final List<Double> notas = new ArrayList<>();

    public Aluno(int matricula, String nome) {
        if (nome == null || nome.isBlank()) {
            throw new IllegalArgumentException("O nome não pode ficar vazio.");
        }
        if (nome.contains(";")) {
            throw new IllegalArgumentException("O nome não pode ter ponto e vírgula.");
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

    public List<Double> getNotas() {
        return List.copyOf(notas);
    }

    public void adicionarNota(double nota) {
        if (nota < 0 || nota > 10) {
            throw new IllegalArgumentException("A nota deve estar entre 0 e 10.");
        }
        if (notas.size() == MAX_NOTAS) {
            throw new IllegalStateException(nome + " já tem " + MAX_NOTAS + " notas.");
        }
        notas.add(nota);
    }

    public double getMedia() {
        return notas.stream().mapToDouble(Double::doubleValue).average().orElse(0);
    }

    public Situacao getSituacao() {
        return Situacao.para(getMedia());
    }

    @Override
    public String toString() {
        return String.format("%d - %-12s média %4.1f  %-11s notas %s",
                matricula, nome, getMedia(), getSituacao().getRotulo(), notas);
    }
}
```

### `AlunoNaoEncontradoException.java`

```java
public class AlunoNaoEncontradoException extends RuntimeException {
    public AlunoNaoEncontradoException(int matricula) {
        super("Não existe aluno com a matrícula " + matricula + ".");
    }
}
```

### `Cadastro.java`

```java
import java.util.Collection;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Cadastro {
    private final Map<Integer, Aluno> alunos = new LinkedHashMap<>();
    private int proximaMatricula = 1001;

    public Aluno cadastrar(String nome) {
        Aluno novo = new Aluno(proximaMatricula, nome);
        alunos.put(novo.getMatricula(), novo);
        proximaMatricula++;
        return novo;
    }

    public void incluir(Aluno aluno) {
        alunos.put(aluno.getMatricula(), aluno);
        proximaMatricula = Math.max(proximaMatricula, aluno.getMatricula() + 1);
    }

    public Aluno buscar(int matricula) {
        Aluno a = alunos.get(matricula);
        if (a == null) {
            throw new AlunoNaoEncontradoException(matricula);
        }
        return a;
    }

    public Collection<Aluno> todos() {
        return List.copyOf(alunos.values());
    }

    public List<Aluno> rankingPorMedia() {
        return alunos.values().stream()
                .sorted(Comparator.comparingDouble(Aluno::getMedia).reversed())
                .toList();
    }

    public Map<Situacao, Long> contagemPorSituacao() {
        Map<Situacao, Long> contagem = new EnumMap<>(Situacao.class);
        for (Situacao s : Situacao.values()) {
            contagem.put(s, 0L);
        }
        contagem.putAll(alunos.values().stream()
                .collect(Collectors.groupingBy(Aluno::getSituacao, Collectors.counting())));
        return contagem;
    }
}
```

### `RepositorioCsv.java`

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Locale;

public class RepositorioCsv {
    private static final String CABECALHO = "matricula;nome;notas";
    private final Path arquivo;

    public RepositorioCsv(Path arquivo) {
        this.arquivo = arquivo;
    }

    public void salvar(Collection<Aluno> alunos) throws IOException {
        List<String> linhas = new ArrayList<>();
        linhas.add(CABECALHO);
        for (Aluno a : alunos) {
            List<String> notas = a.getNotas().stream()
                    .map(n -> String.format(Locale.ROOT, "%.1f", n))
                    .toList();
            linhas.add(a.getMatricula() + ";" + a.getNome() + ";" + String.join("|", notas));
        }
        Files.write(arquivo, linhas, StandardCharsets.UTF_8);
    }

    public List<Aluno> carregar() throws IOException {
        List<Aluno> alunos = new ArrayList<>();
        if (!Files.exists(arquivo)) {
            return alunos;
        }
        List<String> linhas = Files.readAllLines(arquivo, StandardCharsets.UTF_8);
        for (int i = 1; i < linhas.size(); i++) {
            String linha = linhas.get(i);
            if (linha.isBlank()) continue;
            try {
                String[] partes = linha.split(";", -1);
                Aluno a = new Aluno(Integer.parseInt(partes[0].trim()), partes[1]);
                if (!partes[2].isBlank()) {
                    for (String nota : partes[2].split("\\|")) {
                        a.adicionarNota(Double.parseDouble(nota));
                    }
                }
                alunos.add(a);
            } catch (RuntimeException e) {
                System.out.println("  Aviso: linha " + (i + 1) + " ignorada (" + e.getMessage() + ")");
            }
        }
        return alunos;
    }
}
```

### `Main.java`

```java
import java.io.IOException;
import java.nio.file.Path;
import java.util.Map;
import java.util.Scanner;

public class Main {
    static final Scanner entrada = new Scanner(System.in);
    static final RepositorioCsv repositorio = new RepositorioCsv(Path.of("alunos.csv"));
    static final Cadastro cadastro = new Cadastro();

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

    static void salvar() {
        try {
            repositorio.salvar(cadastro.todos());
        } catch (IOException e) {
            System.out.println("  Não foi possível salvar: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        try {
            for (Aluno a : repositorio.carregar()) {
                cadastro.incluir(a);
            }
            System.out.println(cadastro.todos().size() + " aluno(s) carregado(s) de alunos.csv");
        } catch (IOException e) {
            System.out.println("Não foi possível ler alunos.csv: " + e.getMessage());
        }

        int opcao;
        do {
            System.out.println("\n1 - Cadastrar  2 - Lançar nota  3 - Listar  4 - Ranking  5 - Resumo  0 - Sair");
            opcao = lerInteiro("Opção: ");
            try {
                switch (opcao) {
                    case 1 -> {
                        Aluno a = cadastro.cadastrar(ler("Nome: "));
                        salvar();
                        System.out.println("  Cadastrado com a matrícula " + a.getMatricula());
                    }
                    case 2 -> {
                        Aluno a = cadastro.buscar(lerInteiro("Matrícula: "));
                        a.adicionarNota(lerDecimal("Nota: "));
                        salvar();
                        System.out.printf("  Nota lançada. Média de %s: %.1f%n", a.getNome(), a.getMedia());
                    }
                    case 3 -> cadastro.todos().forEach(a -> System.out.println("  " + a));
                    case 4 -> {
                        int posicao = 1;
                        for (Aluno a : cadastro.rankingPorMedia()) {
                            System.out.printf("  %dº %s (%.1f)%n", posicao++, a.getNome(), a.getMedia());
                        }
                    }
                    case 5 -> {
                        for (Map.Entry<Situacao, Long> e : cadastro.contagemPorSituacao().entrySet()) {
                            System.out.println("  " + e.getKey().getRotulo() + ": " + e.getValue());
                        }
                    }
                    case 0 -> System.out.println("Dados salvos em alunos.csv. Até logo!");
                    default -> System.out.println("  Opção inválida.");
                }
            } catch (AlunoNaoEncontradoException | IllegalArgumentException | IllegalStateException e) {
                System.out.println("  " + e.getMessage());
            }
        } while (opcao != 0);
    }
}
```

Compile e rode na pasta do projeto:

```bash
javac *.java
java -Dstdout.encoding=UTF-8 Main
```

### Testado em duas execuções

Na primeira, cadastrando Ana, Bruno e Carla e lançando notas (uma nota 12 e uma matrícula 7777 foram recusadas com mensagem), o arquivo ficou assim:

```text
matricula;nome;notas
1001;Ana Souza;9.0|8.5
1002;Bruno Lima;4.0
1003;Carla Dias;7.0
```

Na segunda execução, com uma linha estragada acrescentada de propósito no fim do arquivo (`abc;Zé;`):

```text
  Aviso: linha 5 ignorada (For input string: "abc")
3 aluno(s) carregado(s) de alunos.csv
Opção: 3
  1001 - Ana Souza    média  8,8  Aprovado    notas [9.0, 8.5]
  1002 - Bruno Lima   média  4,0  Reprovado   notas [4.0]
  1003 - Carla Dias   média  7,0  Aprovado    notas [7.0]
Opção: 1
Nome: Diego Rocha
  Cadastrado com a matrícula 1004
```

| Detalhe | Por quê |
|---|---|
| `LinkedHashMap` | Busca pela matrícula **e** lista na ordem de cadastro |
| `incluir` ajusta `proximaMatricula` | Depois de carregar o arquivo, a próxima matrícula continua a sequência (1004) |
| Nome com `;` recusado no construtor | Um `;` no nome quebraria as colunas do CSV |
| Notas gravadas com `Locale.ROOT` | Sempre com ponto (`8.5`), que o `Double.parseDouble` lê em qualquer computador |
| `try`/`catch` por linha no `carregar` | Uma linha ruim é avisada e pulada; as outras carregam |
| Um `catch` com três tipos no `Main` | Matrícula inexistente, nota inválida e limite de notas viram mensagens, e o menu continua |
| `salvar()` depois de cada mudança | Se o computador desligar, nada se perde |

!!! info "A linha estragada some do arquivo"
    Depois da segunda execução, ao salvar, o arquivo é regravado só com os alunos válidos: a linha `abc;Zé;` desaparece. Num sistema real, você guardaria uma cópia do arquivo original antes de regravar.

---

## Entrega (requisito do certificado)

1. A pasta com os seis arquivos `.java` e o `alunos.csv` gerado.
2. Prints de **duas execuções**: a primeira cadastrando e lançando notas, a segunda mostrando os dados carregados do arquivo.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| Persistência | Os dados voltam na segunda execução; o CSV abre no Excel |
| Coleções e streams | `List` nas notas, `Map` nos alunos, ranking e contagem com streams |
| Exceções | Exceção própria; erros viram mensagens; linha ruim do CSV não derruba o programa |
| Organização | Uma responsabilidade por classe (`RepositorioCsv` separado do `Cadastro`) |

---

## Exercícios extras

### Básico (fixação)

Abra o `alunos.csv` no Excel (ou no LibreOffice Calc). As colunas aparecem separadas?

<!-- gabarito -->
??? success "Gabarito — Básico"
    Num Excel em português, o `;` é o separador padrão: as três colunas aparecem certinhas. As notas ficam todas na terceira coluna, separadas por `|`. Se o arquivo abrir com tudo numa coluna só, use **Dados ➔ Texto para Colunas** e escolha o ponto e vírgula.

### Intermediário (aplicação)

Acrescente ao menu a opção **6 — Remover aluno**, que remove pela matrícula e salva.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    No `Cadastro`:
    ```java
    public void remover(int matricula) {
        if (alunos.remove(matricula) == null) {
            throw new AlunoNaoEncontradoException(matricula);
        }
    }
    ```
    No `Main`: `case 6 -> { cadastro.remover(lerInteiro("Matrícula: ")); salvar(); System.out.println("  Removido."); }`. Matrícula inexistente cai no `catch` que já existe.

### Avançado (desafio)

Antes de regravar o `alunos.csv`, guarde uma cópia como `alunos.bak`, para não perder linhas que não puderam ser lidas.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    No começo do `salvar` do `RepositorioCsv`:
    ```java
    if (Files.exists(arquivo)) {
        Files.copy(arquivo, arquivo.resolveSibling("alunos.bak"), StandardCopyOption.REPLACE_EXISTING);
    }
    ```
    (`import java.nio.file.StandardCopyOption;`). Assim, a linha estragada continua guardada no `.bak` para alguém corrigir à mão.

---

## 💡 Resumo

- `List` e `Map` guardam os dados; streams fazem os relatórios.
- Exceções próprias e `catch` no menu transformam erros em mensagens.
- `RepositorioCsv` grava e lê em UTF-8, uma linha ruim de cada vez.

## ➡️ Próximo passo

Parabéns, você terminou o curso de **Java**! Volte ao [índice do módulo](index.md) e confira o checklist. Bons próximos passos: um **banco de dados** com JDBC no lugar do CSV, testes automatizados com **JUnit** e, depois, o **Spring Boot** para criar sistemas web em Java.
