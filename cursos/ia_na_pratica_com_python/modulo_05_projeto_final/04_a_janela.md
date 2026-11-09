# 04 — A janela do atendente

> **Curso:** IA na prática com Python  
> **Módulo:** 05 — Projeto final  
> **Tempo estimado:** 1 h 30 min  

---

## 🎯 Objetivos

Ao final desta aula, você será capaz de:

- Montar a **janela** do atendente com o **CustomTkinter**: histórico, campo, botão e barra de status.
- Manter a janela **só como "cara"** do programa: a lógica continua no `atendente.py`, já testada.
- Mostrar ao atendente **o que precisa de atenção** (o motivo para revisar) sem esconder nada do cliente.
- Estender a janela com **subclasses**, sem mexer no arquivo original.

## Pré-requisitos

- [Aula 03](03_registro_e_linha_de_comando.md).
- O básico de CustomTkinter ([Python para Desktop, Módulo 02](../../python_para_desktop/modulo_02_interfaces_graficas/index.md)) e o pacote no ambiente virtual: `python -m pip install customtkinter==5.2.2`.

---

## Quem usa a janela

A janela é para quem trabalha no **balcão** da padaria: chega uma mensagem pelo telefone ou pelas redes, a pessoa cola na janela, lê a resposta sugerida e envia ao cliente. A barra de status mostra, para **ela** (não para o cliente), se aquele caso precisa de atenção e por quê.

```text
┌─ Padaria Pão Quente — Atendimento ─────────────────────┐
│ 🥖 Padaria Pão Quente                                   │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Cliente: Quanto custa a coxinha?                    │ │
│ │ Padaria: Coxinha: R$ 7,00 (unidade).                │ │
│ │                                                     │ │
│ │ Cliente: Sou celíaca, tem pão sem glúten?           │ │
│ │ Padaria: Obrigado pela mensagem! Vou passar para a  │ │
│ │ nossa equipe, que responde em breve.                │ │
│ └─────────────────────────────────────────────────────┘ │
│ [ Escreva a mensagem do cliente...         ] [ Enviar ] │
│ Modo: sem IA (regras) · 2 atendimentos · última:        │
│ revisar · ⚠ para revisar: dado sensível: saúde          │
└─────────────────────────────────────────────────────────┘
```

## O código

```python title="janela.py"
"""A janela do atendente (CustomTkinter): o histórico em cima, a mensagem embaixo."""
from pathlib import Path

import customtkinter as ctk

from pao_quente import atender_e_registrar


class JanelaAtendente(ctk.CTk):
    def __init__(self, cliente=None, modo: str = "sem IA (regras)", planilha: Path = Path("atendimentos.xlsx")):
        super().__init__()
        self.cliente, self.modo, self.planilha = cliente, modo, planilha
        self.title("Padaria Pão Quente — Atendimento")
        self.geometry("560x520")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="🥖 Padaria Pão Quente", font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, columnspan=2, padx=16, pady=(16, 4), sticky="w")
        self.historico = ctk.CTkTextbox(self, wrap="word", state="disabled")
        self.historico.grid(row=1, column=0, columnspan=2, padx=16, pady=8, sticky="nsew")
        self.campo = ctk.CTkEntry(self, placeholder_text="Escreva a mensagem do cliente...")
        self.campo.grid(row=2, column=0, padx=(16, 8), pady=8, sticky="ew")
        self.campo.bind("<Return>", lambda evento: self.enviar())
        ctk.CTkButton(self, text="Enviar", width=90, command=self.enviar).grid(row=2, column=1, padx=(0, 16), pady=8)
        self.status = ctk.CTkLabel(self, text=f"Modo: {modo} · 0 atendimentos", text_color="gray")
        self.status.grid(row=3, column=0, columnspan=2, padx=16, pady=(0, 12), sticky="w")
        self.atendimentos = 0
        self.campo.focus()

    def escrever(self, texto: str) -> None:
        self.historico.configure(state="normal")
        self.historico.insert("end", texto + "\n\n")
        self.historico.configure(state="disabled")
        self.historico.see("end")

    def enviar(self) -> dict | None:
        mensagem = self.campo.get().strip()
        if not mensagem:
            return None
        self.campo.delete(0, "end")
        self.escrever(f"Cliente: {mensagem}")
        saida = atender_e_registrar(mensagem, self.cliente, "janela", self.planilha)
        self.escrever(f"Padaria: {saida['resposta']}")
        self.atendimentos += 1
        aviso = f" · ⚠ para revisar: {saida['revisar']}" if saida["revisar"] else ""
        self.status.configure(
            text=f"Modo: {self.modo} · {self.atendimentos} atendimentos · última: {saida['categoria']}{aviso}")
        return saida
```

| Parte | O que faz |
|---|---|
| **`grid` com pesos** | A coluna 0 e a linha 1 (o histórico) **crescem** quando a janela aumenta; o campo e o botão ficam embaixo. |
| **`CTkTextbox` com `state="disabled"`** | Ninguém digita no histórico por engano. Para escrever, `escrever()` libera, insere e bloqueia de novo. |
| **`bind("<Return>", ...)`** | **Enter** envia, como num aplicativo de mensagens. |
| **`atender_e_registrar()`** | A mesma função do terminal e do lote: a janela **não sabe** se tem IA, nem como as respostas são montadas. |
| **`enviar()` devolve a saída** | Quem estender a janela pode usar o resultado (exercício avançado). |

Para abrir:

```text
> python pao_quente.py --simulado janela
```

Ou, com chave no `.env`, `python pao_quente.py janela`. A planilha registra o canal `janela`.

!!! info "Com a IA de verdade, a janela espera"
    Cada mensagem com IA leva um ou dois segundos (duas chamadas: classificar e responder). Durante esse tempo, a janela **não responde** a cliques. Para um balcão com uma mensagem por vez, isso é aceitável. Para resolver de vez, a chamada iria para uma *thread* separada, com o resultado voltando pela janela com `after()`, um assunto para depois do curso.

## Como testar uma janela

A janela tem pouca lógica de propósito: **tudo o que decide** (categoria, resposta, encomenda, registro) já está nos testes do pytest das aulas anteriores. Para a janela, um **roteiro de teste manual** curto, feito antes da entrega:

- [ ] Enter e o botão **Enviar** mandam a mensagem; campo vazio não faz nada.
- [ ] O histórico rola sozinho até a última mensagem e não aceita digitação.
- [ ] Um caso de revisar (por exemplo, "Sou celíaca...") mostra o **motivo** na barra de status.
- [ ] Uma encomenda aparece na aba **Encomendas** da planilha, com o canal `janela`.
- [ ] Aumentar e diminuir a janela não esconde o campo nem o botão.

---

## ⚠️ Erros comuns

- **Colocar regras dentro da janela** (calcular total, conferir resposta no `enviar()`): a regra fica sem teste e diferente do terminal.
- **Esquecer de bloquear o histórico** de novo depois de escrever: o atendente apaga mensagens sem querer.
- **`ModuleNotFoundError: No module named 'customtkinter'`**: instale no ambiente virtual do projeto (o mesmo onde rodam os testes).
- **Fechar a janela com a planilha aberta no Excel**: os atendimentos daquele momento não foram registrados; a barra de status avisa.

---

## Exercícios

### Básico (fixação)

Mostre o **horário** da padaria embaixo da barra de status, numa subclasse da janela (sem mexer no `janela.py`).

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```python
    import customtkinter as ctk

    from janela import JanelaAtendente
    from padaria import HORARIO


    class JanelaComHorario(JanelaAtendente):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            ctk.CTkLabel(self, text=f"Horário: {HORARIO}", text_color="gray").grid(
                row=4, column=0, columnspan=2, padx=16, pady=(0, 12), sticky="w")


    app = JanelaComHorario()
    app.mainloop()
    ```

    A linha 4 fica livre embaixo do status (linha 3). O `*args, **kwargs` repassa tudo para a janela original: a subclasse funciona com IA, sem IA e com outra planilha, sem repetir os parâmetros.

### Intermediário (aplicação)

Acrescente um botão **Limpar**, no canto de cima, que apaga o **histórico da tela** (não a planilha).

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```python
    import customtkinter as ctk

    from janela import JanelaAtendente


    class JanelaComLimpar(JanelaAtendente):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            ctk.CTkButton(self, text="Limpar", width=90, fg_color="gray", command=self.limpar).grid(
                row=0, column=1, padx=(0, 16), pady=(16, 4), sticky="e")

        def limpar(self) -> None:
            self.historico.configure(state="normal")
            self.historico.delete("1.0", "end")
            self.historico.configure(state="disabled")


    app = JanelaComLimpar()
    app.mainloop()
    ```

    O histórico é só o que está **na tela**; o registro de verdade continua na planilha. Por isso limpar a tela é seguro, e o botão não pergunta "tem certeza?". Apagar a planilha seria outra história.

### Avançado (desafio)

Mostre no **título da janela** a soma das encomendas anotadas desde que ela foi aberta, usando o que o `enviar()` devolve.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```python
    from janela import JanelaAtendente
    from padaria import preco_br


    class JanelaComTotal(JanelaAtendente):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.total = 0.0

        def enviar(self):
            saida = super().enviar()
            if saida and saida["encomenda"]:
                self.total += saida["encomenda"].total
                self.title(f"Padaria Pão Quente — encomendas: {preco_br(self.total)}")
            return saida


    app = JanelaComTotal()
    app.mainloop()
    ```

    Com "Quero 20 coxinhas para amanhã" e "Quero 10 sonhos para amanhã", o título mostra **R$ 205,00**. A subclasse **reaproveita** o `enviar()` original com `super()` e só acrescenta a conta; o Enter também usa a versão nova, porque o `bind` chama `self.enviar()`. O total vem da `Encomenda` (cardápio × quantidade), nunca da IA.

---

## 💡 Resumo

- A janela é só a **"cara"** do atendente: chama `atender_e_registrar()`, igual ao terminal e ao lote.
- O histórico fica bloqueado para digitação; a barra de status mostra o **motivo** dos casos para revisar.
- A lógica é testada pelo pytest; a janela, por um **roteiro manual** curto. Subclasses estendem a janela sem mexer no original.

## ➡️ Próximo passo

**[05 — Entrega e certificado](05_entrega_e_certificado.md)**.
