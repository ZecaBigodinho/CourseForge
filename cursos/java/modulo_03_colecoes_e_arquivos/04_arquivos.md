# 04 — Arquivos

> **Curso:** Java  
> **Módulo:** 03 — Coleções, exceções e arquivos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Representar caminhos com **`Path`**.
- Gravar e ler arquivos de texto com **`Files`**, sempre em UTF-8.
- Tratar a `IOException`.
- Montar e ler um arquivo **CSV** simples.

## Pré-requisitos

- [Aula 03](03_excecoes.md) deste módulo.

---

## `Path` e `Files`

O pacote `java.nio.file` traz o jeito moderno de trabalhar com arquivos:

```java
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Diario {
    public static void main(String[] args) {
        Path arquivo = Path.of("diario.txt");
        try {
            Files.writeString(arquivo, "Primeira linha\nSegunda linha\n", StandardCharsets.UTF_8);

            List<String> linhas = Files.readAllLines(arquivo, StandardCharsets.UTF_8);
            System.out.println(linhas.size() + " linhas");   // 2 linhas
            for (String linha : linhas) {
                System.out.println("> " + linha);
            }
        } catch (IOException e) {
            System.out.println("Erro ao usar o arquivo: " + e.getMessage());
        }
    }
}
```

| Método | Faz |
|---|---|
| `Path.of("pasta", "arquivo.txt")` | Monta um caminho (relativo à pasta onde o programa roda) |
| `Files.writeString(p, texto)` | Grava o texto (cria ou **substitui** o arquivo) |
| `Files.write(p, listaDeLinhas)` | Grava uma linha por item |
| `Files.readString(p)` / `Files.readAllLines(p)` | Lê tudo como texto / como lista de linhas |
| `Files.exists(p)` | O arquivo existe? |
| `Files.createDirectories(p)` | Cria as pastas que faltam |

Para **acrescentar** sem apagar: `Files.writeString(p, texto, StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND)`.

!!! tip "Sempre UTF-8"
    Informe `StandardCharsets.UTF_8` ao ler e ao gravar: assim os acentos não se perdem quando o arquivo vai para outro computador. (Desde o Java 18 esse já é o padrão, mas deixar explícito evita surpresas com versões mais antigas.)

---

## CSV: uma tabela em texto

**CSV** é um arquivo de texto em que cada linha é um registro e um separador divide os campos. No Brasil, o Excel usa **ponto e vírgula** (porque a vírgula é o separador decimal):

```text
matricula;nome;notas
1001;Ana Souza;9.0|8.5
1002;Bruno Lima;4.0
```

### Gravar

```java
List<String> linhas = new ArrayList<>();
linhas.add("matricula;nome;notas");
for (Aluno a : alunos) {
    linhas.add(a.getMatricula() + ";" + a.getNome() + ";" + juntarNotas(a));
}
Files.write(arquivo, linhas, StandardCharsets.UTF_8);
```

### Ler

```java
List<String> linhas = Files.readAllLines(arquivo, StandardCharsets.UTF_8);
for (int i = 1; i < linhas.size(); i++) {            // começa em 1: pula o cabeçalho
    String[] partes = linhas.get(i).split(";", -1);
    int matricula = Integer.parseInt(partes[0]);
    String nome = partes[1];
    // ...
}
```

`split(";", -1)` divide a linha; o `-1` mantém os campos vazios do fim (um aluno sem notas).

!!! warning "Cuidados com CSV"
    - Se um campo puder conter o **separador** (um nome com `;`), o arquivo quebra. Recuse esse caractere na entrada ou use uma biblioteca de CSV.
    - Grave os números sempre do **mesmo jeito**. O projeto grava as notas com ponto (`String.format(Locale.ROOT, "%.1f", n)`) para que `Double.parseDouble` consiga ler de volta em qualquer computador.
    - Uma linha estragada não deve derrubar o programa: leia cada linha dentro de um `try`/`catch` e avise.

---

## Exercícios

### Básico (fixação)

Grave num arquivo `compras.txt` três itens de uma lista de compras, um por linha, e depois leia e mostre quantos itens há.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    Path p = Path.of("compras.txt");
    Files.write(p, List.of("arroz", "feijão", "café"), StandardCharsets.UTF_8);
    System.out.println(Files.readAllLines(p, StandardCharsets.UTF_8).size() + " itens"); // 3 itens
    ```
    Dentro de um `try`/`catch (IOException e)` (ou com `throws IOException` no `main`).

### Intermediário (aplicação)

Faça um “diário” que **acrescenta** uma linha com a data de hoje e um texto a cada execução, sem apagar as anteriores.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    String linha = java.time.LocalDate.now() + " - " + texto + System.lineSeparator();
    Files.writeString(Path.of("diario.txt"), linha, StandardCharsets.UTF_8,
            StandardOpenOption.CREATE, StandardOpenOption.APPEND);
    ```
    `CREATE` cria o arquivo na primeira vez; `APPEND` escreve no fim (`import java.nio.file.StandardOpenOption;`).

### Avançado (desafio)

Leia um CSV `produtos.csv` (`nome;preco`, com cabeçalho) e mostre o produto mais caro. Linhas com preço inválido devem ser avisadas e ignoradas.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    String maisCaro = null;
    double maior = -1;
    List<String> linhas = Files.readAllLines(Path.of("produtos.csv"), StandardCharsets.UTF_8);
    for (int i = 1; i < linhas.size(); i++) {
        try {
            String[] p = linhas.get(i).split(";");
            double preco = Double.parseDouble(p[1].replace(",", "."));
            if (preco > maior) { maior = preco; maisCaro = p[0]; }
        } catch (RuntimeException e) {
            System.out.println("Linha " + (i + 1) + " ignorada.");
        }
    }
    System.out.println(maisCaro == null ? "Nenhum produto válido." : maisCaro + " (" + maior + ")");
    ```
    O `catch (RuntimeException e)` pega tanto o preço inválido (`NumberFormatException`) quanto a linha sem `;` (`ArrayIndexOutOfBoundsException`).

---

## 💡 Resumo

- `Path.of(...)` para caminhos; `Files.write`/`writeString` para gravar; `readAllLines`/`readString` para ler.
- Sempre `StandardCharsets.UTF_8`; `IOException` precisa ser tratada ou declarada.
- CSV brasileiro: `;` como separador; recuse o separador nos dados; grave números de um jeito só.
- Leia cada linha num `try`/`catch` para uma linha ruim não derrubar tudo.

## ➡️ Próximo passo

Na **[aula 05](05_projeto_cadastro_csv.md)** o cadastro de alunos passa a salvar em CSV.
