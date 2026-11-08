# 05 — Demonstração, entrega e certificado

> **Curso:** Automação com Python  
> **Módulo:** 05 — Projeto final  
> **Tempo estimado:** 1 h 30 min (mais a preparação da demonstração)  

---

## 🎯 Objetivos

Ao final desta aula, você terá:

- Um **README** que explica como instalar e usar a Secretaria.
- Feito a **demonstração** do projeto, seguindo um roteiro.
- Conferido o projeto com o **checklist final** e a **rubrica**.
- Entregue o projeto e concluído o curso **Automação com Python**. 🎉

## Pré-requisitos

- Aulas [01](01_planejando_a_secretaria.md) a [04](04_linha_de_comando_e_testes.md) deste módulo, com os testes passando.

---

## O README

Todo projeto que outra pessoa vai usar precisa de um **README.md** na pasta principal: o que é, como instalar, como usar. Modelo:

```markdown
# Secretaria automática

Gera o boletim, os certificados e os e-mails de resultado de uma turma a partir da planilha.

## Instalação

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install openpyxl==3.1.5 fpdf2==2.8.9 python-dotenv==1.2.1 aiosmtpd==1.4.6 pytest==8.4.2
    copy .env.example .env

## Uso

    python -m secretaria tudo caminho\da\turma.xlsx            (rascunhos, nada é enviado)
    python -m secretaria emails caminho\da\turma.xlsx --enviar (envia pelo servidor do .env)

Os arquivos ficam em saida\AAAA-MM-DD, junto com o secretaria.log.

## A planilha

Aba "Alunos": Matrícula, Nome, E-mail, 1º bim, 2º bim, 3º bim, 4º bim, Faltas.
Aba "Info": Turma, Curso, Ano, Aulas dadas, Responsável.

## Regras

Aprovado: média ≥ 6,0 e frequência ≥ 75%. Recuperação: média de 4,0 a 5,9.
Reprovado: média abaixo de 4,0 ou frequência abaixo de 75%. Pendente: alguma nota com problema.

## Testes

    python -m pytest testes
```

!!! tip "Escreva para quem não estava na aula"
    Imagine a secretária da escola, ou você daqui a seis meses: ela precisa conseguir instalar e usar **só lendo o README**. Peça para um colega seguir o README do zero, num computador diferente, e anote onde ele travou.

## O roteiro da demonstração (5 a 8 minutos)

| Tempo | Mostre |
|---|---|
| 1 min | **O problema:** quanto tempo a secretaria gasta fazendo isso à mão para uma turma (e para 10 turmas) |
| 1 min | **A planilha** de treino e os problemas de propósito |
| 2 min | **`python -m secretaria tudo ...`** rodando, e a pasta de saída: o boletim (abas Resumo e Problemas), um certificado, um rascunho de e-mail aberto |
| 1 min | **O envio** para o servidor de teste, com o outro terminal mostrando os e-mails chegando |
| 1 min | **Os testes** passando (`python -m pytest testes`) |
| 1 min | **Segurança:** o que o programa **não** faz sozinho (envio, decisões da escola) e onde fica a senha (`.env`, fora do Git) |
| 1 min | **Uma melhoria** que você fez além da aula (veja o checklist) |

!!! warning "Nada de dados reais na demonstração"
    Use a planilha de **treino**. Notas, e-mails e nomes de alunos de verdade são dados pessoais, muitas vezes de menores de idade. A demonstração não precisa deles para mostrar que o programa funciona.

## Checklist final

- [ ] `python -m secretaria tudo treino_secretaria/turma_1A.xlsx` roda sem erro e gera boletim, certificados, CSV de códigos, rascunhos e log.
- [ ] O envio para o **servidor de teste** funciona (`--enviar` com o `aiosmtpd` ligado) e o servidor desligado vira erro no log, não um traceback.
- [ ] `python -m pytest testes` passa.
- [ ] O `.env` está fora do Git (`.gitignore`) e existe um `.env.example`.
- [ ] O README explica instalação, uso, planilha, regras e testes.
- [ ] Você fez **pelo menos uma melhoria** própria. Ideias: a propriedade `aprovado` e a menção honrosa ([aula 02](02_pacote_e_dados.md)); a lista de aprovados em PDF ou as notas no e-mail da recuperação ([aula 03](03_documentos_e_emails.md)); a opção `--silencioso` ou o teste de envio ([aula 04](04_linha_de_comando_e_testes.md)); o organizador de pastas do Módulo 01 como comando `organizar`.

## Rubrica de avaliação

| Critério | Precisa melhorar | Bom | Excelente |
|---|---|---|---|
| **Funciona** | Algum comando quebra com a planilha de treino | Os quatro comandos funcionam | Funciona também com uma planilha nova criada pelo aluno, com outros problemas |
| **Regras corretas** | Médias ou situações erradas | Regras e arredondamento corretos | Regras corretas e cobertas por testes |
| **Segurança** | Senha no código ou envio sem `--enviar` | `.env`, rascunho por padrão, servidor de teste | Tudo isso, mais validação da configuração e mensagens claras |
| **Organização** | Um arquivo só, difícil de entender | Pacote com as partes separadas | Pacote organizado, funções pequenas, nomes claros |
| **Testes** | Sem testes | Os testes da aula passam | Testes novos para a melhoria feita |
| **README e demonstração** | Sem README ou demonstração confusa | README completo e demonstração no tempo | Um colega instalou e usou só pelo README |

!!! success "O que libera o certificado"
    O certificado do curso é liberado com a **entrega e a demonstração da Secretaria automática**: o projeto funcionando com a planilha de treino, os testes passando, o README e pelo menos uma melhoria própria.

!!! note "Para o professor"
    Na demonstração, peça ao aluno para rodar os testes **na hora** e para mostrar um e-mail chegando no servidor de teste. Uma boa pergunta final: *"O que você mudaria antes de usar isto com a planilha de verdade da escola?"* (Resposta esperada: testar com uma cópia, conferir os rascunhos, combinar com a coordenação e com as famílias, configurar o `.env` com uma conta institucional autorizada.)

---

## Parabéns! 🎉

Você terminou o curso **Automação com Python**. Agora você sabe:

- organizar, renomear e mover arquivos em lote, com **simulação**, sem sobrescrever e com **relatório para desfazer**;
- ler, limpar, calcular e gerar **planilhas** do Excel, arredondando do jeito certo;
- gerar **documentos do Word**, **PDFs**, **certificados**, **crachás** e preparar **imagens** em lote;
- montar e enviar **e-mails** com segurança, guardar **senhas no `.env`**, registrar **logs** e **agendar** scripts;
- juntar tudo num **pacote** com **linha de comando** e **testes automáticos**.

E, acima de tudo, as quatro regras de quem automatiza: **treinar numa cópia, simular antes, nunca apagar e guardar o que mudou**.

!!! tip "Continue estudando"
    - **[Python para Desktop](../../python_para_desktop/docs/index.md):** transforme a Secretaria num programa com **janelas** (CustomTkinter) e banco de dados.
    - **[Git e GitHub](../../python_para_desktop/modulo_05_git_github/index.md):** versione o projeto e publique o README.
    - **[Introdução à IA](../../introducao_a_ia/docs/index.md):** o próximo curso da trilha, **IA na prática com Python**, vai usar o que você aprendeu aqui.
    - **[Catálogo de cursos](../../catalogo.md).**
