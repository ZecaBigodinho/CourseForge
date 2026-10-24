# Eventos e Interatividade (Binds, Funções de Callback e Variáveis de Controle)

## Objetivos

Neste capítulo, você aprenderá a:

- Compreender o modelo de eventos do Tkinter e o funcionamento do laço principal.
- Associar funções de callback a eventos do mouse e do teclado com o método `bind()`.
- Capturar e interpretar informações dos objetos Event, como posição do mouse, tecla pressionada e widget de origem.
- Diferenciar os níveis de vinculação: por instância, por classe e para todos os widgets.
- Utilizar variáveis de controle (`StringVar`, `IntVar`, `DoubleVar`, `BooleanVar`) para sincronizar dados entre o programa e os widgets de forma bidirecional.
- Empregar o método `trace()` para reagir a mudanças nessas variáveis.
- Construir interfaces dinâmicas que respondem instantaneamente às ações do usuário, sem necessidade de botões de ação.

## Pré-requisitos

Antes de prosseguir, você deve dominar:

- Criação de janelas com `Tk()` e `Toplevel`.
- Widgets básicos (`Label`, `Button`, `Entry`, `Text`) e seus principais atributos.
- Gerenciadores de layout `pack` e `grid`.
- Uso de `Frames` como contêineres.
- Funções em Python: definição, parâmetros e retorno.

Se necessário, revise os capítulos anteriores da série sobre Tkinter.

## Motivação

Até agora, nossas interfaces respondiam a cliques em botões, graças ao parâmetro `command`. Mas e se quisermos que algo aconteça quando o usuário pressiona Enter em um campo de texto? Ou quando ele passa o mouse sobre um botão? Ou, ainda, quando move um controle deslizante e um valor é atualizado instantaneamente? Essas interações mais ricas são possíveis através do sistema de eventos e callbacks do Tkinter.

Além disso, gerenciar manualmente o texto de um Entry ou o estado de um Checkbutton — lendo com `get()` e escrevendo com `delete`/`insert` — pode se tornar trabalhoso e propenso a erros. Para simplificar e tornar o código mais limpo, o Tkinter oferece as variáveis de controle, que mantêm automaticamente a interface e a lógica do programa em sincronia.

Neste capítulo, você sairá do básico "clique aqui, rotule ali" e construirá interfaces verdadeiramente interativas, que reagem a uma vasta gama de estímulos do usuário e mantêm dados atualizados com elegância.

## Conteúdo

### O laço de eventos e o modelo de callback

O Tkinter é orientado a eventos. Após a construção da interface, o método `mainloop()` entra em um laço infinito onde a biblioteca aguarda que algo aconteça — um clique, uma tecla, um movimento de mouse — e, quando ocorre, despacha esse evento para o widget apropriado, executando uma função de callback que você registrou previamente.

Essas funções são associadas a eventos específicos por meio do método `bind()`, disponível em todo widget.

### O método bind()

Sintaxe básica:

```python
widget.bind(sequencia, callback)
```

- **sequencia**: uma string que descreve o tipo de evento (ex.: `"<Button-1>"` para clique com botão esquerdo, `"<KeyPress-A>"` para tecla A, `"<Motion>"` para movimento do mouse).
- **callback**: a função Python a ser chamada, que deve aceitar um único argumento — o objeto `Event`.

Exemplo:

```python
import tkinter as tk

def ao_clicar(event):
    print(f"Clicou em x={event.x}, y={event.y}")

janela = tk.Tk()
janela.title("Evento de Clique")
janela.geometry("300x200")
janela.bind("<Button-1>", ao_clicar)  # associa clique à janela toda
janela.mainloop()
```

### O objeto Event

Quando um evento ocorre, o Tkinter cria um objeto Event com vários atributos úteis. Os mais comuns são:

| Atributo | Descrição |
|---|---|
| `x`, `y` | Coordenadas do mouse em relação ao widget que recebeu o evento. |
| `x_root`, `y_root` | Coordenadas em relação à tela. |
| `widget` | Referência ao widget que disparou o evento. |
| `keysym` | Símbolo da tecla pressionada (ex.: `"Return"`, `"a"`, `"F1"`). |
| `keycode` | Código numérico da tecla. |
| `char` | Caractere Unicode associado à tecla (vazio para teclas especiais). |
| `num` | Número do botão do mouse (1=esquerdo, 2=meio, 3=direito). |
| `type` | Tipo do evento (ex.: `"2"` para KeyPress). |

### Tipos de sequências de eventos

As sequências seguem o formato `"<MODIFICADOR-TIPO-DETALHE>"`. Exemplos:

- **Mouse:** `"<Button-1>"` (clique esquerdo), `"<ButtonRelease-3>"` (soltar botão direito), `"<Double-Button-1>"` (duplo clique), `"<Motion>"` (movimento), `"<Enter>"`, `"<Leave>"` (mouse entra/sai do widget).
- **Teclado:** `"<KeyPress-a>"` (tecla A minúscula), `"<KeyPress-A>"` (Shift+A), `"<KeyPress-Return>"` (Enter), `"<KeyPress-Escape>"` (Esc), `"<Control-c>"` (Ctrl+C), `"<Alt-F4>"`.
- **Combinações:** `"<Control-Shift-s>"`.

Podemos usar atalhos com `"<Return>"`, `"<Escape>"`, `"<F1>"` a `"<F12>"`, etc.

!!! tip "Use event.keysym para identificar teclas de forma legível"
    Dentro da função callback, `event.keysym` retorna uma string como `"Return"`, `"BackSpace"`, `"Tab"`, facilitando a lógica condicional.

### Níveis de vinculação

O Tkinter oferece três maneiras de associar eventos, com escopos diferentes:

1. **Por instância** (`widget.bind(...)`): afeta apenas aquele widget específico.
2. **Por classe** (`widget.bind_class("ClassName", ...)` ou `widget.bind_class("Entry", ...)`): afeta todos os widgets daquela classe.
3. **Para toda a aplicação** (`widget.bind_all(...)`): captura o evento em qualquer lugar da aplicação.

```python
# Faz com que todos os Entry chamem a função ao pressionar Return
janela.bind_class("Entry", "<Return>", lambda e: print("Enter pressionado em Entry"))
```

### Funções de callback com parâmetros extras

Muitas vezes queremos passar argumentos adicionais para a callback além do evento. Usamos `lambda`:

```python
def acao(event, mensagem):
    print(mensagem)

botao.bind("<Button-1>", lambda e: acao(e, "Botão clicado!"))
```

O `lambda` recebe o evento (obrigatório) e chama a função desejada com os parâmetros extras.

### Variáveis de controle Tkinter

As variáveis de controle são objetos especiais que atuam como uma camada de abstração entre a lógica do programa e os widgets. Elas permitem leitura e escrita de valores sem manipular diretamente os widgets, e notificam automaticamente a interface sobre mudanças.

Os principais tipos são:

| Classe | Tipo Python correspondente | Exemplo de criação |
|---|---|---|
| `StringVar` | str | `var = tk.StringVar(value="padrão")` |
| `IntVar` | int | `var = tk.IntVar(value=0)` |
| `DoubleVar` | float | `var = tk.DoubleVar(value=3.14)` |
| `BooleanVar` | bool | `var = tk.BooleanVar(value=False)` |

Essas variáveis são associadas a widgets através de parâmetros como `textvariable` (em Label, Entry), `variable` (em Checkbutton, Radiobutton), `value` (em Radiobutton), etc.

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Variáveis de Controle")

texto_var = tk.StringVar(value="Digite algo")
entrada = tk.Entry(janela, textvariable=texto_var)
entrada.pack(pady=10)

rotulo = tk.Label(janela, textvariable=texto_var)
rotulo.pack(pady=10)

# Ao digitar, o Label é atualizado automaticamente
janela.mainloop()
```

Aqui, `textvariable=texto_var` liga o Entry e o Label à mesma variável. Qualquer mudança no campo de entrada reflete instantaneamente no rótulo, sem uma linha de código extra.

!!! note "Vantagem das variáveis de controle"
    Elas eliminam a necessidade de chamar `entry.get()` repetidamente. Você pode ler o valor diretamente com `variavel.get()` e alterá-lo com `variavel.set(novo_valor)`, e todos os widgets vinculados são atualizados.

### Método trace(): reagindo a mudanças

As variáveis de controle permitem registrar funções de callback que são chamadas automaticamente quando o valor é alterado (por leitura, escrita ou exclusão). O método é `trace_add("write", callback)`, onde a callback recebe três argumentos: nome da variável, índice (se lista) e modo de acesso.

```python
def valor_mudou(*args):
    print(f"Novo valor: {texto_var.get()}")

texto_var.trace_add("write", valor_mudou)
```

!!! warning "A API de trace mudou no Python 3.6+"
    O método antigo era `trace("w", callback)`. Agora, utilize `trace_add("write", callback)`. Consulte a documentação se estiver mantendo código legado.

### Aplicações práticas

- **Validação em tempo real:** ao digitar um CPF, o texto é formatado automaticamente.
- **Habilitar/desabilitar botão:** um botão "Salvar" só fica ativo se um `StringVar` de e-mail não estiver vazio.
- **Sincronização entre múltiplos widgets:** um slider (`Scale`) e um campo numérico (`Spinbox`) podem compartilhar uma `IntVar` e manter o mesmo valor.

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Controle Sincronizado")

valor = tk.IntVar(value=50)

# Slider
tk.Scale(janela, from_=0, to=100, variable=valor, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20)

# Spinbox
tk.Spinbox(janela, from_=0, to=100, textvariable=valor).pack(pady=20)

# Label de monitoramento (usando trace)
tk.Label(janela, text="Valor atual:").pack()
rotulo_valor = tk.Label(janela, textvariable=valor)
rotulo_valor.pack()

janela.mainloop()
```

### Boas práticas

- Mantenha as callbacks curtas e delegue a lógica de negócio para funções separadas.
- Evite operações pesadas dentro de callbacks de eventos frequentes (`<Motion>`, `<KeyRelease>`), pois podem travar a interface. Para isso, use `after()`.
- Prefira variáveis de controle a manipular widgets diretamente sempre que possível; isso desacopla interface de lógica.
- Dê nomes descritivos às variáveis de controle, como `var_nome`, `var_idade`, `var_aceito_termos`.
- Use `lambda` com moderação; se a lógica for complexa, defina uma função nomeada para melhor legibilidade.
- Lembre-se de que bind no widget pai pode capturar eventos de filhos (propagação). Para restringir, verifique `event.widget`.

## Exemplos

??? example "Exemplo 1: Pintura livre com o mouse"
    === "Código"
        ```python
        import tkinter as tk

        janela = tk.Tk()
        janela.title("Desenho Livre")

        canvas = tk.Canvas(janela, bg="white", width=400, height=300)
        canvas.pack()

        def pintar(event):
            """Desenha um pequeno círculo onde o mouse estiver, enquanto arrastado."""
            x, y = event.x, event.y
            canvas.create_oval(x-2, y-2, x+2, y+2, fill="black", outline="")

        # Associa o movimento do mouse com botão esquerdo pressionado ao desenho
        canvas.bind("<B1-Motion>", pintar)

        # Clique inicial para desenhar um ponto parado
        canvas.bind("<Button-1>", pintar)

        janela.mainloop()
        ```

    === "Resultado"
        Uma janela com fundo branco onde o usuário pode desenhar livremente arrastando o mouse com o botão esquerdo pressionado.

    === "Explicação"
        O `<B1-Motion>` dispara quando o mouse se move com o botão esquerdo pressionado. A função `pintar` usa as coordenadas do evento para criar pequenos círculos no Canvas. O `<Button-1>` garante que um clique parado também marque um ponto. Esse exemplo mostra como eventos de mouse podem criar interações contínuas.

??? example "Exemplo 2: Campo de texto com limite de caracteres e contador"
    === "Código"
        ```python
        import tkinter as tk

        LIMITE = 50

        def ao_digitar(*args):
            """Atualiza o contador de caracteres e bloqueia excedente."""
            conteudo = texto_var.get()
            # Se ultrapassar o limite, corta o texto
            if len(conteudo) > LIMITE:
                texto_var.set(conteudo[:LIMITE])
            contador_var.set(f"{len(texto_var.get())}/{LIMITE}")

        janela = tk.Tk()
        janela.title("Limite de caracteres")

        texto_var = tk.StringVar()
        texto_var.trace_add("write", ao_digitar)

        contador_var = tk.StringVar(value=f"0/{LIMITE}")

        tk.Label(janela, text="Mensagem:").pack()
        entrada = tk.Entry(janela, textvariable=texto_var, width=60)
        entrada.pack(pady=5)
        tk.Label(janela, textvariable=contador_var).pack()

        janela.mainloop()
        ```

    === "Resultado"
        Um campo de entrada que impede o usuário de digitar mais de 50 caracteres. Abaixo, um rótulo mostra quantos caracteres foram usados (ex.: "12/50").

    === "Explicação"
        A variável `texto_var` é vinculada ao Entry. O método `trace_add("write", ao_digitar)` chama `ao_digitar` a cada modificação. Se o conteúdo ultrapassar o limite, cortamos com `texto_var.set(...)`. A variável `contador_var` é atualizada e reflete no Label. Note que não usamos bind no teclado, pois o trace na variável é mais confiável e funciona também com colagem (Ctrl+V).

??? example "Exemplo 3: Atalho de teclado global e menu de contexto"
    === "Código"
        ```python
        import tkinter as tk
        from tkinter import messagebox

        def salvar(event=None):
            messagebox.showinfo("Salvar", "Documento salvo (simulação)!")

        def mostrar_menu_contexto(event):
            menu_contexto.post(event.x_root, event.y_root)

        janela = tk.Tk()
        janela.title("Atalhos e Menu Contexto")
        janela.geometry("400x250")

        # Menu de contexto (clique direito)
        menu_contexto = tk.Menu(janela, tearoff=0)
        menu_contexto.add_command(label="Salvar", command=salvar)
        menu_contexto.add_command(label="Fechar", command=janela.destroy)

        # Atalho global: Ctrl+S
        janela.bind_all("<Control-s>", salvar)

        # Vinculando o menu de contexto ao botão direito
        janela.bind("<Button-3>", mostrar_menu_contexto)

        # Rótulo de instrução
        tk.Label(janela, text="Pressione Ctrl+S para Salvar.\nClique com botão direito para menu.").pack(expand=True)

        janela.mainloop()
        ```

    === "Resultado"
        Uma janela onde Ctrl+S exibe uma mensagem simulando salvamento. Um clique com o botão direito abre um menu contextual com opções "Salvar" e "Fechar".

    === "Explicação"
        `bind_all()` captura o atalho em qualquer widget da aplicação. Para o menu de contexto, criamos um Menu com `tearoff=0` (sem linha destacável) e o exibimos com `post(x, y)` nas coordenadas da tela (`x_root`, `y_root`). A função `salvar` aceita um argumento opcional `event` porque `bind_all` passa o objeto evento, e o comando do menu não passa nada — por isso o parâmetro padrão `None`.

## Exercícios

### Básico (fixação)

1. Crie uma janela com um Label. Faça com que, ao passar o mouse sobre o label (`<Enter>`), ele mude de cor de fundo (use `bg`) e, ao sair (`<Leave>`), volte à cor original.
2. Associe a tecla Escape à janela para fechá-la (use `janela.destroy` ou `janela.quit`).
3. Utilize um StringVar vinculado a um Entry e a um Label. Faça com que o Label mostre o texto do Entry sempre em maiúsculas, usando `trace_add`.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    import tkinter as tk

    janela = tk.Tk()
    janela.title("Eventos")

    # 1) Hover: muda a cor ao entrar e volta ao sair
    rotulo = tk.Label(janela, text="Passe o mouse aqui", bg="lightgray", padx=20, pady=10)
    rotulo.pack(padx=20, pady=10)
    rotulo.bind("<Enter>", lambda evento: rotulo.config(bg="lightblue"))
    rotulo.bind("<Leave>", lambda evento: rotulo.config(bg="lightgray"))

    # 2) Esc fecha a janela
    janela.bind("<Escape>", lambda evento: janela.destroy())

    # 3) Entry e Label ligados por StringVar — o Label mostra em maiúsculas
    texto = tk.StringVar()
    tk.Entry(janela, textvariable=texto).pack(padx=20, pady=5)
    espelho = tk.Label(janela, text="")
    espelho.pack(pady=(0, 10))


    def ao_mudar(*args):
        espelho.config(text=texto.get().upper())


    texto.trace_add("write", ao_mudar)

    janela.mainloop()
    ```


### Intermediário (aplicação)

Desenvolva um formulário de cadastro que contenha os campos "Nome" e "E-mail", ambos com Entry vinculados a StringVar. Abaixo, adicione um Checkbutton "Aceito os termos" vinculado a um BooleanVar. O botão "Cadastrar" deve permanecer desabilitado (`state="disabled"`) até que os dois campos estejam preenchidos e o checkbox marcado. Use `trace_add` nas três variáveis para atualizar o estado do botão em tempo real.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    import tkinter as tk

    janela = tk.Tk()
    janela.title("Cadastro")

    nome = tk.StringVar()
    email = tk.StringVar()
    aceito = tk.BooleanVar(value=False)

    tk.Label(janela, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(janela, textvariable=nome, width=30).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(janela, text="E-mail:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(janela, textvariable=email, width=30).grid(row=1, column=1, padx=5, pady=5)
    tk.Checkbutton(janela, text="Aceito os termos", variable=aceito).grid(
        row=2, column=0, columnspan=2, pady=5)


    def cadastrar():
        print(f"Cadastrado: {nome.get()} <{email.get()}>")


    botao = tk.Button(janela, text="Cadastrar", state="disabled", command=cadastrar)
    botao.grid(row=3, column=0, columnspan=2, pady=10)


    def validar(*args):
        pronto = nome.get().strip() and email.get().strip() and aceito.get()
        botao.config(state="normal" if pronto else "disabled")


    for variavel in (nome, email, aceito):
        variavel.trace_add("write", validar)

    janela.mainloop()
    ```


### Avançado (desafio)

Construa um pequeno jogo de "Clique no alvo":

- Um círculo (use Canvas) aparece em posição aleatória na tela.
- O jogador deve clicar no círculo. Quando acerta, o círculo muda para outra posição aleatória e um contador de acertos é incrementado.
- Se errar (clicar fora do círculo), um contador de erros é incrementado.
- Ao atingir 10 acertos ou 5 erros, o jogo termina e exibe uma mensagem final.
- Utilize `bind("<Button-1>", ...)` no Canvas, calcule se o clique foi dentro do círculo (distância do centro menor que o raio) e gerencie a lógica com variáveis de controle (`IntVar`) para os contadores.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    import random
    import tkinter as tk
    from tkinter import messagebox

    LARGURA, ALTURA, RAIO = 400, 300, 20

    janela = tk.Tk()
    janela.title("Clique no alvo")

    acertos = tk.IntVar(value=0)
    erros = tk.IntVar(value=0)

    placar = tk.Frame(janela)
    placar.pack(fill="x", padx=10, pady=5)
    tk.Label(placar, text="Acertos:").pack(side="left")
    tk.Label(placar, textvariable=acertos).pack(side="left", padx=(0, 15))
    tk.Label(placar, text="Erros:").pack(side="left")
    tk.Label(placar, textvariable=erros).pack(side="left")

    canvas = tk.Canvas(janela, width=LARGURA, height=ALTURA, bg="white")
    canvas.pack(padx=10, pady=10)
    alvo = {"x": 0, "y": 0}


    def mover_alvo():
        alvo["x"] = random.randint(RAIO, LARGURA - RAIO)
        alvo["y"] = random.randint(RAIO, ALTURA - RAIO)
        canvas.delete("alvo")
        canvas.create_oval(alvo["x"] - RAIO, alvo["y"] - RAIO, alvo["x"] + RAIO, alvo["y"] + RAIO,
                           fill="red", outline="", tags="alvo")


    def fim_de_jogo(mensagem):
        canvas.unbind("<Button-1>")
        messagebox.showinfo("Fim de jogo", f"{mensagem}\nAcertos: {acertos.get()} | Erros: {erros.get()}")


    def ao_clicar(evento):
        distancia = ((evento.x - alvo["x"]) ** 2 + (evento.y - alvo["y"]) ** 2) ** 0.5
        if distancia <= RAIO:
            acertos.set(acertos.get() + 1)
            if acertos.get() >= 10:
                fim_de_jogo("Parabéns, você venceu!")
                return
            mover_alvo()
        else:
            erros.set(erros.get() + 1)
            if erros.get() >= 5:
                fim_de_jogo("Fim de jogo: 5 erros.")


    canvas.bind("<Button-1>", ao_clicar)
    mover_alvo()
    janela.mainloop()
    ```


## Projeto Prático

### Editor de Texto com Status Dinâmico

Desenvolva um editor de texto simples usando o widget Text, com uma barra de status que exibe em tempo real:

- Número de caracteres.
- Número de palavras.
- Número de linhas.
- Posição atual do cursor (linha, coluna).

**Requisitos:**

- A janela deve conter uma Text que preenche quase toda a área, e um Frame inferior (Label ou Label dentro de um frame) para a barra de status.
- Utilize StringVar(s) para os valores exibidos na barra de status, atualizados via callbacks.
- Capture o evento `<KeyRelease>` na Text para recalcular caracteres, palavras e linhas.
- Capture o evento `<ButtonRelease-1>` ou `<KeyRelease>` para atualizar a posição do cursor (use `text.index(tk.INSERT)` que retorna `"linha.coluna"`).
- Adicione um menu "Arquivo" com opções "Novo" (limpa o texto) e "Sair". O menu deve ter atalhos (Ctrl+N, Ctrl+Q).
- Ao fechar a janela, pergunte se deseja salvar (simulação com messagebox).

**Estrutura recomendada:**

```python
import tkinter as tk
from tkinter import messagebox

class EditorApp:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Editor Simples")
        self.janela.geometry("600x400")

        # Variáveis de status
        self.var_caracteres = tk.StringVar(value="Caracteres: 0")
        self.var_palavras = tk.StringVar(value="Palavras: 0")
        self.var_linhas = tk.StringVar(value="Linhas: 1")
        self.var_posicao = tk.StringVar(value="Ln 1, Col 0")

        self.criar_widgets()
        self.criar_menu()
        self.configurar_eventos()

    def criar_widgets(self):
        # Área de texto
        self.texto = tk.Text(self.janela, wrap=tk.WORD, undo=True)
        self.texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Barra de status
        status_frame = tk.Frame(self.janela, bd=1, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(status_frame, textvariable=self.var_caracteres).pack(side=tk.LEFT, padx=5)
        tk.Label(status_frame, textvariable=self.var_palavras).pack(side=tk.LEFT, padx=5)
        tk.Label(status_frame, textvariable=self.var_linhas).pack(side=tk.LEFT, padx=5)
        tk.Label(status_frame, textvariable=self.var_posicao).pack(side=tk.RIGHT, padx=5)

    def criar_menu(self):
        menubar = tk.Menu(self.janela)
        self.janela.config(menu=menubar)
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Novo", command=self.novo, accelerator="Ctrl+N")
        menu_arquivo.add_command(label="Sair", command=self.confirmar_sair, accelerator="Ctrl+Q")
        self.janela.bind_all("<Control-n>", lambda e: self.novo())
        self.janela.bind_all("<Control-q>", lambda e: self.confirmar_sair())

    def configurar_eventos(self):
        self.texto.bind("<KeyRelease>", self.atualizar_status)
        self.texto.bind("<ButtonRelease-1>", self.atualizar_posicao)
        self.janela.protocol("WM_DELETE_WINDOW", self.confirmar_sair)

    def atualizar_status(self, event=None):
        conteudo = self.texto.get("1.0", tk.END)
        # Último caractere é sempre \n, desconsideramos na contagem
        num_caracteres = len(conteudo) - 1 if conteudo.endswith("\n") else len(conteudo)
        palavras = len(conteudo.split())
        linhas = int(self.texto.index("end-1c").split(".")[0])
        self.var_caracteres.set(f"Caracteres: {num_caracteres}")
        self.var_palavras.set(f"Palavras: {palavras}")
        self.var_linhas.set(f"Linhas: {linhas}")
        self.atualizar_posicao()

    def atualizar_posicao(self, event=None):
        pos = self.texto.index(tk.INSERT)  # "linha.coluna"
        linha, coluna = pos.split(".")
        self.var_posicao.set(f"Ln {linha}, Col {coluna}")

    def novo(self):
        if self.texto.edit_modified():
            resposta = messagebox.askyesno("Novo", "Deseja salvar as alterações?")
            if resposta is None:
                return
        self.texto.delete("1.0", tk.END)
        self.texto.edit_modified(False)

    def confirmar_sair(self):
        if self.texto.edit_modified():
            resposta = messagebox.askyesno("Sair", "Deseja salvar antes de sair?")
            if resposta is None:
                return
        self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = EditorApp()
    app.iniciar()
```

**Desafios extras:**

- Implemente a funcionalidade de salvar e abrir arquivo reais (use `filedialog`).
- Adicione sublinhado, negrito e itálico usando tags no Text (`**`, `*`, `__`).
- Exiba o percentual de progresso da leitura (posição do scroll) na barra de status.

Este projeto consolida eventos de teclado, variáveis de controle e a criação de uma aplicação interativa e responsiva, típica de editores de texto reais.

## Resumo

Neste capítulo, você aprendeu que:

- O Tkinter é orientado a eventos e o `mainloop()` aguarda ações do usuário para despachar callbacks.
- O método `bind()` associa funções a eventos específicos do mouse e teclado, com diversas opções de sequência.
- O objeto `Event` fornece detalhes como coordenadas, tecla pressionada e widget fonte.
- Existem três níveis de vinculação: por instância, por classe e global (`bind_all`).
- As variáveis de controle (`StringVar`, `IntVar`, etc.) sincronizam dados entre widgets e programa de forma limpa, suportando `trace_add` para notificações em tempo real.
- A combinação de eventos e variáveis de controle permite criar GUIs altamente interativas e dinâmicas, sem a necessidade de poluir o código com manipulação manual de widgets.

Com essas habilidades, suas aplicações ganham em fluidez e profissionalismo, respondendo imediatamente a cada ação do usuário.

## Próximo Capítulo

No próximo capítulo, conheceremos o **CustomTkinter**, uma evolução visual que permitirá aplicar temas escuros, bordas arredondadas e designs modernos às suas aplicações, deixando-as com cara de sistemas profissionais atuais.
