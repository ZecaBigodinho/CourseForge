# Padrão de imagens das aulas

Regras para toda imagem que entra em uma aula. O teste `tests/test_imagens.py` confere as regras marcadas com ✔ automaticamente.

## Onde guardar

| Tipo | Pasta |
|---|---|
| Imagens de uma aula (capturas, esquemas) | `cursos/<curso>/<módulo>/assets/` |
| Imagens do curso inteiro (capa, ícones) | `cursos/<curso>/assets/` |
| Marca do site (logo, favicon) | `cursos/assets/` |

## Nome do arquivo

`<NN>_<descricao_curta>.webp` — `NN` é o número da aula; tudo em minúsculas, sem acentos e sem espaços.

Exemplo: `01_janela_paragrafo.webp` (aula 01, janela Parágrafo).

## Formato e tamanho

- ✔ **WebP** para capturas e fotos; **SVG** para desenhos e ícones. (PNG e JPG não entram nas aulas.)
- ✔ Até **300 KB** por imagem.
- Largura de até **1400 px** (o site mostra no máximo cerca de 800 px; o restante serve para a ampliação).
- Sem dados pessoais na imagem: nomes, e-mails, fotos de pessoas reais, caminhos de pastas com o nome do usuário. Use arquivos e textos de **exemplo**.
- Office e programas em **português**, com o visual padrão (sem temas personalizados), para bater com o texto da aula.

## Como escrever na aula

Com legenda (o jeito preferido para capturas de tela):

```markdown
<figure markdown="span">
  ![Janela Parágrafo do Word com recuo de 1,25 cm e espaçamento 1,5](assets/01_janela_paragrafo.webp){ loading=lazy }
  <figcaption>A janela Parágrafo: recuo, espaçamento e alinhamento no mesmo lugar.</figcaption>
</figure>
```

- ✔ **Texto alternativo obrigatório** (entre os colchetes): descreve **o que a imagem mostra e por que importa**, em uma frase. Não comece com “Imagem de...”.
- ✔ **`{ loading=lazy }`** em toda imagem: ela só carrega quando o aluno chega nela.
- A **legenda** (`figcaption`) diz o que o aluno deve reparar.
- **Ampliação:** um clique abre a imagem grande (plugin `glightbox`). Para uma imagem que **não** deve ampliar, acrescente a classe `sem-zoom`: `{ loading=lazy .sem-zoom }`.
- A imagem **complementa** o texto: o passo a passo continua escrito (quem usa leitor de tela ou tem internet lenta não pode depender da imagem).

## Preparando uma captura

```bash
python ferramentas/midia/preparar_imagem.py captura.png cursos/pacote_office/modulo_01_word/assets/01_janela_paragrafo.webp
```

O script converte para WebP, reduz a largura para no máximo 1400 px, remove os metadados e avisa se passar de 300 KB. Para recortar uma parte da tela, use `--recorte esquerda,topo,direita,baixo` (em pixels da imagem original).
