# Integração SQLite e Interface Gráfica

## Objetivos

Neste capítulo, você aprenderá a:

- Projetar a comunicação entre um banco de dados SQLite e uma interface gráfica Tkinter ou CustomTkinter.
- Utilizar o widget `Treeview` (do módulo `tkinter.ttk`) para exibir dados em formato tabular dentro da GUI.
- Carregar registros do banco de dados e preencher a Treeview de forma dinâmica.
- Coletar dados de formulários (`Entry`, `OptionMenu`, etc.) e executar operações CRUD (Inserir, Atualizar, Excluir) no SQLite.
- Tratar exceções do banco de dados sem travar a interface, exibindo mensagens amigáveis com `messagebox`.
- Manter a interface sempre sincronizada com o banco, atualizando a listagem após cada operação.
- Compreender a arquitetura em camadas (interface ↔ lógica de negócio ↔ banco de dados) para construir aplicações robustas e fáceis de manter.

## Pré-requisitos

Antes de iniciar, você deve dominar:

- Criação de interfaces com Tkinter ou CustomTkinter (`CTk`, `CTkFrame`, `CTkButton`, `CTkEntry`, `CTkLabel`).
- Gerenciadores de layout (`pack`, `grid`) e organização com frames.
- Uso de variáveis de controle (`StringVar`, `IntVar`) e eventos (`command`, `bind`).
- Fundamentos de SQLite e SQL: criação de tabelas, comandos `INSERT`, `SELECT`, `UPDATE`, `DELETE` e uso de parâmetros com `?`.
- O módulo `sqlite3` da biblioteca padrão e o padrão de conexão com `with`.
- Tratamento de exceções (`try`/`except`).

Caso algum desses tópicos ainda gere dúvidas, revise os capítulos anteriores, em especial Introdução a Banco de Dados com SQLite.

## Motivação

Ter um banco de dados resolvendo a persistência é excelente, mas de nada adianta se o usuário da sua aplicação precisar digitar comandos SQL em um console. O grande poder das aplicações desktop está na integração entre o backend (SQLite) e o frontend (Tkinter/CustomTkinter): o usuário preenche formulários gráficos, clica em botões e os dados são automaticamente salvos, consultados ou removidos do banco, com o resultado refletido instantaneamente na tela.

Neste capítulo, você vai aprender a construir essa ponte. Vamos transformar aquele módulo de funções SQL que você escreveu em uma interface viva, usando um dos widgets mais importantes para exibição de dados tabulares: a `Treeview`. Também abordaremos como proteger a interface contra falhas — afinal, um erro de banco de dados não pode quebrar a janela do programa; ele precisa ser capturado e exibido de forma elegante.

Ao final, você terá a base para criar sistemas completos de cadastro, como um CRUD de clientes, produtos, contatos ou qualquer outra entidade.

## Conteúdo

### Arquitetura em camadas (visão geral)

Em uma aplicação bem projetada, separamos responsabilidades:

- **Camada de persistência (`banco.py`)**: funções que executam SQL e retornam dados (dicionários, listas). Não sabem nada sobre a interface.
- **Camada de lógica / controle (`controle.py` ou dentro da própria classe da interface)**: faz a ponte, chamando funções do banco e atualizando a interface.
- **Camada de apresentação (`interface.py`)**: widgets, eventos e layout. Reage às ações do usuário e exibe resultados.

Neste capítulo, usaremos uma classe principal que já contém a lógica de controle, mas manteremos as funções de banco em um módulo separado, seguindo o princípio da modularização.

### Apresentando a Treeview

A `Treeview` faz parte do módulo `tkinter.ttk` (themed Tk). Ela é ideal para exibir listas de registros em formato de tabela, com colunas e linhas, suportando seleção, ordenação e scroll.

```python
import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.geometry("600x300")

# Criação da Treeview com colunas
colunas = ("id", "nome", "email")
tree = ttk.Treeview(janela, columns=colunas, show="headings")
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("email", text="E-mail")
tree.pack(fill="both", expand=True)

# Adiciona uma barra de rolagem
scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

janela.mainloop()
```

- `show="headings"` oculta a primeira coluna vazia padrão.
- `tree.heading("col", text="Título")` define o cabeçalho.
- `scrollbar` vinculada à Treeview permite rolar quando houver muitos registros.

!!! note "Treeview é do Tkinter clássico, não do CustomTkinter"
    O CustomTkinter não fornece uma tabela nativa. No entanto, você pode perfeitamente usar a `Treeview` do `ttk` dentro de um `CTkFrame`, pois ambos são widgets Tkinter compatíveis. O visual será um pouco mais "padrão", mas a funcionalidade é preservada.

### Inserindo dados na Treeview

Para preencher a tabela, primeiro limpamos os itens existentes e depois inserimos cada registro.

```python
def atualizar_tabela(dados):
    # Remove todos os registros atuais da Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Insere cada linha (dados é uma lista de tuplas ou dicionários)
    for registro in dados:
        tree.insert("", "end", values=registro)
```

Se dados for uma lista de dicionários, converta para tupla: `tuple(registro.values())`.

### Carregando dados do SQLite para a Treeview

Supondo um módulo `banco.py` com uma função `listar_clientes()` que retorna uma lista de dicionários:

```python
def listar_clientes():
    with sqlite3.connect("clientes.db") as conn:
        conn.row_factory = sqlite3.Row  # retorna dicionários-like
        cursor = conn.execute("SELECT id, nome, email FROM clientes")
        return [dict(row) for row in cursor.fetchall()]
```

Na interface, chamamos essa função e preenchemos a Treeview:

```python
def carregar_dados():
    try:
        clientes = banco.listar_clientes()
        # Limpa a treeview
        for item in tree.get_children():
            tree.delete(item)
        for cliente in clientes:
            tree.insert("", "end", values=(cliente["id"], cliente["nome"], cliente["email"]))
    except sqlite3.Error as e:
        messagebox.showerror("Erro no banco de dados", f"Não foi possível carregar os dados.\n{e}")
```

### Salvando dados do formulário no banco

O fluxo típico é:

1. Usuário preenche campos (ex.: `CTkEntry` para nome e email).
2. Clica no botão "Salvar".
3. Função de callback:
    - Coleta os valores com `.get()`.
    - Valida (campos não vazios, formatos).
    - Chama função do módulo de banco para inserir/atualizar.
    - Se sucesso, limpa o formulário, atualiza a Treeview e mostra mensagem de sucesso.
    - Se erro, captura exceção e exibe `messagebox.showerror`.

Exemplo com CustomTkinter:

```python
import customtkinter as ctk
from tkinter import messagebox
import banco  # nosso módulo

class App:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Clientes")
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        # Frame de formulário
        form = ctk.CTkFrame(self.janela)
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = ctk.CTkEntry(form)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form, text="E-mail:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_email = ctk.CTkEntry(form)
        self.entry_email.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkButton(form, text="Adicionar", command=self.adicionar).grid(row=0, column=4, padx=10)

        # Treeview (usando ttk)
        self.tree = ttk.Treeview(self.janela, columns=("id", "nome", "email"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("email", text="E-mail")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def adicionar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        if not nome or not email:
            messagebox.showwarning("Campos obrigatórios", "Preencha nome e e-mail.")
            return
        try:
            banco.inserir_cliente(nome, email)
            self.carregar_dados()
            self.entry_nome.delete(0, "end")
            self.entry_email.delete(0, "end")
            messagebox.showinfo("Sucesso", "Cliente adicionado.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "E-mail já cadastrado.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco", str(e))

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            clientes = banco.listar_clientes()
            for c in clientes:
                self.tree.insert("", "end", values=(c["id"], c["nome"], c["email"]))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados.\n{e}")
```

### Atualização e exclusão

Para atualizar um registro, geralmente selecionamos uma linha na Treeview, carregamos os valores nos campos, e um botão "Atualizar" executa o `UPDATE`. O ID do registro pode ser recuperado do item selecionado:

```python
def ao_selecionar(self, event):
    selecionado = self.tree.selection()
    if selecionado:
        item = self.tree.item(selecionado)
        valores = item["values"]  # (id, nome, email)
        self.id_atual = valores[0]
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, valores[1])
        self.entry_email.delete(0, "end")
        self.entry_email.insert(0, valores[2])
```

A exclusão pode ser feita com um botão "Excluir" que pega o ID da linha selecionada e chama `banco.excluir_cliente(id)`, com confirmação via `messagebox.askyesno`.

```python
def excluir(self):
    selecionado = self.tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um cliente para excluir.")
        return
    if messagebox.askyesno("Confirmar", "Deseja realmente excluir?"):
        id_cliente = self.tree.item(selecionado)["values"][0]
        try:
            banco.excluir_cliente(id_cliente)
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Cliente excluído.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", str(e))
```

!!! tip "Boas práticas de usabilidade"
    - Sempre confirme exclusões com `askyesno` ou `askokcancel`.
    - Limpe os campos e a seleção após operações bem-sucedidas.
    - Desabilite o botão "Atualizar" se nenhum item estiver selecionado.
    - Considere usar `tree.bind("<<TreeviewSelect>>", ao_selecionar)` para reagir à seleção.

### Tratamento de erros sem quebrar a interface

É crítico que nenhuma exceção não tratada chegue ao mainloop. Toda operação de banco deve estar dentro de `try`/`except`. As exceções específicas do SQLite (`sqlite3.IntegrityError`, `sqlite3.OperationalError`, `sqlite3.DatabaseError`) devem ser capturadas e convertidas em messagebox para o usuário. Isso mantém a interface estável e profissional.

Além disso, validações de campos (vazio, formato de e-mail) devem ser feitas antes de chamar o banco, reduzindo idas desnecessárias e prevenindo exceções.

### CustomTkinter + Treeview: convivência pacífica

Como mencionado, a Treeview pertence ao `tkinter.ttk`. Para usá-la em uma janela CTk, basta importá-la e adicioná-la normalmente. Você pode estilizar um pouco as cores da Treeview usando `ttk.Style()`, mas não espere que ela herde totalmente o tema do CustomTkinter. Uma alternativa é criar uma lista personalizada com `CTkScrollableFrame` e labels, mas a Treeview é muito mais prática e funcional, então a recomendação é mantê-la.

Exemplo de como estilizar:

```python
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
style.map("Treeview", background=[("selected", "#1f538d")])
```

Isso já dá um visual mais próximo do tema escuro.

### Boas práticas

- Mantenha o módulo de banco de dados completamente independente da GUI.
- Utilize `row_factory = sqlite3.Row` para acessar colunas por nome.
- Atualize a Treeview sempre após operações que alteram o banco.
- Forneça feedback visual: barra de status, contador de registros.
- Não bloqueie a interface com consultas longas; para grandes volumes, use `after()` e paginação (tópico avançado).

## Exemplos

??? example "Exemplo 1: CRUD completo de contatos (Tkinter clássico)"
    === "Código"
        ```python
        import tkinter as tk
        from tkinter import ttk, messagebox
        import sqlite3

        # Módulo de banco (funções)
        def criar_tabela():
            with sqlite3.connect("contatos.db") as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS contatos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        telefone TEXT NOT NULL UNIQUE
                    )
                """)

        def listar_contatos():
            with sqlite3.connect("contatos.db") as conn:
                conn.row_factory = sqlite3.Row
                return [dict(row) for row in conn.execute("SELECT * FROM contatos").fetchall()]

        def inserir_contato(nome, telefone):
            with sqlite3.connect("contatos.db") as conn:
                conn.execute("INSERT INTO contatos (nome, telefone) VALUES (?, ?)", (nome, telefone))

        def excluir_contato(id_contato):
            with sqlite3.connect("contatos.db") as conn:
                conn.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))

        # Interface
        class App:
            def __init__(self):
                self.janela = tk.Tk()
                self.janela.title("Contatos")
                self.janela.geometry("500x350")
                criar_tabela()
                self.criar_widgets()
                self.carregar_dados()

            def criar_widgets(self):
                frame = tk.Frame(self.janela)
                frame.pack(fill="x", padx=10, pady=10)

                tk.Label(frame, text="Nome:").grid(row=0, column=0, padx=5)
                self.entry_nome = tk.Entry(frame)
                self.entry_nome.grid(row=0, column=1, padx=5)

                tk.Label(frame, text="Telefone:").grid(row=0, column=2, padx=5)
                self.entry_fone = tk.Entry(frame)
                self.entry_fone.grid(row=0, column=3, padx=5)

                tk.Button(frame, text="Adicionar", command=self.adicionar).grid(row=0, column=4, padx=5)
                tk.Button(frame, text="Excluir", command=self.excluir).grid(row=0, column=5, padx=5)

                # Treeview
                colunas = ("id", "nome", "telefone")
                self.tree = ttk.Treeview(self.janela, columns=colunas, show="headings")
                self.tree.heading("id", text="ID")
                self.tree.heading("nome", text="Nome")
                self.tree.heading("telefone", text="Telefone")
                self.tree.pack(fill="both", expand=True, padx=10, pady=10)

            def carregar_dados(self):
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for contato in listar_contatos():
                    self.tree.insert("", "end", values=(contato["id"], contato["nome"], contato["telefone"]))

            def adicionar(self):
                nome = self.entry_nome.get().strip()
                fone = self.entry_fone.get().strip()
                if not nome or not fone:
                    messagebox.showwarning("Aviso", "Preencha todos os campos.")
                    return
                try:
                    inserir_contato(nome, fone)
                    self.carregar_dados()
                    self.entry_nome.delete(0, "end")
                    self.entry_fone.delete(0, "end")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Erro", "Telefone já cadastrado.")

            def excluir(self):
                selecionado = self.tree.selection()
                if not selecionado:
                    messagebox.showwarning("Seleção", "Escolha um contato.")
                    return
                if messagebox.askyesno("Confirmar", "Excluir contato?"):
                    id_contato = self.tree.item(selecionado)["values"][0]
                    excluir_contato(id_contato)
                    self.carregar_dados()

        if __name__ == "__main__":
            App().janela.mainloop()
        ```

    === "Resultado"
        Uma janela com campo de nome e telefone, botões Adicionar e Excluir, e uma tabela listando todos os contatos. Ao adicionar, os dados aparecem na tabela. Excluir remove após confirmação.

    === "Explicação"
        O banco é acessado por funções puras. A classe `App` cria a interface, conecta os botões e chama as funções de banco. A Treeview é recarregada após cada operação, mantendo a visualização atualizada. Tratamento de `IntegrityError` impede duplicação de telefone.

??? example "Exemplo 2: Atualização com seleção (CustomTkinter + Treeview)"
    === "Código"
        ```python
        import customtkinter as ctk
        from tkinter import ttk, messagebox
        import sqlite3

        # Funções de banco (mesmas do Exemplo 1, suponha existentes)

        class App:
            def __init__(self):
                ctk.set_appearance_mode("dark")
                self.janela = ctk.CTk()
                self.janela.title("Contatos Moderno")
                self.janela.geometry("600x400")

                # Variável para armazenar ID em edição
                self.id_edicao = None

                # Formulário
                form = ctk.CTkFrame(self.janela)
                form.pack(fill="x", padx=10, pady=10)
                ctk.CTkLabel(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
                self.entry_nome = ctk.CTkEntry(form)
                self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
                ctk.CTkLabel(form, text="Telefone:").grid(row=0, column=2, padx=5, pady=5)
                self.entry_fone = ctk.CTkEntry(form)
                self.entry_fone.grid(row=0, column=3, padx=5, pady=5)

                self.btn_salvar = ctk.CTkButton(form, text="Adicionar", command=self.salvar)
                self.btn_salvar.grid(row=0, column=4, padx=5, pady=5)
                self.btn_cancelar = ctk.CTkButton(form, text="Cancelar", command=self.cancelar_edicao, state="disabled")
                self.btn_cancelar.grid(row=0, column=5, padx=5, pady=5)

                # Treeview
                colunas = ("id", "nome", "telefone")
                self.tree = ttk.Treeview(self.janela, columns=colunas, show="headings")
                self.tree.heading("id", text="ID")
                self.tree.heading("nome", text="Nome")
                self.tree.heading("telefone", text="Telefone")
                self.tree.pack(fill="both", expand=True, padx=10, pady=10)
                self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)

                self.carregar_dados()

            def carregar_dados(self):
                for item in self.tree.get_children():
                    self.tree.delete(item)
                # listar_contatos() definida em outro módulo
                for c in listar_contatos():
                    self.tree.insert("", "end", values=(c["id"], c["nome"], c["telefone"]))

            def salvar(self):
                nome = self.entry_nome.get().strip()
                fone = self.entry_fone.get().strip()
                if not nome or not fone:
                    messagebox.showwarning("Aviso", "Campos obrigatórios.")
                    return
                try:
                    if self.id_edicao:  # Atualizar
                        with sqlite3.connect("contatos.db") as conn:
                            conn.execute("UPDATE contatos SET nome=?, telefone=? WHERE id=?",
                                         (nome, fone, self.id_edicao))
                        messagebox.showinfo("Sucesso", "Contato atualizado.")
                    else:  # Inserir
                        inserir_contato(nome, fone)
                        messagebox.showinfo("Sucesso", "Contato adicionado.")
                    self.carregar_dados()
                    self.limpar_formulario()
                except sqlite3.IntegrityError:
                    messagebox.showerror("Erro", "Telefone já cadastrado.")

            def ao_selecionar(self, event):
                selecionado = self.tree.selection()
                if selecionado:
                    valores = self.tree.item(selecionado)["values"]
                    self.id_edicao = valores[0]
                    self.entry_nome.delete(0, "end")
                    self.entry_nome.insert(0, valores[1])
                    self.entry_fone.delete(0, "end")
                    self.entry_fone.insert(0, valores[2])
                    self.btn_salvar.configure(text="Atualizar")
                    self.btn_cancelar.configure(state="normal")
                else:
                    self.cancelar_edicao()

            def cancelar_edicao(self):
                self.id_edicao = None
                self.limpar_formulario()
                self.btn_salvar.configure(text="Adicionar")
                self.btn_cancelar.configure(state="disabled")

            def limpar_formulario(self):
                self.entry_nome.delete(0, "end")
                self.entry_fone.delete(0, "end")
                self.tree.selection_remove(self.tree.selection())
        ```

    === "Resultado"
        A interface alterna entre modos de adição e edição. Ao selecionar um contato na tabela, os campos são preenchidos e o botão muda para "Atualizar". O botão "Cancelar" limpa e retorna ao modo de inserção.

    === "Explicação"
        Uma variável `self.id_edicao` controla se estamos inserindo ou atualizando. A seleção na Treeview dispara `ao_selecionar`, que popula os campos e habilita o modo edição. As operações de banco são as mesmas, mas o SQL executado depende do valor de `self.id_edicao`. A experiência do usuário fica mais fluida.

## Exercícios

### Básico (fixação)

1. Crie uma tabela `produtos` com campos `id`, `descricao` e `preco`. Monte uma interface Tkinter com `Treeview` que lista todos os produtos cadastrados. Adicione um botão "Atualizar Lista" que recarrega a tabela.
2. Adicione um formulário para inserir novos produtos. Ao clicar em "Salvar", insira no banco e atualize a Treeview. Trate `sqlite3.IntegrityError` caso a descrição seja duplicada (adicione `UNIQUE`).
3. Implemente a exclusão de um produto selecionado com confirmação.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    import sqlite3
    import tkinter as tk
    from tkinter import ttk, messagebox

    conn = sqlite3.connect("produtos.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE,
            preco REAL NOT NULL
        )""")

    janela = tk.Tk()
    janela.title("Produtos")

    # 2) Formulário
    form = tk.Frame(janela, padx=10, pady=10)
    form.pack(fill="x")
    tk.Label(form, text="Descrição:").grid(row=0, column=0, sticky="e")
    entrada_desc = tk.Entry(form, width=30)
    entrada_desc.grid(row=0, column=1, padx=5)
    tk.Label(form, text="Preço:").grid(row=0, column=2, sticky="e")
    entrada_preco = tk.Entry(form, width=10)
    entrada_preco.grid(row=0, column=3, padx=5)

    # 1) Treeview com a lista
    tree = ttk.Treeview(janela, columns=("id", "descricao", "preco"), show="headings", height=8)
    for coluna, titulo in (("id", "ID"), ("descricao", "Descrição"), ("preco", "Preço (R$)")):
        tree.heading(coluna, text=titulo)
    tree.column("id", width=40)
    tree.pack(fill="both", expand=True, padx=10)


    def atualizar_lista():
        tree.delete(*tree.get_children())
        for linha in conn.execute("SELECT id, descricao, preco FROM produtos ORDER BY descricao"):
            tree.insert("", "end", values=(linha[0], linha[1], f"{linha[2]:.2f}"))


    def salvar():
        descricao = entrada_desc.get().strip()
        try:
            preco = float(entrada_preco.get().replace(",", "."))
        except ValueError:
            messagebox.showwarning("Preço inválido", "Digite um número no preço.")
            return
        if not descricao:
            messagebox.showwarning("Descrição", "Preencha a descrição.")
            return
        try:
            with conn:
                conn.execute("INSERT INTO produtos (descricao, preco) VALUES (?, ?)", (descricao, preco))
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicado", f"Já existe um produto '{descricao}'.")
            return
        entrada_desc.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)
        atualizar_lista()


    # 3) Excluir com confirmação
    def excluir():
        selecao = tree.selection()
        if not selecao:
            messagebox.showinfo("Excluir", "Selecione um produto na lista.")
            return
        id_produto, descricao, _ = tree.item(selecao[0], "values")
        if messagebox.askyesno("Confirmar", f"Excluir '{descricao}'?"):
            with conn:
                conn.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
            atualizar_lista()


    botoes = tk.Frame(janela, pady=10)
    botoes.pack()
    tk.Button(botoes, text="Salvar", command=salvar).pack(side="left", padx=5)
    tk.Button(botoes, text="Excluir", command=excluir).pack(side="left", padx=5)
    tk.Button(botoes, text="Atualizar Lista", command=atualizar_lista).pack(side="left", padx=5)

    atualizar_lista()
    janela.mainloop()
    ```


### Intermediário (aplicação)

1. Desenvolva um CRUD de clientes (nome, e-mail, telefone) usando CustomTkinter para os formulários e botões, e Treeview para a listagem. Permita edição inline: ao selecionar um cliente, os dados vão para os campos e o botão "Salvar" se torna "Atualizar". Inclua validação de e-mail (presença de `@`) e telefone (apenas dígitos, no mínimo 10). Use um módulo separado para as funções de banco de dados.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python title="clientes_db.py"
    import sqlite3

    CAMINHO = "clientes.db"


    def conectar():
        conn = sqlite3.connect(CAMINHO)
        conn.row_factory = sqlite3.Row
        return conn


    def criar_tabela():
        with conectar() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    telefone TEXT NOT NULL
                )""")


    def listar():
        with conectar() as conn:
            return [dict(l) for l in conn.execute("SELECT * FROM clientes ORDER BY nome")]


    def inserir(nome, email, telefone):
        with conectar() as conn:
            conn.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                         (nome, email, telefone))


    def atualizar(id_cliente, nome, email, telefone):
        with conectar() as conn:
            conn.execute("UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                         (nome, email, telefone, id_cliente))


    def excluir(id_cliente):
        with conectar() as conn:
            conn.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    ```

    ```python title="app_clientes.py"
    import sqlite3
    import customtkinter as ctk
    from tkinter import ttk, messagebox

    import clientes_db as db


    class AppClientes:
        def __init__(self):
            db.criar_tabela()
            self.id_edicao = None
            self.janela = ctk.CTk()
            self.janela.title("Clientes")
            self.janela.geometry("640x420")

            form = ctk.CTkFrame(self.janela)
            form.pack(fill="x", padx=10, pady=10)
            self.campos = {}
            for coluna, rotulo in enumerate(("Nome", "E-mail", "Telefone")):
                ctk.CTkLabel(form, text=f"{rotulo}:").grid(row=0, column=coluna * 2, padx=5, pady=5)
                entrada = ctk.CTkEntry(form, width=140)
                entrada.grid(row=0, column=coluna * 2 + 1, padx=5, pady=5)
                self.campos[rotulo] = entrada

            botoes = ctk.CTkFrame(self.janela, fg_color="transparent")
            botoes.pack(fill="x", padx=10)
            self.btn_salvar = ctk.CTkButton(botoes, text="Salvar", command=self.salvar)
            self.btn_salvar.pack(side="left", padx=5)
            ctk.CTkButton(botoes, text="Excluir", command=self.excluir).pack(side="left", padx=5)
            ctk.CTkButton(botoes, text="Limpar", command=self.limpar).pack(side="left", padx=5)

            colunas = ("id", "nome", "email", "telefone")
            self.tree = ttk.Treeview(self.janela, columns=colunas, show="headings")
            for coluna, titulo in zip(colunas, ("ID", "Nome", "E-mail", "Telefone")):
                self.tree.heading(coluna, text=titulo)
            self.tree.column("id", width=40)
            self.tree.pack(fill="both", expand=True, padx=10, pady=10)
            self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)
            self.carregar()

        def valores(self):
            nome = self.campos["Nome"].get().strip()
            email = self.campos["E-mail"].get().strip()
            telefone = self.campos["Telefone"].get().strip()
            if not nome:
                raise ValueError("Informe o nome.")
            if "@" not in email:
                raise ValueError("E-mail inválido (falta o @).")
            if not telefone.isdigit() or len(telefone) < 10:
                raise ValueError("Telefone: apenas dígitos, com DDD (mínimo 10).")
            return nome, email, telefone

        def carregar(self, registros=None):
            self.tree.delete(*self.tree.get_children())
            for c in (registros if registros is not None else db.listar()):
                self.tree.insert("", "end", values=(c["id"], c["nome"], c["email"], c["telefone"]))

        def salvar(self):
            try:
                nome, email, telefone = self.valores()
                if self.id_edicao is None:
                    db.inserir(nome, email, telefone)
                else:
                    db.atualizar(self.id_edicao, nome, email, telefone)
            except ValueError as erro:
                messagebox.showwarning("Dados inválidos", str(erro))
                return
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicado", "Já existe um cliente com esse e-mail.")
                return
            self.limpar()
            self.carregar()

        def ao_selecionar(self, evento=None):
            selecao = self.tree.selection()
            if not selecao:
                return
            id_cliente, nome, email, telefone = self.tree.item(selecao[0], "values")
            self.limpar(manter_selecao=True)
            for rotulo, valor in zip(("Nome", "E-mail", "Telefone"), (nome, email, telefone)):
                self.campos[rotulo].insert(0, valor)
            self.id_edicao = int(id_cliente)
            self.btn_salvar.configure(text="Atualizar")  # edição inline

        def excluir(self):
            if self.id_edicao is None:
                messagebox.showinfo("Excluir", "Selecione um cliente na lista.")
                return
            if messagebox.askyesno("Confirmar", "Excluir o cliente selecionado?"):
                db.excluir(self.id_edicao)
                self.limpar()
                self.carregar()

        def limpar(self, manter_selecao=False):
            for entrada in self.campos.values():
                entrada.delete(0, "end")
            self.id_edicao = None
            self.btn_salvar.configure(text="Salvar")
            if not manter_selecao:
                self.tree.selection_remove(self.tree.selection())


    if __name__ == "__main__":
        app = AppClientes()
        app.janela.mainloop()
    ```


### Avançado (desafio)

1. Estenda o CRUD de clientes com um campo de pesquisa (`CTkEntry`) e um botão "Buscar". Ao digitar parte do nome, a Treeview deve exibir apenas os registros cujo nome contenha o termo (use `LIKE` na consulta SQL). Adicione também uma opção de ordenação: ao clicar no cabeçalho de uma coluna, a tabela deve ser ordenada (crescente/decrescente). Implemente a ordenação sem recarregar do banco (ou seja, ordenando a lista de dicionários localmente). Trate corretamente a alternância entre ordenações.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    # Em clientes_db.py — busca com LIKE (o % fica no parâmetro, nunca na string SQL):
    def buscar_por_nome(termo):
        with conectar() as conn:
            return [dict(l) for l in conn.execute(
                "SELECT * FROM clientes WHERE nome LIKE ? ORDER BY nome", (f"%{termo}%",))]


    # Em AppClientes — __init__ ganha a barra de busca e cabeçalhos clicáveis:
        def __init__(self):
            db.criar_tabela()
            self.id_edicao = None
            self.registros = []                       # o que está na tabela agora
            self.ordem = {"coluna": None, "desc": False}
            self.janela = ctk.CTk()
            self.janela.title("Clientes")
            self.janela.geometry("640x460")

            busca = ctk.CTkFrame(self.janela, fg_color="transparent")
            busca.pack(fill="x", padx=10, pady=(10, 0))
            self.entrada_busca = ctk.CTkEntry(busca, placeholder_text="Buscar por nome...")
            self.entrada_busca.pack(side="left", fill="x", expand=True, padx=(0, 5))
            ctk.CTkButton(busca, text="Buscar", width=80, command=self.buscar).pack(side="left")

            form = ctk.CTkFrame(self.janela)
            form.pack(fill="x", padx=10, pady=10)
            self.campos = {}
            for coluna, rotulo in enumerate(("Nome", "E-mail", "Telefone")):
                ctk.CTkLabel(form, text=f"{rotulo}:").grid(row=0, column=coluna * 2, padx=5, pady=5)
                entrada = ctk.CTkEntry(form, width=140)
                entrada.grid(row=0, column=coluna * 2 + 1, padx=5, pady=5)
                self.campos[rotulo] = entrada

            botoes = ctk.CTkFrame(self.janela, fg_color="transparent")
            botoes.pack(fill="x", padx=10)
            self.btn_salvar = ctk.CTkButton(botoes, text="Salvar", command=self.salvar)
            self.btn_salvar.pack(side="left", padx=5)
            ctk.CTkButton(botoes, text="Excluir", command=self.excluir).pack(side="left", padx=5)
            ctk.CTkButton(botoes, text="Limpar", command=self.limpar).pack(side="left", padx=5)

            colunas = ("id", "nome", "email", "telefone")
            self.titulos = dict(zip(colunas, ("ID", "Nome", "E-mail", "Telefone")))
            self.tree = ttk.Treeview(self.janela, columns=colunas, show="headings")
            for coluna in colunas:
                self.tree.heading(coluna, text=self.titulos[coluna],
                                  command=lambda c=coluna: self.ordenar(c))
            self.tree.column("id", width=40)
            self.tree.pack(fill="both", expand=True, padx=10, pady=10)
            self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar)
            self.carregar()

        def carregar(self, registros=None):
            self.registros = registros if registros is not None else db.listar()
            self.tree.delete(*self.tree.get_children())
            for c in self.registros:
                self.tree.insert("", "end", values=(c["id"], c["nome"], c["email"], c["telefone"]))

        def buscar(self):
            termo = self.entrada_busca.get().strip()
            self.carregar(db.buscar_por_nome(termo) if termo else None)  # vazio = lista completa

        def ordenar(self, coluna):
            """Ordena a lista que já está na tela, sem consultar o banco de novo."""
            desc = not self.ordem["desc"] if self.ordem["coluna"] == coluna else False
            self.ordem = {"coluna": coluna, "desc": desc}
            chave = (lambda c: c[coluna]) if coluna == "id" else (lambda c: str(c[coluna]).lower())
            self.carregar(sorted(self.registros, key=chave, reverse=desc))
            for c, titulo in self.titulos.items():   # seta no cabeçalho ativo
                seta = (" ▼" if desc else " ▲") if c == coluna else ""
                self.tree.heading(c, text=titulo + seta)
    ```


## Projeto Prático

### Sistema de Cadastro de Clientes com SQLite e CustomTkinter

Vamos construir um sistema completo de cadastro de clientes, integrando tudo o que aprendemos.

**Requisitos funcionais:**

- **Tela principal com:**
    - Formulário: campos nome, email, telefone, cidade e um `CTkOptionMenu` para plano (Básico, Premium, Empresarial).
    - Botões: Adicionar, Atualizar, Excluir, Limpar.
    - Área de busca: campo de texto e botão Buscar (filtra por nome ou email).
    - Treeview exibindo todos os clientes (ID, Nome, Email, Telefone, Cidade, Plano).
- **Funcionalidades:**
    - **Adicionar:** insere novo cliente no SQLite e atualiza a tabela.
    - **Atualizar:** ao selecionar um cliente na tabela, preenche o formulário e habilita o botão "Atualizar". Ao clicar, executa UPDATE.
    - **Excluir:** remove o cliente selecionado com confirmação.
    - **Limpar:** reseta o formulário e cancela modo de edição.
    - **Buscar:** filtra a Treeview conforme termo digitado; se campo vazio, mostra todos.
- **Banco de dados:** tabela `clientes` com colunas `id` (PK autoincrement), `nome`, `email` (UNIQUE), `telefone`, `cidade`, `plano`.
- **Tratamento de erros:** capturar `IntegrityError` para email duplicado, `OperationalError` para problemas de conexão, e validar campos obrigatórios antes de enviar ao banco.

**Arquitetura:**

```text
cadastro_clientes/
├── banco.py          # funções SQL (criar_tabela, inserir, listar, atualizar, excluir, buscar)
├── interface.py      # classe App com toda a GUI (CustomTkinter + Treeview)
└── main.py           # ponto de entrada
```

**Implementação passo a passo:**

1. **Módulo `banco.py`:**
    - Função `conectar()` retorna conexão com `clientes.db`.
    - `criar_tabela()` usando `CREATE TABLE IF NOT EXISTS`.
    - `inserir(nome, email, telefone, cidade, plano)` → insere e retorna True ou levanta exceção.
    - `listar_todos()` → retorna lista de dicionários.
    - `atualizar(id, dados_dict)` → executa UPDATE.
    - `excluir(id)` → executa DELETE.
    - `buscar(termo)` → usa `WHERE nome LIKE ? OR email LIKE ?`.

2. **Classe `App` em `interface.py`:**
    - No `__init__`, configura tema CustomTkinter, chama `criar_tabela()`, constrói a interface e carrega dados.
    - Cria frames: `form_frame` (campos e botões), `busca_frame` (campo busca e botão), `tree_frame` (Treeview + scrollbar).
    - Métodos: `adicionar`, `atualizar`, `excluir`, `limpar`, `buscar`, `carregar_dados`, `ao_selecionar`.
    - Variável `self.id_edicao` para controlar modo de edição.
    - Atualização dinâmica dos botões (habilitar/desabilitar Atualizar/Cancelar).

3. **Integração e tratamento de erros:**
    - Em cada operação (inserir, atualizar, excluir), envolver a chamada ao banco com `try`/`except`, exibindo `messagebox` em caso de erro e recarregando dados em caso de sucesso.
    - Validar campos: nome e email obrigatórios, email deve conter `@`.
    - Na busca, se o campo estiver vazio, recarregar todos; senão, chamar `banco.buscar(termo)`.

**Desafio extra (opcional):**

- Adicione um `CTkLabel` de status na parte inferior que mostre a quantidade de clientes cadastrados.
- Implemente a exportação da lista para CSV usando `filedialog.asksaveasfilename`.
- Substitua a Treeview por uma lista de cards (`CTkFrame` para cada cliente) usando `CTkScrollableFrame`, para um visual mais moderno.

Esse projeto é o coroamento dos seus estudos em persistência e interfaces gráficas, mostrando como construir uma aplicação desktop robusta, com separação clara entre backend e frontend, pronta para ser utilizada no mundo real.

## Resumo

Neste capítulo, você aprendeu que:

- A integração entre SQLite e Tkinter/CustomTkinter é feita conectando funções de banco a widgets e eventos.
- A `Treeview` do `ttk` é o widget padrão para exibir dados tabulares e pode ser usada junto com CustomTkinter.
- O fluxo típico de um CRUD é: coletar dados do formulário → validar → executar SQL → atualizar Treeview.
- Deve-se tratar exceções do SQLite com `try`/`except` e exibir mensagens amigáveis (`messagebox`), nunca permitindo que o erro trave a interface.
- O modo de edição pode ser implementado controlando um ID de referência e alterando o texto dos botões.
- A separação em camadas (banco de dados, lógica, interface) facilita a manutenção e evolução do sistema.

Com essas habilidades, você está apto a desenvolver sistemas completos de cadastro e controle, que vão muito além de simples scripts, oferecendo uma experiência profissional ao usuário final.


<!-- revisao-visual -->
!!! tip "Revisão visual: Banco de dados"
    Ficou alguma dúvida? A [Central de Revisão](../modulo_00_revisao_e_fixacao/09_sqlite_db_revisao.md) explica **banco de dados** com analogias do dia a dia, diagramas e os erros mais comuns — use antes dos exercícios ou para estudar para a prova.
