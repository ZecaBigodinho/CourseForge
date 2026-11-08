# 01 — Montando e-mails com o Python

> **Curso:** Automação com Python  
> **Módulo:** 04 — E-mail, agendamento e boas práticas  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Entender as **regras** de quem envia e-mail automático (consentimento, quantidade, privacidade).
- Montar um e-mail com `EmailMessage`: remetente, destinatário, assunto, **texto**, versão **HTML** e **anexo**.
- Salvar o e-mail como **rascunho `.eml`** para conferir no Outlook ou no Thunderbird **antes** de enviar qualquer coisa.

## Pré-requisitos

- [Módulo 02](../modulo_02_planilhas/index.md): ambiente virtual e leitura de planilhas.

---

## Antes do código: as regras do e-mail automático

E-mail automático é a automação que mais pode **dar errado em público**: uma mensagem errada vai para 40 pessoas de uma vez e não volta. Por isso, além das [regras de segurança do curso](../modulo_01_arquivos_e_pastas/01_o_que_vale_automatizar.md#as-regras-de-seguranca):

| Regra | Por quê |
|---|---|
| **Só para quem espera receber** (alunos da sua turma, clientes que pediram) | E-mail em massa sem pedido é *spam*. Provedores bloqueiam a conta, e a LGPD exige uma base para usar o e-mail de alguém. |
| **Um e-mail por pessoa**, nunca todos no "Para" | Pôr 40 endereços no mesmo "Para" mostra o e-mail de todo mundo para todo mundo (vazamento de dado pessoal). |
| **Rascunho primeiro, servidor de teste depois, envio real por último** | Você confere o texto ([esta aula](#salvando-como-rascunho-eml)), depois o envio ([aula 02](02_servidor_de_teste.md)), e só então manda de verdade. |
| **Poucos e devagar** | Provedores como o Gmail limitam quantos e-mails uma conta pode mandar por dia e bloqueiam quem dispara rápido demais. |
| **Senha fora do código** | A senha do e-mail vai num arquivo `.env`, que nunca é compartilhado ([aula 03](03_env_e_configuracao.md)). |

!!! danger "Neste curso, nenhum e-mail sai do seu computador"
    Todos os endereços dos exemplos terminam em **`@example.com`**, um domínio reservado para exemplos: nada é entregue lá. E os envios das aulas vão para um **servidor de teste** que roda no próprio computador. Envio real só no fim, com autorização e depois de testar tudo.

## Instalando as bibliotecas do módulo

Com o ambiente virtual ativado:

```powershell
python -m pip install aiosmtpd==1.4.6 python-dotenv==1.2.1
```

O `email` e o `smtplib` (montar e enviar e-mails) já vêm com o Python. O **aiosmtpd** é o servidor de e-mail de teste ([aula 02](02_servidor_de_teste.md)) e o **python-dotenv** lê o arquivo `.env` ([aula 03](03_env_e_configuracao.md)).

## Os arquivos de treino

A planilha de treino tem os **trabalhos pendentes** de alguns alunos (dados inventados), com prazos contados a partir de **hoje**: um vence em 3 dias, outro em 10 e um já está **atrasado**. Dois alunos têm problema no e-mail, de propósito: um está **vazio** e outro foi **digitado errado**.

```python title="criar_treino_emails.py"
"""Cria os arquivos de treino do Módulo 04: planilha de pendências e um anexo."""
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook

TREINO = Path("treino_emails")

# Prazos contados a partir de hoje, para o lembrete sempre ter algo "para esta semana"
HOJE = date.today()
TRABALHOS = {
    "Pesquisa sobre golpes no WhatsApp": HOJE + timedelta(days=3),
    "Cartaz da campanha de segurança": HOJE + timedelta(days=10),
    "Resumo do capítulo 4": HOJE - timedelta(days=2),  # já passou do prazo
}
PENDENCIAS = [  # nome, e-mail (inventado, @example.com), trabalho
    ("Ana Souza", "ana.souza@example.com", "Pesquisa sobre golpes no WhatsApp"),
    ("Bruno Lima", "bruno.lima@example.com", "Pesquisa sobre golpes no WhatsApp"),
    ("Bruno Lima", "bruno.lima@example.com", "Resumo do capítulo 4"),
    ("Carla Mendes", "carla.mendes@example.com", "Cartaz da campanha de segurança"),
    ("Diego Rocha", "", "Pesquisa sobre golpes no WhatsApp"),  # sem e-mail cadastrado
    ("Elisa Prado", "elisa.prado@example", "Resumo do capítulo 4"),  # e-mail digitado errado
]


def main() -> None:
    if TREINO.exists():
        print(f"A pasta '{TREINO}' já existe. Apague-a se quiser começar do zero.")
        return
    TREINO.mkdir()
    livro = Workbook()
    aba = livro.active
    aba.title = "Pendências"
    aba.append(["Nome", "E-mail", "Trabalho", "Prazo"])
    for nome, email, trabalho in PENDENCIAS:
        aba.append([nome, email, trabalho, TRABALHOS[trabalho]])
        aba.cell(row=aba.max_row, column=4).number_format = "dd/mm/yyyy"
    livro.save(TREINO / "pendencias.xlsx")
    (TREINO / "orientacoes.txt").write_text(
        "Orientações para os trabalhos\n\n- Entregue pela plataforma da escola.\n"
        "- Dúvidas: procure o professor na aula.\n", encoding="utf-8")
    print(f"Arquivos de treino criados em: {TREINO.resolve()}")


if __name__ == "__main__":
    main()
```

## Montando um e-mail

```python title="montar_email.py"
from email.message import EmailMessage
from pathlib import Path

PASTA = Path("treino_emails")

msg = EmailMessage()
msg["From"] = "Professor <professor@example.com>"
msg["To"] = "Ana Souza <ana.souza@example.com>"
msg["Subject"] = "Lembrete: Pesquisa sobre golpes no WhatsApp"

# Versão em texto simples (todo programa de e-mail mostra)...
msg.set_content(
    "Olá, Ana!\n\n"
    "Lembrete: a Pesquisa sobre golpes no WhatsApp ainda não foi entregue.\n"
    "As orientações estão no anexo.\n\n"
    "Abraço,\nProfessor\n"
)
# ...e uma versão formatada (HTML), mostrada pelos programas que entendem
msg.add_alternative(
    "<p>Olá, <strong>Ana</strong>!</p>"
    "<p>Lembrete: a <strong>Pesquisa sobre golpes no WhatsApp</strong> ainda não foi entregue.</p>"
    "<p>As orientações estão no anexo.</p><p>Abraço,<br>Professor</p>",
    subtype="html",
)
anexo = PASTA / "orientacoes.txt"
msg.add_attachment(anexo.read_bytes(), maintype="text", subtype="plain", filename=anexo.name)

# Em vez de enviar, salva como rascunho .eml: dá para abrir e conferir no Outlook ou no Thunderbird
destino = PASTA / "saida" / "rascunho_ana.eml"
destino.parent.mkdir(exist_ok=True)
destino.write_bytes(bytes(msg))
print(f"Rascunho salvo: {destino}")
print(msg["Subject"], "|", len(bytes(msg)), "bytes")
```

```text
Rascunho salvo: treino_emails\saida\rascunho_ana.eml
Lembrete: Pesquisa sobre golpes no WhatsApp | 1396 bytes
```

| Parte | Comando |
|---|---|
| Cabeçalhos | `msg["From"]`, `msg["To"]`, `msg["Subject"]` (também `msg["Cc"]` e `msg["Reply-To"]`) |
| Texto simples | `msg.set_content(texto)` |
| Versão formatada | `msg.add_alternative(html, subtype="html")` |
| Anexo | `msg.add_attachment(bytes, maintype=..., subtype=..., filename=...)` |

!!! info "Texto e HTML juntos"
    O e-mail leva **as duas versões**. Programas que mostram formatação (Gmail, Outlook) exibem o HTML; os que não mostram (alguns relógios, leitores de tela, filtros de segurança) usam o texto. Sempre escreva as duas com o mesmo conteúdo.

!!! tip "Tipos de anexo"
    PDF: `maintype="application", subtype="pdf"`. Imagem JPG: `maintype="image", subtype="jpeg"`. Planilha Excel: `maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet"`. Quando não souber, `mimetypes.guess_type("arquivo.pdf")` (módulo `mimetypes`) descobre para você.

## Salvando como rascunho (.eml)

`bytes(msg)` é o e-mail **completo**, exatamente como seria enviado. Gravado num arquivo `.eml`, ele abre com **duplo clique** no Outlook, no Thunderbird ou no aplicativo Email do Windows, mostrando assunto, texto formatado e anexo. É a melhor forma de **conferir** antes de enviar: erros de português, nome errado, anexo faltando.

!!! warning "Abrir o .eml não envia nada"
    O programa de e-mail só **mostra** o rascunho. Se você clicar em **Responder** ou **Encaminhar** ali, aí sim estará escrevendo um e-mail de verdade: só feche a janela.

---

## ⚠️ Erros comuns

- **Todos os destinatários no mesmo "Para"**: expõe os e-mails de todo mundo. Um e-mail por pessoa.
- **Só a versão HTML**: alguns programas mostram o e-mail em branco. Use `set_content` (texto) **e** `add_alternative` (HTML).
- **`TypeError` no `add_attachment`**: faltou ler o arquivo como bytes (`read_bytes()`) ou informar `maintype`/`subtype`.
- **Testar com e-mails de colegas de verdade**: use `@example.com` até o envio real ser autorizado.

---

## Exercícios

### Básico (fixação)

Monte um e-mail com o assunto **"Reunião de pais — sábado, 9h"** e um texto curto, e salve como `treino_emails/saida/reuniao.eml`. Repare que o assunto tem acento e travessão.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    from email.message import EmailMessage
    from pathlib import Path

    msg = EmailMessage()
    msg["From"] = "Secretaria <secretaria@example.com>"
    msg["To"] = "Família da Ana <familia.ana@example.com>"
    msg["Subject"] = "Reunião de pais — sábado, 9h"
    msg.set_content("Bom dia! Lembramos da reunião de pais no sábado, às 9h, no auditório.\n\nSecretaria")

    destino = Path("treino_emails") / "saida" / "reuniao.eml"
    destino.parent.mkdir(exist_ok=True)
    destino.write_bytes(bytes(msg))
    ```

    Abra o `.eml` no bloco de notas: o assunto aparece "codificado" (`=?utf-8?q?Reuni=C3=A3o...`). Isso é normal: cabeçalhos de e-mail só aceitam letras simples, e o Python converte sozinho. No programa de e-mail, o assunto aparece certo.

### Intermediário (aplicação)

Acrescente ao e-mail da aula um **Reply-To** (`coordenacao@example.com`, para as respostas irem para a coordenação) e um **Cc** para `professor.auxiliar@example.com`. Salve como `rascunho_cc.eml` e confira os cabeçalhos.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    from email.message import EmailMessage
    from pathlib import Path

    msg = EmailMessage()
    msg["From"] = "Professor <professor@example.com>"
    msg["To"] = "Ana Souza <ana.souza@example.com>"
    msg["Cc"] = "professor.auxiliar@example.com"
    msg["Reply-To"] = "coordenacao@example.com"
    msg["Subject"] = "Lembrete: Pesquisa sobre golpes no WhatsApp"
    msg.set_content("Olá, Ana! A pesquisa ainda não foi entregue.\n\nProfessor")

    destino = Path("treino_emails") / "saida" / "rascunho_cc.eml"
    destino.parent.mkdir(exist_ok=True)
    destino.write_bytes(bytes(msg))
    print(msg["Cc"], "|", msg["Reply-To"])
    ```

    **Cc** (cópia) é visível para todos os destinatários; use para quem deve **acompanhar** o assunto. Para esconder destinatários existe o **Bcc** (cópia oculta), mas para avisos individuais o certo continua sendo um e-mail por pessoa.

### Avançado (desafio)

Gere um **rascunho para cada aluno** da `pendencias.xlsx` que tenha e-mail preenchido (uma linha = um e-mail, por enquanto), com o nome do trabalho no assunto. Conte quantos rascunhos foram criados.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from email.message import EmailMessage
    from pathlib import Path

    from openpyxl import load_workbook

    pasta = Path("treino_emails")
    saida = pasta / "saida" / "rascunhos_simples"
    saida.mkdir(parents=True, exist_ok=True)

    criados = 0
    planilha = load_workbook(pasta / "pendencias.xlsx")["Pendências"]
    for numero, (nome, email, trabalho, prazo) in enumerate(planilha.iter_rows(min_row=2, values_only=True), start=2):
        if not email:
            continue
        msg = EmailMessage()
        msg["From"] = "professor@example.com"
        msg["To"] = f"{nome} <{email}>"
        msg["Subject"] = f"Lembrete: {trabalho}"
        msg.set_content(f"Olá, {nome.split()[0]}! O trabalho '{trabalho}' vence em {prazo:%d/%m}.")
        (saida / f"linha_{numero}.eml").write_bytes(bytes(msg))
        criados += 1
    print(f"{criados} rascunhos")
    ```

    Saem **5** rascunhos (o Diego não tem e-mail). Repare em dois problemas que o projeto ([aula 05](05_projeto_lembrete.md)) resolve: o **Bruno** recebe **dois** e-mails (um por trabalho), e o e-mail da **Elisa** (`elisa.prado@example`, sem o `.com`) passou, embora esteja errado.

---

## 💡 Resumo

- E-mail automático: **só para quem espera**, **um por pessoa**, **poucos e devagar**, **senha fora do código**.
- `EmailMessage`: cabeçalhos, `set_content` (texto), `add_alternative` (HTML) e `add_attachment`.
- Grave `bytes(msg)` num `.eml` para **conferir** antes de enviar.
- Endereços `@example.com` nunca chegam a ninguém: use nos testes.

## ➡️ Próximo passo

**[02 — Enviando para um servidor de teste](02_servidor_de_teste.md)**: o envio de verdade, sem sair do computador.
