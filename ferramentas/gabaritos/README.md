# Teste dos gabaritos

Executa cada gabarito publicado nas aulas e confere o resultado. A **aula é a fonte única**: o código é lido do bloco `??? success "Gabarito — <nível>"` do próprio Markdown. Assim, o teste sempre usa a mesma versão que o aluno vê.

## Rodar

Na raiz do repositório:

```bash
python ferramentas/gabaritos/testar.py
```

- `testar.py poo banco_04`: só alguns arquivos de `casos/`.
- `testar.py -v`: mostra a saída de cada gabarito.
- Sai com código `1` se algum falhar, o que permite usar em CI.

Requisitos: as dependências do curso (`customtkinter==5.2.2`, `python-dotenv`, `matplotlib`) e uma **tela disponível**. Os testes de Interfaces e Banco abrem janelas por um instante.

## O que é conferido

| Casos | Verificação |
|---|---|
| `fundamentos_*` | O gabarito roda com a entrada de teste sem erro. Os resultados foram conferidos à mão quando o gabarito foi escrito. |
| `poo`, `interfaces_*`, `banco_*` | Além de rodar, o teste confere o resultado: digita nos campos, clica nos botões, gera eventos e verifica telas, arquivos e o banco. |
| `projetos_base` | Os projetos das aulas (Dashboard e Projeto de Dados) abrem sem erro. Os gabaritos que modificam esses projetos dependem deles. |

Não testado: o empacotamento com PyInstaller (Banco 04, Avançado 1), porque exige instalar o pacote e testar em outro computador.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `testar.py` | Roda os casos. |
| `extrair.py` | Lê gabaritos e blocos de código das aulas. |
| `casos/*.py` | Um arquivo por grupo de aulas: entrada de teste e verificações de cada gabarito. |
| `_gui.py` | Camada para testar janelas: o `mainloop()` volta na hora, as caixas de diálogo respondem sozinhas e há helpers como `clicar("Salvar")`. |
| `patch_classe.py` | Aplica os métodos de um gabarito sobre a classe da aula (usado quando o exercício modifica o projeto da aula). |
| `inserir.py` | Insere gabaritos novos nas aulas, no formato que o `extrair.py` lê. |

## Formato do gabarito na aula

Cada bloco de código do gabarito vira uma parte. O título do bloco diz o que ela é:

- **sem título**: código solto;
- `title="estoque.py"`: arquivo completo. Gabaritos com vários arquivos têm um bloco por arquivo, e o teste executa o último;
- `title="views/main_view.py — MainView"`: trecho com métodos a alterar naquele arquivo.

## Criar um gabarito novo

1. Escreva o rascunho num arquivo à parte, com `GABARITOS = [(aula, nível, código, entrada)]`.
2. Insira nas aulas: `python ferramentas/gabaritos/inserir.py cursos/python_para_desktop/<módulo> rascunho.py --aplicar`. Sem `--aplicar`, o comando só simula.
3. Em `casos/`, acrescente o caso com `G(aula, nível)` no lugar do código, a entrada e, se quiser conferir resultados, um `teste`.
4. Rode `testar.py`. Depois disso, o rascunho pode ser apagado.

Se uma aula mudar (por exemplo, o código do projeto), rode `testar.py` de novo. Os gabaritos que dependem daquele código acusam a quebra.
