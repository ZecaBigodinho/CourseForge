# 02 — Streams

> **Curso:** Java  
> **Módulo:** 03 — Coleções, exceções e arquivos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Escrever **lambdas** (`n -> n * 2`) e referências a métodos (`Aluno::getNome`).
- Montar um **stream**: `filter`, `map`, `sorted`, `limit`.
- Terminar com `toList`, `count`, `sum`/`average` e `collect`.
- Agrupar e contar com `Collectors.groupingBy`.

## Pré-requisitos

- [Aula 01](01_colecoes.md) deste módulo.

---

## Lambdas

Uma **lambda** é uma função curta, sem nome, passada como valor (como as *arrow functions* do JavaScript):

```java
n -> n * 2                  // recebe n e devolve n * 2
(a, b) -> a + b             // dois parâmetros
p -> p.getPreco() > 10      // devolve true ou false
```

Uma **referência a método** é um atalho quando a lambda só chama um método: `p -> p.getNome()` vira `Produto::getNome`.

---

## O stream: uma linha de montagem

```java
import java.util.List;

public class Relatorio {
    record Produto(String nome, double preco, String categoria) {}

    public static void main(String[] args) {
        List<Produto> produtos = List.of(
            new Produto("Caderno", 24.9, "papelaria"),
            new Produto("Caneta", 2.5, "papelaria"),
            new Produto("Mochila", 89.9, "mochilas"),
            new Produto("Lápis", 1.5, "papelaria")
        );

        List<String> baratos = produtos.stream()
            .filter(p -> p.preco() < 10)          // fica com quem passa no teste
            .sorted((a, b) -> Double.compare(a.preco(), b.preco()))
            .map(Produto::nome)                   // transforma cada item
            .toList();                            // junta numa lista

        System.out.println(baratos);              // [Lápis, Caneta]
    }
}
```

1. `stream()` abre a linha de montagem sobre a lista (a lista original **não muda**).
2. As **operações intermediárias** (`filter`, `map`, `sorted`, `limit`) vão encaixadas uma depois da outra.
3. Uma **operação final** (`toList`, `count`, `sum`…) produz o resultado.

| Operação | Faz |
|---|---|
| `filter(cond)` | Fica só com os que passam |
| `map(f)` | Transforma cada item |
| `sorted(comparador)` | Ordena |
| `limit(n)` | Fica com os `n` primeiros |
| `toList()` | Junta numa lista (Java 16+) |
| `count()` | Conta |
| `mapToDouble(f).sum()` / `.average()` | Soma / média de números |
| `anyMatch(cond)` | Algum passa no teste? |

### Números: `mapToDouble`

```java
double total = produtos.stream().mapToDouble(Produto::preco).sum();
double media = produtos.stream().mapToDouble(Produto::preco).average().orElse(0);
System.out.println(total);                  // 118.80000000000001 (!)
System.out.printf("R$ %.2f%n", total);      // R$ 118,80
```

`average()` devolve um `OptionalDouble`, porque uma lista vazia não tem média; `orElse(0)` diz o que usar nesse caso.

!!! warning "Por que 118.80000000000001?"
    O `double` guarda os números em binário, e valores como `24.9` não têm representação exata: ao somar, aparecem “restos” minúsculos. Isso acontece em praticamente todas as linguagens (no JavaScript, `0.1 + 0.2` dá `0.30000000000000004`). Para **mostrar**, formate com `printf("%.2f")`. Para **dinheiro de verdade** (sistemas de loja, banco), o Java tem a classe `BigDecimal`, que faz contas decimais exatas.

### Ordenar com `Comparator`

```java
import java.util.Comparator;

produtos.stream()
    .sorted(Comparator.comparingDouble(Produto::preco).reversed())  // do mais caro ao mais barato
    .limit(2)
    .forEach(p -> System.out.println(p.nome()));                    // Mochila, Caderno
```

---

## Agrupar e contar

```java
import java.util.Map;
import java.util.stream.Collectors;

Map<String, Long> porCategoria = produtos.stream()
    .collect(Collectors.groupingBy(Produto::categoria, Collectors.counting()));

System.out.println(porCategoria); // {mochilas=1, papelaria=3} (a ordem pode variar)
```

!!! tip "Stream ou `for`?"
    Os dois resolvem. Streams deixam claro **o que** se quer (filtrar, ordenar, contar); o `for` é melhor quando há muitos passos com condições misturadas. Use o que ficar mais fácil de ler.

---

## Exercícios

### Básico (fixação)

Com a lista de produtos da aula, mostre os nomes de todos em letras maiúsculas.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    List<String> nomes = produtos.stream().map(p -> p.nome().toUpperCase()).toList();
    System.out.println(nomes); // [CADERNO, CANETA, MOCHILA, LÁPIS]
    ```

### Intermediário (aplicação)

Calcule o preço médio só da categoria `papelaria`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    double media = produtos.stream()
        .filter(p -> p.categoria().equals("papelaria"))
        .mapToDouble(Produto::preco)
        .average()
        .orElse(0);
    System.out.printf("%.2f%n", media); // 9,63
    ```
    (24,90 + 2,50 + 1,50) ÷ 3 = 9,63.

### Avançado (desafio)

Some o valor total de cada categoria (`Map<String, Double>`).

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    Map<String, Double> totalPorCategoria = produtos.stream()
        .collect(Collectors.groupingBy(Produto::categoria, Collectors.summingDouble(Produto::preco)));
    System.out.println(totalPorCategoria); // {mochilas=89.9, papelaria=28.9} (a ordem pode variar)
    ```
    `groupingBy` aceita um segundo argumento que diz **o que** calcular em cada grupo.

---

## 💡 Resumo

- Lambda: `p -> p.preco() > 10`; referência: `Produto::nome`.
- Stream: `stream()` + intermediárias (`filter`, `map`, `sorted`, `limit`) + uma final (`toList`, `count`, `sum`).
- `average()` devolve opcional: use `orElse`.
- `Collectors.groupingBy` agrupa; com `counting()` ou `summingDouble()`, resume cada grupo.

## ➡️ Próximo passo

Na **[aula 03](03_excecoes.md)** você trata os erros do programa.
