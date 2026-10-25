# 02 — Funções essenciais: SE, CONT.SE, SOMASE e PROCX

> **Curso:** Pacote Office  
> **Módulo:** 02 — Excel  
> **Tempo estimado:** 2 h  

---

## Objetivos

Ao final desta aula, você será capaz de:

- Fazer a planilha **tomar decisões** com `SE`, `E`, `OU` e `SES`.
- **Contar**, **somar** e tirar **média** só do que atende a uma condição: `CONT.SE`, `SOMASE`, `MÉDIASE` e as versões com várias condições.
- **Buscar** um dado em uma tabela com `PROCX` — e reconhecer o `PROCV`, que você ainda vai encontrar em planilhas antigas.
- Tratar erros com `SEERRO` e usar funções simples de **texto** e **data**.

## Pré-requisitos

- [Aula 01](01_celulas_formulas_e_referencias.md): fórmulas, intervalos e referência absoluta (`$`).

---

## A planilha desta aula

Copie a tabela e cole no Excel na célula **A1**. Ela é usada nos exemplos e nos exercícios.

| Aluno | Turma | Nota 1 | Nota 2 | Faltas |
|---|---|---|---|---|
| Ana | A | 8 | 7 | 2 |
| Bruno | B | 5 | 4,5 | 6 |
| Carla | A | 9,5 | 9 | 0 |
| Diego | B | 6 | 7 | 3 |
| Elisa | A | 4 | 6 | 12 |
| Felipe | B | 7,5 | 8 | 1 |
| Gabriela | A | 6 | 5 | 4 |
| Henrique | B | 3 | 5,5 | 9 |

Em **F1** escreva `Média` e em **F2** `=MÉDIA(C2:D2)`; copie até F9.

---

## SE: a fórmula que decide

```text
=SE(teste; valor_se_verdadeiro; valor_se_falso)
```

- `=SE(F2>=6;"Aprovado";"Reprovado")` — se a média for 6 ou mais, escreve *Aprovado*; senão, *Reprovado*.
- Os **testes** usam os comparadores `=`, `<>` (diferente), `>`, `<`, `>=` e `<=`.
- **Texto vai entre aspas** (`"Aprovado"`); números e endereços, sem aspas.

### Mais de uma condição: E e OU

- `E(teste1; teste2)` é verdadeiro só se **todos** forem verdadeiros: `=SE(E(F2>=6;E2<=10);"Aprovado";"Reprovado")` — média boa **e** poucas faltas.
- `OU(teste1; teste2)` é verdadeiro se **pelo menos um** for: `=SE(OU(F2<6;E2>8);"Atenção";"")` — média baixa **ou** muitas faltas. As aspas vazias `""` deixam a célula em branco.

### Mais de dois resultados: SES

Em vez de um `SE` dentro do outro, use `SES`, que testa em ordem e para no primeiro verdadeiro:

```text
=SES(F2>=6;"Aprovado"; F2>=4;"Recuperação"; VERDADEIRO;"Reprovado")
```

O último par, `VERDADEIRO;"Reprovado"`, é o “senão”: vale para tudo o que não passou nos testes anteriores.

!!! tip "Leia a fórmula em voz alta"
    “**Se** a média for maior ou igual a 6, Aprovado; **se** for maior ou igual a 4, Recuperação; **senão**, Reprovado.” Se a frase faz sentido, a fórmula provavelmente está certa. A ordem importa: o teste mais exigente vem primeiro.

---

## Contar e somar com condição

| Função | O que faz | Exemplo |
|---|---|---|
| `CONT.SE(intervalo; critério)` | conta as células que atendem ao critério | `=CONT.SE(F2:F9;">=6")` |
| `SOMASE(intervalo; critério; intervalo_soma)` | soma uma coluna onde outra atende ao critério | `=SOMASE(B2:B9;"B";E2:E9)` |
| `MÉDIASE(intervalo; critério; intervalo_média)` | média com condição | `=MÉDIASE(B2:B9;"A";F2:F9)` |
| `CONT.SES(int1; crit1; int2; crit2; ...)` | conta com **várias** condições | `=CONT.SES(B2:B9;"A";F2:F9;">=6")` |
| `SOMASES(intervalo_soma; int1; crit1; ...)` | soma com várias condições | `=SOMASES(E2:E9;B2:B9;"A";F2:F9;"<6")` |

- O **critério** vai entre aspas quando tem comparador: `">=6"`, `"<>A"`.
- O critério pode vir de uma célula: `=CONT.SE(G2:G9;J2)` conta quantas vezes aparece o que está escrito em J2. Para juntar comparador e célula: `">="&J2`.

!!! warning "SOMASES começa pelo intervalo da soma"
    Em `SOMASE`, o intervalo da soma é o **último** argumento; em `SOMASES` (e `MÉDIASES`), é o **primeiro**. É a confusão mais comum com essas funções — a dica que aparece embaixo da célula mostra a ordem certa.

---

## Buscar dados: PROCX

`PROCX` procura um valor em uma coluna e devolve o que está na mesma linha de outra coluna:

```text
=PROCX(o_que_procurar; onde_procurar; o_que_devolver; [se_não_encontrar])
```

- `=PROCX("Diego";A2:A9;F2:F9)` ➔ **6,5** (a média do Diego).
- `=PROCX(J2;A2:A9;B2:B9;"Não encontrado")` ➔ a turma do aluno digitado em J2, ou a mensagem, se o nome não existir.
- Se o “o que devolver” tiver **várias colunas** (`F2:G9`), o resultado **se espalha** pelas células ao lado: média e situação de uma vez.

### E o PROCV?

Você vai ver muito `PROCV` em planilhas antigas e em tutoriais:

```text
=PROCV(J2;A2:G9;6;FALSO)
```

Ele procura na **primeira coluna** do intervalo e devolve a **6ª coluna**; o `FALSO` pede correspondência exata. Funciona, mas quebra se alguém inserir uma coluna no meio e não busca para a esquerda. No Microsoft 365, prefira `PROCX`.

!!! info "PROCX não existe em versões antigas"
    `PROCX` existe no Microsoft 365 e no Excel 2021 ou mais novo. Se a planilha for aberta em um Excel 2016 ou 2019, a célula mostra `#NOME?` — nesse caso, use `PROCV`.

---

## Tratar erros: SEERRO

`=SEERRO(fórmula; valor_se_der_erro)` mostra outra coisa no lugar do erro:

- `=SEERRO(F2/E2;0)` — se as faltas forem zero, mostra `0` em vez de `#DIV/0!`.
- `#N/D` é o erro de “não encontrado” das funções de busca. No `PROCX`, prefira o 4º argumento; em fórmulas antigas, você verá `=SEERRO(PROCV(...);"Não encontrado")`.

!!! warning "SEERRO esconde todos os erros"
    Ele também esconde os erros que você **deveria** ver, como um nome de função digitado errado. Use só quando souber qual erro espera.

---

## Texto e datas em uma olhada

| Função ou operador | O que faz | Exemplo ➔ resultado |
|---|---|---|
| `&` | junta textos | `=A2&" — Turma "&B2` ➔ `Ana — Turma A` |
| `ARRUMAR` | tira espaços sobrando | `=ARRUMAR("  Ana   Souza ")` ➔ `Ana Souza` |
| `PRI.MAIÚSCULA` | Iniciais Maiúsculas | `=PRI.MAIÚSCULA("ana souza")` ➔ `Ana Souza` |
| `MAIÚSCULA` | MAIÚSCULAS | `=MAIÚSCULA("ana")` ➔ `ANA` |
| `HOJE` | a data de hoje (muda sozinha) | `=HOJE()` |
| subtração de datas | dias entre duas datas | `=B2-A2` (formate o resultado como *Geral*) |
| `DATADIF` | idade em anos completos | `=DATADIF(A2;HOJE();"A")` |

!!! tip "Preenchimento Relâmpago"
    Para separar ou juntar textos sem fórmula, digite o primeiro resultado à mão na coluna ao lado (por exemplo, só o primeiro nome) e use *Dados* ➔ **Preenchimento Relâmpago**. O Excel descobre o padrão e completa a coluna.

---

??? note "Equivalentes gratuitos: LibreOffice Calc e Google Planilhas"
    | Função | LibreOffice Calc | Google Planilhas |
    |---|---|---|
    | `SE`, `E`, `OU`, `CONT.SE`, `SOMASE`, `MÉDIASE`, `SEERRO` | Mesmos nomes | Mesmos nomes |
    | `SES` | `SES` | `IFS` |
    | `PROCX` | `PROCX`, a partir do LibreOffice **24.8**; antes, use `PROCV` | `XLOOKUP` |
    | `PROCV` | `PROCV` | `PROCV` |
    | Preenchimento Relâmpago | Não tem; use fórmulas de texto | *Preenchimento inteligente* (sugere sozinho) |

    No Google Planilhas, algumas funções mais novas só têm o nome em inglês. Se um nome em português não for reconhecido, comece a digitar o nome em inglês e escolha da lista.

---

## ⚠️ Erros comuns

- **Esquecer as aspas no texto:** `=SE(F2>=6;Aprovado;Reprovado)` dá `#NOME?`. Texto sempre entre aspas.
- **Testes do `SES` na ordem errada:** começando por `F2>=4`, quem tirou 9 também cai em *Recuperação*. Do mais exigente para o menos.
- **Intervalos de tamanhos diferentes:** `=SOMASE(B2:B9;"B";E2:E8)` soma a coluna errada. Os intervalos devem ter o mesmo número de linhas.
- **Espaço escondido no nome:** `"Ana "` não é igual a `"Ana"`, e o `PROCX` não encontra. Use `ARRUMAR` na coluna de nomes.

---

## Exercícios

Use a planilha desta aula, com a coluna **F** (Média) já calculada.

### Básico (fixação)

1. Em **G1** escreva `Situação`. Em **G2**, mostre *Aprovado* se a média for 6 ou mais e *Reprovado* se não for; copie até G9.
2. Em **I1** escreva `Aprovados` e em **J1** conte quantos alunos foram aprovados.
3. Em **I2** escreva `Média da turma` e em **J2** calcule a média de todas as médias.

<!-- gabarito -->
??? success "Gabarito — Básico"
    1. **G2:** `=SE(F2>=6;"Aprovado";"Reprovado")` ➔ copie até G9.
    2. **J1:** `=CONT.SE(G2:G9;"Aprovado")` ➔ **4** (Ana, Carla, Diego e Felipe).
    3. **J2:** `=MÉDIA(F2:F9)` ➔ **6,3125** (com duas casas: 6,31).

    **Confira as médias:** 7,5 · 4,75 · 9,25 · 6,5 · 5 · 7,75 · 5,5 · 4,25.

### Intermediário (aplicação)

A escola mudou a regra. Agora:

- **Aprovado:** média 6 ou mais **e** no máximo 10 faltas;
- **Recuperação:** média 4 ou mais **e** no máximo 10 faltas;
- **Reprovado:** todos os outros casos.

1. Reescreva a fórmula da coluna **G** com a regra nova.
2. Monte um resumo: quantos alunos em cada situação; a média da turma **A** e da turma **B**; o total de faltas da turma **B**; e quantos alunos da turma **A** foram aprovados.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    1. **G2:** `=SES(E(F2>=6;E2<=10);"Aprovado";E(F2>=4;E2<=10);"Recuperação";VERDADEIRO;"Reprovado")` ➔ copie até G9.
    2. Resumo (escreva os rótulos na coluna I e as fórmulas na J):
        - `=CONT.SE(G2:G9;"Aprovado")` ➔ **4** · `=CONT.SE(G2:G9;"Recuperação")` ➔ **3** · `=CONT.SE(G2:G9;"Reprovado")` ➔ **1**
        - `=MÉDIASE(B2:B9;"A";F2:F9)` ➔ **6,81** · `=MÉDIASE(B2:B9;"B";F2:F9)` ➔ **5,81**
        - `=SOMASE(B2:B9;"B";E2:E9)` ➔ **19** faltas
        - `=CONT.SES(B2:B9;"A";G2:G9;"Aprovado")` ➔ **2** (Ana e Carla)

    **Repare na Elisa:** média 5, que daria Recuperação, mas 12 faltas — por isso fica *Reprovado*. Bruno, Gabriela e Henrique ficam em *Recuperação*.

### Avançado (desafio)

1. Monte uma **ficha de consulta**: em **L1** escreva `Aluno` e em **L2** digite um nome. Em **M2**, uma **única fórmula** deve mostrar a **média** e, na célula ao lado, a **situação** do aluno. Se o nome não existir, deve aparecer *Não encontrado*.
2. Em **H1** escreva `Alerta` e, em H2:H9, mostre *Atenção* para quem tem média abaixo de 6 **ou** mais de 8 faltas, deixando a célula **vazia** para os outros. Conte quantos alunos estão em alerta.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    1. **M2:** `=PROCX(L2;A2:A9;F2:G9;"Não encontrado")`. Como o retorno tem duas colunas (F e G), o resultado se espalha em **M2:N2**. Teste: `Diego` ➔ **6,5** e **Aprovado**; `Elisa` ➔ **5** e **Reprovado**; `Zeca` ➔ *Não encontrado*.
    2. **H2:** `=SE(OU(F2<6;E2>8);"Atenção";"")` ➔ copie até H9. Para contar: `=CONT.SE(H2:H9;"Atenção")` ➔ **4** (Bruno, Elisa, Gabriela e Henrique).

    **Se aparecer `#DESPEJAR!` na M2:** a célula N2 não está vazia, e o resultado não tem onde se espalhar. Apague o que estiver em N2.

---

## 💡 Resumo

- `SE(teste; se_sim; se_não)` decide; `E` exige tudo, `OU` aceita um; `SES` resolve vários resultados em ordem.
- `CONT.SE`, `SOMASE`, `MÉDIASE` trabalham com **uma** condição; as versões com **S** no fim aceitam várias.
- `PROCX` busca em qualquer direção e já trata o “não encontrado”; `PROCV` é o jeito antigo.
- Texto entre aspas; critérios com comparador também (`">=6"`).

## ➡️ Próximo passo

**[03 — Tabelas, gráficos e formatação condicional](03_tabelas_graficos_e_formatacao.md)**: transformar dados em uma tabela organizada, destacar o que importa com cores e mostrar tudo em um gráfico.
