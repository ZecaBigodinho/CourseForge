# 02 — Variáveis, tipos e operadores

> **Curso:** Java  
> **Módulo:** 01 — Fundamentos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Declarar variáveis com os tipos `int`, `double`, `boolean`, `char` e `String`.
- Usar constantes (`final`) e o `var`.
- Fazer contas com os operadores e entender a **divisão inteira**.
- Converter entre tipos (*casting*) e formatar números com `printf`.

## Pré-requisitos

- [Aula 01](01_primeiro_programa.md) deste módulo.

---

## Variáveis e tipos

Em Java, toda variável tem um **tipo**, que não muda depois:

```java
public class Variaveis {
    public static void main(String[] args) {
        String nome = "Ana";
        int idade = 17;
        double altura = 1.65;      // decimal com PONTO no código
        boolean matriculada = true;
        char turma = 'A';          // um caractere, com aspas simples

        System.out.println(nome + " tem " + idade + " anos e está na turma " + turma);
    }
}
```

| Tipo | Guarda | Exemplo |
|---|---|---|
| `int` | Inteiros (até cerca de 2 bilhões) | `17`, `-3` |
| `long` | Inteiros enormes | `7800000000L` |
| `double` | Números com casas decimais | `1.65`, `9.5` |
| `boolean` | Verdadeiro ou falso | `true`, `false` |
| `char` | Um caractere | `'A'` |
| `String` | Texto (com `S` maiúsculo) | `"Ana"` |

`int`, `double`, `boolean` e `char` são tipos **primitivos** (minúsculos). `String` é uma **classe**, por isso começa com maiúscula.

### Constantes e `var`

```java
final double MEDIA_APROVACAO = 7.0;   // final: não pode mudar
var turno = "manhã";                    // var: o Java descobre o tipo (String)
```

Por convenção, constantes têm nome em `MAIUSCULAS_COM_SUBLINHADO`. O `var` (Java 10+) só funciona com valor inicial e **continua tendo tipo fixo**: `turno = 5;` dá erro.

---

## Operadores

| Operador | Faz | Exemplo | Resultado |
|---|---|---|---|
| `+ - *` | Soma, subtração, multiplicação | `3 * 4` | `12` |
| `/` | Divisão | `7 / 2` | **`3`** (veja abaixo) |
| `%` | Resto da divisão | `7 % 2` | `1` |
| `++` / `--` | Soma ou subtrai 1 | `n++` | |
| `+=` | Soma e guarda | `total += 5` | |

!!! danger "A divisão inteira"
    Entre dois `int`, a divisão **descarta** a parte decimal: `7 / 2` dá `3`, e não `3.5`. Para ter decimais, pelo menos um lado precisa ser `double`: `7.0 / 2` ou `(double) soma / quantidade`. Esse é um dos erros mais comuns ao calcular médias.

---

## Conversões (*casting*)

```java
int soma = 29;
int quantidade = 4;
double media = (double) soma / quantidade;   // 7.25
int arredondada = (int) Math.round(media);   // 7

double preco = 18.9;
int inteiro = (int) preco;                   // 18: o (int) corta, não arredonda
```

- De `int` para `double` o Java converte sozinho (não perde nada).
- De `double` para `int` você precisa pedir com `(int)`, porque as casas decimais se perdem.
- Texto ➔ número: `Integer.parseInt("17")` e `Double.parseDouble("7.5")`.

---

## Mostrar números formatados

```java
double media = 7.25;
System.out.printf("Média: %.2f%n", media);
```

- `%.2f` mostra o número com **2 casas decimais**; `%d` mostra um inteiro; `%s`, um texto.
- `%n` pula linha.

!!! info "Vírgula ou ponto?"
    No código, decimal é sempre com **ponto** (`7.25`). Mas o `printf` segue o idioma do computador: num Windows em português, ele mostra **`7,25`**. Para forçar o ponto: `System.out.printf(java.util.Locale.US, "%.2f%n", media);`.

---

## Exercícios

### Básico (fixação)

Guarde o nome, o preço e a quantidade de um produto e mostre o total da compra com duas casas.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    String produto = "Caderno";
    double preco = 24.9;
    int quantidade = 3;
    System.out.printf("%d x %s = R$ %.2f%n", quantidade, produto, preco * quantidade);
    ```
    Num Windows em português, a saída é `3 x Caderno = R$ 74,70`.

### Intermediário (aplicação)

Quanto dá cada linha? Confira rodando.

```java
System.out.println(10 / 4);
System.out.println(10 / 4.0);
System.out.println(10 % 4);
System.out.println((int) 9.99);
```

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    `2` (divisão inteira), `2.5` (um lado é `double`), `2` (resto de 10 por 4) e `9` (o `(int)` corta as casas, não arredonda). O `println` de um `double` mostra com **ponto** (`2.5`); só o `printf` segue o idioma.

### Avançado (desafio)

Um aluno teve 7, 8, 6 e 9. Calcule a média com `int` para as notas e mostre a média correta (7,5), e não 7.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    int n1 = 7, n2 = 8, n3 = 6, n4 = 9;
    int soma = n1 + n2 + n3 + n4;          // 30
    double media = (double) soma / 4;      // 7.5
    System.out.printf("Média: %.1f%n", media);
    ```
    Sem o `(double)`, `30 / 4` daria `7`.

---

## 💡 Resumo

- Tipos: `int`, `long`, `double`, `boolean`, `char` e `String`; o tipo não muda.
- `final` para constantes; `var` descobre o tipo, mas ele continua fixo.
- **`int / int` descarta os decimais**: use `(double)` em médias.
- `printf("%.2f")` formata e segue o idioma do computador (vírgula no Brasil).

## ➡️ Próximo passo

Na **[aula 03](03_condicoes_e_lacos.md)** o programa passa a decidir e repetir.
