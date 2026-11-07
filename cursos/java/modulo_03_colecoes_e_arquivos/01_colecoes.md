# 01 — ArrayList e HashMap

> **Curso:** Java  
> **Módulo:** 03 — Coleções, exceções e arquivos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Diferenciar **array** de **`List`** e usar `ArrayList`.
- Usar **`Map`**/`HashMap` para buscar por uma chave.
- Entender os *generics* (`List<String>`) e os tipos “embrulho” (`Integer`, `Double`).
- Escolher entre `List`, `Map` e `Set`.

## Pré-requisitos

- [Módulo 02](../modulo_02_poo/index.md) completo.

---

## Array × `List`

Um **array** tem tamanho fixo: `double[] notas = new double[4];`. Uma **`List`** cresce e diminui sozinha:

```java
import java.util.ArrayList;
import java.util.List;

public class Listas {
    public static void main(String[] args) {
        List<String> nomes = new ArrayList<>();
        nomes.add("Ana");
        nomes.add("Bruno");
        nomes.add("Carla");

        System.out.println(nomes.size());        // 3
        System.out.println(nomes.get(0));        // Ana
        System.out.println(nomes.contains("Bruno")); // true

        nomes.remove("Bruno");
        nomes.set(0, "Ana Souza");
        System.out.println(nomes);               // [Ana Souza, Carla]

        for (String n : nomes) {
            System.out.println("Olá, " + n);
        }
    }
}
```

| Método | Faz |
|---|---|
| `add(x)` / `add(i, x)` | Acrescenta no fim / na posição `i` |
| `get(i)` / `set(i, x)` | Lê / troca a posição `i` (começa em 0) |
| `remove(x)` ou `remove(i)` | Remove o objeto / a posição |
| `size()`, `isEmpty()`, `contains(x)` | Tamanho, se está vazia, se contém |

- `List<String>`: o **generic** entre `< >` diz o tipo dos itens. O compilador recusa `nomes.add(10)`.
- `new ArrayList<>()`: o `<>` vazio (*diamante*) repete o tipo da esquerda.
- Declare como `List` (a interface) e crie como `ArrayList` (a implementação): fica fácil trocar depois.

!!! info "`Integer`, `Double`: os embrulhos"
    Coleções só guardam **objetos**. Para números, use os tipos “embrulho”: `List<Integer>`, `List<Double>`. O Java converte sozinho entre `int` e `Integer` (*autoboxing*): `notas.add(7.5)` funciona numa `List<Double>`.

---

## `Map`: buscar por uma chave

Um **`Map`** guarda pares **chave ➔ valor**. Buscar pela chave é imediato, sem percorrer tudo:

```java
import java.util.HashMap;
import java.util.Map;

Map<String, Integer> estoque = new HashMap<>();
estoque.put("caderno", 40);
estoque.put("caneta", 120);
estoque.put("caderno", 35);              // a mesma chave: substitui

System.out.println(estoque.get("caneta"));         // 120
System.out.println(estoque.get("lápis"));          // null (não existe)
System.out.println(estoque.getOrDefault("lápis", 0)); // 0
System.out.println(estoque.containsKey("caderno"));   // true

for (Map.Entry<String, Integer> item : estoque.entrySet()) {
    System.out.println(item.getKey() + ": " + item.getValue());
}
```

| Tipo | Ordem ao percorrer |
|---|---|
| `HashMap` | Qualquer uma (não garantida) |
| `LinkedHashMap` | A ordem em que foi inserido |
| `TreeMap` | Ordem crescente das chaves |

---

## Qual coleção usar?

| Use | Quando |
|---|---|
| `List` | Uma sequência em ordem, que pode repetir (itens de um pedido) |
| `Map` | Buscar por uma chave única (aluno pela matrícula, preço pelo produto) |
| `Set` (`HashSet`) | Itens **sem repetição** (as turmas diferentes de uma escola) |

---

## Exercícios

### Básico (fixação)

Crie uma `List<Double>` com quatro notas, acrescente mais uma e calcule a média com um `for`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```java
    List<Double> notas = new ArrayList<>(List.of(7.0, 8.5, 6.0, 9.0));
    notas.add(10.0);
    double soma = 0;
    for (double n : notas) soma += n;
    System.out.println(soma / notas.size()); // 8.1
    ```
    `List.of(...)` cria uma lista **que não pode ser alterada**; por isso ela é passada para `new ArrayList<>(...)`, que pode.

### Intermediário (aplicação)

Conte quantas vezes cada palavra aparece em `"ana bruno ana carla bruno ana"`, usando um `Map<String, Integer>`.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```java
    Map<String, Integer> contagem = new HashMap<>();
    for (String p : "ana bruno ana carla bruno ana".split(" ")) {
        contagem.put(p, contagem.getOrDefault(p, 0) + 1);
    }
    System.out.println(contagem); // {ana=3, bruno=2, carla=1} (a ordem pode variar)
    ```

### Avançado (desafio)

Dada a lista de turmas `["1A", "2B", "1A", "3C", "2B"]`, mostre as turmas **sem repetição** e em ordem.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```java
    List<String> turmas = List.of("1A", "2B", "1A", "3C", "2B");
    Set<String> unicas = new TreeSet<>(turmas);
    System.out.println(unicas); // [1A, 2B, 3C]
    ```
    `TreeSet` tira as repetições **e** ordena (`import java.util.Set;` e `java.util.TreeSet;`).

---

## 💡 Resumo

- `List<T>` / `ArrayList`: sequência que cresce; `add`, `get`, `remove`, `size`.
- `Map<K, V>` / `HashMap`: busca pela chave; `put`, `get`, `getOrDefault`, `entrySet`.
- Coleções guardam objetos: `Integer`, `Double` (o Java converte sozinho).
- `Set` para itens sem repetição.

## ➡️ Próximo passo

Na **[aula 02](02_streams.md)** você processa coleções com streams.
