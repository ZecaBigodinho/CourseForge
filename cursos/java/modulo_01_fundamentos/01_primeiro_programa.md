# 01 — JDK e o primeiro programa

> **Curso:** Java  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Explicar o que são o **JDK**, o compilador `javac` e a **JVM**.
- Instalar o JDK 21 e conferir a instalação.
- Escrever, compilar e rodar o primeiro programa.
- Entender cada parte de `public static void main(String[] args)` e ler os erros do compilador.

## Pré-requisitos

- Saber abrir o terminal e navegar entre pastas.

---

## Como o Java funciona

```text
Ola.java  ──javac──►  Ola.class  ──java (JVM)──►  programa rodando
 (código)            (bytecode)
```

1. Você escreve o código num arquivo **`.java`**.
2. O compilador **`javac`** confere o código e gera um arquivo **`.class`** em *bytecode*.
3. A **JVM** (Máquina Virtual Java), chamada pelo comando **`java`**, roda o bytecode. A mesma `.class` roda em Windows, Linux ou macOS: é o “escreva uma vez, rode em qualquer lugar”.

O **JDK** (*Java Development Kit*) traz tudo isso: compilador, JVM e bibliotecas.

---

## Instalar o JDK 21

1. Baixe o JDK 21 (LTS) de uma distribuição gratuita, como o **Eclipse Temurin** ([adoptium.net](https://adoptium.net/)), e instale. Marque a opção de configurar o `PATH` (e o `JAVA_HOME`, se aparecer).
2. Abra um terminal **novo** e confira:

```bash
java -version
javac -version
```

As duas linhas devem mostrar a versão **21**.

!!! tip "VS Code"
    No VS Code, instale o **Extension Pack for Java** (da Microsoft). Ele mostra os erros enquanto você digita, completa o código e põe um botão **Run** em cima do `main`.

---

## O primeiro programa

Crie a pasta `curso-java` e, dentro dela, o arquivo `Ola.java`:

```java
public class Ola {
    public static void main(String[] args) {
        System.out.println("Olá, mundo!");
    }
}
```

Compile e rode no terminal, dentro da pasta:

```bash
javac Ola.java
java Ola
```

Saída: `Olá, mundo!`. Repare que `javac` recebe o **arquivo** (`Ola.java`) e `java` recebe o **nome da classe** (`Ola`, sem extensão).

!!! info "Atalho do Java moderno"
    Desde o Java 11, `java Ola.java` compila e roda de uma vez, sem gerar o `.class`. É ótimo para programas de um arquivo só, como os deste módulo.

### Peça por peça

| Parte | Significa |
|---|---|
| `public class Ola` | Todo código Java fica dentro de uma **classe**. O nome da classe pública deve ser **igual ao nome do arquivo** |
| `public static void main(String[] args)` | O **ponto de partida**: a JVM começa a rodar por aqui |
| `System.out.println(...)` | Escreve na tela e pula linha (`print` escreve sem pular) |
| `;` | Toda instrução termina com ponto e vírgula |
| `{ }` | Abrem e fecham blocos (classe, método) |

Por enquanto, aceite o `public static void` como “a fórmula do `main`”: cada palavra será explicada no Módulo 02.

---

## Acentos aparecendo errado no terminal

No Windows, “Olá” pode aparecer como `Ol�`. O código está certo: é o terminal usando outra codificação. Rode assim:

```bash
java -Dstdout.encoding=UTF-8 Ola.java
```

No terminal do VS Code, outra opção é rodar uma vez `chcp 65001` antes do `java`.

---

## Ler os erros do compilador

O `javac` responde em inglês. Três erros que todo mundo encontra:

```text
Ola.java:4: error: ';' expected
```

Faltou o **ponto e vírgula** no fim da linha 4 (o `^` na linha de baixo aponta onde).

```text
Ola.java:3: error: incompatible types: String cannot be converted to int
```

Você pôs um texto onde o tipo pedia um número inteiro (aula 02).

```text
Ola.java:5: error: cannot find symbol
  symbol:   method printn(String)
```

O compilador não achou `printn`: erro de digitação de `println`.

E um erro muito comum de quem está começando:

```text
Teste.java:1: error: class Ola is public, should be declared in a file named Ola.java
```

O nome do arquivo não bate com o nome da classe pública.

---

## Exercícios

### Básico (fixação)

Escreva um programa `Apresentacao.java` que mostre, em três linhas, seu nome, sua cidade e o curso que está fazendo.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    public class Apresentacao {
        public static void main(String[] args) {
            System.out.println("Ana Souza");
            System.out.println("São Paulo");
            System.out.println("Curso de Java");
        }
    }
    ```
    `java Apresentacao.java` (ou `javac Apresentacao.java` e `java Apresentacao`).

### Intermediário (aplicação)

Mostre as três informações na **mesma linha**, separadas por “ · ”, usando `print` e `println`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    System.out.print("Ana Souza");
    System.out.print(" · ");
    System.out.print("São Paulo");
    System.out.print(" · ");
    System.out.println("Curso de Java");
    ```
    `print` não pula linha; o último `println` pula. Também dá para juntar textos com `+`: `System.out.println("Ana Souza" + " · " + "São Paulo");`.

### Avançado (desafio)

Salve o `Ola.java` com o nome `ola.java` (minúsculo) e tente compilar. O que acontece? E se a classe não for `public`?

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Com `public class Ola` num arquivo `ola.java`, o `javac` acusa que a classe pública deve estar num arquivo chamado `Ola.java`: maiúsculas e minúsculas importam. Se você tirar o `public` (`class Ola`), compila, porque a regra do nome vale só para a classe **pública**. Mesmo assim, a convenção é: uma classe pública por arquivo, com o mesmo nome.

---

## 💡 Resumo

- `.java` ➔ `javac` ➔ `.class` (bytecode) ➔ `java` (JVM).
- JDK 21 instalado: `java -version` e `javac -version`.
- Classe pública com o nome do arquivo; o programa começa no `main`.
- `java Arquivo.java` roda direto; `-Dstdout.encoding=UTF-8` corrige acentos no terminal.

## ➡️ Próximo passo

Na **[aula 02](02_variaveis_e_tipos.md)** você guarda valores em variáveis.
