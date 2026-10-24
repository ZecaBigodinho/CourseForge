# Projeto de Dados: Arquitetura Completa

## Objetivos

Ao final deste capítulo, você terá integrado Interfaces Gráficas, SQLite e `.env` em um projeto de arquitetura profissional — o ensaio geral para o Projeto Finalizador. Especificamente, você aprenderá a:

- Estruturar um projeto Python desktop em diretórios com separação de responsabilidades (Model, View, Controller).
- Aplicar o padrão MVC (Model-View-Controller) adaptado para aplicações com Tkinter/CustomTkinter.
- Utilizar CustomTkinter para uma interface moderna e responsiva.
- Implementar a camada de persistência com SQLite, centralizando o acesso a dados em classes de modelo.
- Carregar configurações sensíveis de um arquivo `.env` com `python-dotenv`, garantindo segurança e portabilidade.
- Tratar erros de forma global, protegendo a interface e fornecendo feedback claro ao usuário.
- Empacotar a aplicação final com PyInstaller, gerando um executável independente para distribuição.
- Compreender a importância da modularização e da organização de código para manutenção e escalabilidade.

## Pré-requisitos

Este capítulo assume que você domina todos os tópicos anteriores do curso, incluindo:

- Python básico e intermediário (variáveis, funções, coleções, strings, exceções).
- Tkinter e CustomTkinter (widgets, layouts, eventos, variáveis de controle).
- Banco de dados SQLite e módulo `sqlite3` (CRUD, parâmetros, integridade).
- Variáveis de ambiente com `python-dotenv` e arquivo `.env`.
- Manipulação de arquivos e diretórios (`pathlib`, `os`).
- Princípios de modularização e importação de módulos.
- Uso básico de terminal para instalação de pacotes e execução de scripts.

Se algum desses temas ainda não está consolidado, revise os capítulos correspondentes antes de prosseguir.

## Motivação

Projetos reais de software não são escritos em um único arquivo com centenas de linhas. À medida que a complexidade aumenta, torna-se impossível manter o código organizado sem uma arquitetura bem definida. Imagine um sistema de controle de estoque, clientes e vendas: misturar interface gráfica, consultas SQL e regras de negócio em um só lugar transforma qualquer alteração em um pesadelo.

A arquitetura Model-View-Controller (MVC) oferece uma solução testada e aprovada. Ela separa a aplicação em três camadas:

- **Model (Modelo)**: gerencia os dados e a lógica de negócio (banco de dados, validações, regras).
- **View (Visão)**: cuida da interface gráfica, exibindo informações e capturando ações do usuário.
- **Controller (Controlador)**: faz a ponte, recebendo eventos da View, acionando o Model e atualizando a View.

Essa separação facilita manutenção, testes e colaboração em equipe. Embora o MVC seja frequentemente associado a aplicações web, ele se adapta perfeitamente ao desktop. Neste capítulo, vamos implementar um sistema completo — um **Gerenciador de Produtos** — utilizando essa arquitetura, junto com CustomTkinter, SQLite, variáveis de ambiente e, ao final, empacotaremos o projeto em um executável. Será o coroamento do seu aprendizado.

## Conteúdo

### Estrutura de diretórios proposta

Organizaremos o projeto da seguinte forma:

```text
gerenciador_produtos/
├── app.py                  # Ponto de entrada da aplicação
├── config.py               # Carrega configurações do .env
├── .env                    # Variáveis de ambiente (NÃO versionado)
├── .env.example            # Template para desenvolvedores
├── .gitignore
├── requirements.txt        # Dependências do projeto
├── models/
│   ├── __init__.py
│   ├── database.py         # Conexão e inicialização do SQLite
│   └── produto.py          # Classe Produto e operações CRUD
├── views/
│   ├── __init__.py
│   ├── main_view.py        # Janela principal e layout
│   └── widgets.py          # Componentes reutilizáveis (se necessário)
├── controllers/
│   ├── __init__.py
│   └── produto_controller.py  # Controlador para operações de produto
└── utils/
    ├── __init__.py
    └── exceptions.py       # Exceções personalizadas
```

Essa estrutura pode ser expandida com novas entidades (clientes, vendas) seguindo o mesmo padrão. O arquivo `app.py` é mínimo: cria a aplicação e inicia o controlador principal.

### Camada de Configuração (config.py e .env)

Seguindo as boas práticas do capítulo anterior, centralizamos as configurações em `config.py`:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Caminho do banco de dados (com valor padrão)
DB_PATH = os.getenv("DB_PATH", "produtos.db")

# Tema da interface
TEMA = os.getenv("TEMA", "dark")
COR_TEMA = os.getenv("COR_TEMA", "blue")

# Título da aplicação
TITULO_APP = os.getenv("TITULO_APP", "Gerenciador de Produtos")

# Outras configurações podem ser adicionadas
```

O arquivo `.env` conterá:

```env
DB_PATH=produtos.db
TEMA=dark
COR_TEMA=dark-blue
TITULO_APP=Gerenciador de Produtos
```

E o `.env.example` orientará outros desenvolvedores.

### Camada Model: banco de dados e entidades

Em `models/database.py`, gerenciamos a conexão com SQLite e a criação das tabelas:

```python
# models/database.py
import sqlite3
from config import DB_PATH

def obter_conexao():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar_banco():
    """Cria as tabelas se não existirem."""
    with obter_conexao() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL CHECK(preco >= 0),
                quantidade INTEGER NOT NULL DEFAULT 0
            );
        """)
```

Em `models/produto.py`, definimos a classe `Produto` e as operações CRUD:

```python
# models/produto.py
from models.database import obter_conexao

class Produto:
    def __init__(self, id=None, nome="", descricao="", preco=0.0, quantidade=0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

    @classmethod
    def listar_todos(cls):
        """Retorna uma lista de objetos Produto."""
        with obter_conexao() as conn:
            rows = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
            return [cls(**dict(row)) for row in rows]

    @classmethod
    def buscar_por_id(cls, produto_id):
        with obter_conexao() as conn:
            row = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()
            return cls(**dict(row)) if row else None

    def salvar(self):
        """Insere ou atualiza o produto no banco."""
        with obter_conexao() as conn:
            if self.id:
                conn.execute(
                    "UPDATE produtos SET nome=?, descricao=?, preco=?, quantidade=? WHERE id=?",
                    (self.nome, self.descricao, self.preco, self.quantidade, self.id)
                )
            else:
                cursor = conn.execute(
                    "INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (?, ?, ?, ?)",
                    (self.nome, self.descricao, self.preco, self.quantidade)
                )
                self.id = cursor.lastrowid

    def excluir(self):
        """Remove o produto do banco."""
        if self.id:
            with obter_conexao() as conn:
                conn.execute("DELETE FROM produtos WHERE id = ?", (self.id,))
```

!!! note "Model com classe vs. dicionários"
    Utilizar uma classe enriquece a legibilidade e permite adicionar métodos de validação ou regras de negócio posteriormente. O uso de `@classmethod` para listar e buscar permite instanciar objetos diretamente.

### Camada View: interface com CustomTkinter

`views/main_view.py` contém a construção da janela principal, frames e widgets. A View **nunca acessa o banco de dados diretamente**; ela apenas exibe dados e captura eventos, delegando ao Controller.

```python
# views/main_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from config import TEMA, COR_TEMA, TITULO_APP

class MainView(ctk.CTk):
    def __init__(self):
        # Aparência vem do .env (via config.py) e precisa ser definida antes de criar a janela
        ctk.set_appearance_mode(TEMA)
        ctk.set_default_color_theme(COR_TEMA)
        super().__init__()
        self.title(TITULO_APP)
        self.geometry("800x500")
        self._criar_widgets()

    def _criar_widgets(self):
        # Frame de formulário
        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = ctk.CTkEntry(form, width=200)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form, text="Preço:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_preco = ctk.CTkEntry(form, width=100)
        self.entry_preco.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form, text="Qtd:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.entry_quantidade = ctk.CTkEntry(form, width=60)
        self.entry_quantidade.grid(row=0, column=5, padx=5, pady=5)

        # Botões (comandos serão vinculados pelo Controller)
        self.btn_adicionar = ctk.CTkButton(form, text="Adicionar")
        self.btn_adicionar.grid(row=0, column=6, padx=10, pady=5)
        self.btn_atualizar = ctk.CTkButton(form, text="Atualizar", state="disabled")
        self.btn_atualizar.grid(row=0, column=7, padx=5, pady=5)
        self.btn_excluir = ctk.CTkButton(form, text="Excluir", state="disabled")
        self.btn_excluir.grid(row=0, column=8, padx=5, pady=5)
        self.btn_limpar = ctk.CTkButton(form, text="Limpar")
        self.btn_limpar.grid(row=0, column=9, padx=5, pady=5)

        # Treeview para listagem
        colunas = ("id", "nome", "preco", "quantidade")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço (R$)")
        self.tree.heading("quantidade", text="Qtd")
        self.tree.column("id", width=50)
        self.tree.column("preco", width=100)
        self.tree.column("quantidade", width=80)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
```

A View expõe os widgets como atributos públicos para que o Controller possa acessá-los e associar eventos. Outra abordagem é usar métodos `set_controller` e chamar callbacks; aqui, faremos a ligação diretamente.

### Camada Controller: a orquestração

O `produto_controller.py` instancia a View e o Model, conecta eventos e implementa a lógica de interação:

```python
# controllers/produto_controller.py
from tkinter import messagebox
import sqlite3
from models.produto import Produto
from views.main_view import MainView

class ProdutoController:
    def __init__(self):
        self.view = MainView()
        self._conectar_eventos()
        self._atualizar_lista()
        self.id_edicao = None

    def _conectar_eventos(self):
        self.view.btn_adicionar.configure(command=self.adicionar)
        self.view.btn_atualizar.configure(command=self.atualizar)
        self.view.btn_excluir.configure(command=self.excluir)
        self.view.btn_limpar.configure(command=self.limpar)
        self.view.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _ao_selecionar(self, event):
        selecionado = self.view.tree.selection()
        if selecionado:
            valores = self.view.tree.item(selecionado)["values"]
            self.id_edicao = valores[0]
            self.view.entry_nome.delete(0, "end")
            self.view.entry_nome.insert(0, valores[1])
            self.view.entry_preco.delete(0, "end")
            self.view.entry_preco.insert(0, valores[2])
            self.view.entry_quantidade.delete(0, "end")
            self.view.entry_quantidade.insert(0, valores[3])
            self.view.btn_atualizar.configure(state="normal")
            self.view.btn_excluir.configure(state="normal")
            self.view.btn_adicionar.configure(state="disabled")
        else:
            self.limpar()

    def _validar_campos(self):
        nome = self.view.entry_nome.get().strip()
        preco_str = self.view.entry_preco.get().strip()
        qtd_str = self.view.entry_quantidade.get().strip()
        if not nome:
            raise ValueError("Nome do produto é obrigatório.")
        try:
            preco = float(preco_str)
            if preco < 0:
                raise ValueError
        except ValueError:
            raise ValueError("Preço deve ser um número positivo.")
        try:
            qtd = int(qtd_str)
            if qtd < 0:
                raise ValueError
        except ValueError:
            raise ValueError("Quantidade deve ser um número inteiro não negativo.")
        return nome, preco, qtd

    def adicionar(self):
        try:
            nome, preco, qtd = self._validar_campos()
            produto = Produto(nome=nome, preco=preco, quantidade=qtd)
            produto.salvar()
            self._atualizar_lista()
            self.limpar()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")
        except ValueError as e:
            messagebox.showerror("Erro de validação", str(e))
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", f"Não foi possível salvar.\n{e}")

    def atualizar(self):
        if not self.id_edicao:
            return
        try:
            nome, preco, qtd = self._validar_campos()
            produto = Produto(id=self.id_edicao, nome=nome, preco=preco, quantidade=qtd)
            produto.salvar()
            self._atualizar_lista()
            self.limpar()
            messagebox.showinfo("Sucesso", "Produto atualizado.")
        except ValueError as e:
            messagebox.showerror("Erro de validação", str(e))
        except sqlite3.Error as e:
            messagebox.showerror("Erro no banco de dados", str(e))

    def excluir(self):
        if not self.id_edicao:
            return
        if messagebox.askyesno("Confirmar", "Excluir o produto selecionado?"):
            try:
                produto = Produto(id=self.id_edicao)
                produto.excluir()
                self._atualizar_lista()
                self.limpar()
                messagebox.showinfo("Sucesso", "Produto excluído.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", str(e))

    def limpar(self):
        self.view.entry_nome.delete(0, "end")
        self.view.entry_preco.delete(0, "end")
        self.view.entry_quantidade.delete(0, "end")
        self.id_edicao = None
        self.view.btn_adicionar.configure(state="normal")
        self.view.btn_atualizar.configure(state="disabled")
        self.view.btn_excluir.configure(state="disabled")
        self.view.tree.selection_remove(self.view.tree.selection())

    def _atualizar_lista(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        for produto in Produto.listar_todos():
            self.view.tree.insert("", "end", values=(
                produto.id,
                produto.nome,
                f"{produto.preco:.2f}",
                produto.quantidade
            ))

    def iniciar(self):
        self.view.mainloop()
```

### Tratamento de erros centralizado

Acrescentamos uma camada extra de segurança capturando exceções específicas (`ValueError` para validação, `sqlite3.Error` para banco) e exibindo mensagens adequadas. Poderíamos também criar um decorador para capturar erros e logá-los, mas o padrão atual já é robusto.

### Empacotamento com PyInstaller

Para distribuir a aplicação como um executável, utilizamos o PyInstaller. Primeiro, instale:

```bash
pip install pyinstaller
```

Dentro da pasta do projeto, execute:

```bash
pyinstaller --onefile --windowed --name "GerenciadorProdutos" app.py
```

- `--onefile`: gera um único arquivo executável.
- `--windowed`: evita abrir uma janela de console no Windows.
- `--name`: define o nome do executável.

Isso criará uma pasta `dist` contendo o executável. No entanto, o arquivo `.env` não será incluído automaticamente. Precisamos de uma estratégia:

1. **Opção recomendada**: não empacotar o `.env`; em vez disso, solicitar as configurações na primeira execução ou usar valores padrão. O aplicativo pode criar um `.env` se não existir, com opções básicas.
2. **Incluir o `.env` como dado**: adicionar `--add-data ".env;."` no Windows ou `--add-data ".env:."` no Linux/macOS. Entretanto, isso incluiria as credenciais do desenvolvedor, o que é perigoso.

Para nosso caso, podemos modificar ligeiramente o `config.py` para aceitar a ausência do `.env` e carregar padrões, ou buscar o `.env` no diretório do executável. Uma solução elegante é:

```python
import sys
from pathlib import Path
from dotenv import load_dotenv

# Determina o caminho base (funciona tanto em desenvolvimento quanto no executável)
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")
```

E não empacotar o `.env`. Ao executar pela primeira vez, o programa pode mostrar uma janela de configuração ou criar um `.env` vazio.

No nosso projeto, vamos adotar a abordagem de não incluir o `.env` no pacote; os valores padrão em `config.py` garantem o funcionamento básico.

!!! tip "Testando o executável"
    Após gerar o executável, sempre teste em uma máquina limpa (ou máquina virtual) para verificar se todas as dependências foram incluídas. O PyInstaller geralmente detecta imports automaticamente, mas bibliotecas como `customtkinter` podem precisar de ajustes. Consulte a documentação do PyInstaller se houver problemas.

### Integrando tudo: o arquivo app.py

```python
# app.py
from models.database import inicializar_banco
from controllers.produto_controller import ProdutoController

if __name__ == "__main__":
    inicializar_banco()
    app = ProdutoController()
    app.iniciar()
```

Simples e claro: a criação da aplicação é delegada ao Controller, que por sua vez cria a View e gerencia as interações.

## Exemplos

??? example "Exemplo 1: Estrutura de diretórios e imports"
    === "Estrutura"
        ```text
        gerenciador_produtos/
        ├── app.py
        ├── config.py
        ├── models/
        │   ├── __init__.py
        │   ├── database.py
        │   └── produto.py
        ├── views/
        │   ├── __init__.py
        │   └── main_view.py
        └── controllers/
            ├── __init__.py
            └── produto_controller.py
        ```

    === "Explicação"
        Cada pacote (`models`, `views`, `controllers`) tem um arquivo `__init__.py` vazio para ser reconhecido como módulo Python. Os imports seguem a hierarquia: `controllers` importa de `views` e `models`; `models` importa de `config`; `views` não importa de `models` nem de `controllers`.

??? example "Exemplo 2: Validando e salvando produto"
    === "Código (trecho do controller)"
        ```python
        def adicionar(self):
            try:
                nome, preco, qtd = self._validar_campos()
                produto = Produto(nome=nome, preco=preco, quantidade=qtd)
                produto.salvar()
                # Atualiza a lista e limpa formulário...
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        ```

    === "Resultado"
        Se o campo "Preço" estiver vazio ou contiver letras, a validação levanta `ValueError` e uma caixa de erro é exibida ao usuário, sem travar a aplicação.

    === "Explicação"
        A validação ocorre no Controller, que conhece as regras de negócio (preço positivo, nome obrigatório). O Model recebe dados já validados.

??? example "Exemplo 3: Empacotamento com PyInstaller"
    === "Comando"
        ```bash
        pyinstaller --onefile --windowed --name "GerenciadorProdutos" app.py
        ```

    === "Saída esperada"
        O PyInstaller analisa os imports, coleta bibliotecas e gera `dist/GerenciadorProdutos.exe` (no Windows) ou executável equivalente no Linux/macOS.

    === "Explicação"
        `--windowed` suprime o console. Se houver erros de módulo não encontrado, podemos usar `--hidden-import`. Para CustomTkinter, geralmente não é necessário, mas podemos adicionar `--hidden-import customtkinter` por segurança.

## Exercícios

### Básico (fixação)

1. Reproduza a estrutura de diretórios mostrada e implemente o Gerenciador de Produtos conforme o código fornecido. Execute e teste todas as operações CRUD.
2. Altere o esquema de cores no `.env` para `green` e o tema para `light`. Verifique se a interface reflete as mudanças após reiniciar.
3. Adicione uma coluna `descricao` na Treeview e no formulário, permitindo visualizar e editar a descrição do produto.

<!-- gabarito -->
??? success "Gabarito — Básico"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    # 1) Monte as pastas como na aula, rode `python app.py` e teste: adicionar, selecionar
    #    na tabela (os campos são preenchidos), atualizar, excluir (com confirmação) e limpar.

    # 2) .env — tema claro e cor verde. Feche e abra o programa: a View lê esses valores
    #    ao iniciar (ctk.set_appearance_mode e ctk.set_default_color_theme).
    #        TEMA=light
    #        COR_TEMA=green

    # 3) Coluna e campo "Descrição"
    ```

    ```python title="views/main_view.py — MainView"
        def _criar_widgets(self):
            form = ctk.CTkFrame(self)
            form.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            self.entry_nome = ctk.CTkEntry(form, width=200)
            self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(form, text="Preço:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
            self.entry_preco = ctk.CTkEntry(form, width=100)
            self.entry_preco.grid(row=0, column=3, padx=5, pady=5)
            ctk.CTkLabel(form, text="Qtd:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
            self.entry_quantidade = ctk.CTkEntry(form, width=60)
            self.entry_quantidade.grid(row=0, column=5, padx=5, pady=5)

            # Linha nova: descrição ocupando a largura do formulário
            ctk.CTkLabel(form, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            self.entry_descricao = ctk.CTkEntry(form)
            self.entry_descricao.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="we")

            self.btn_adicionar = ctk.CTkButton(form, text="Adicionar")
            self.btn_adicionar.grid(row=0, column=6, padx=10, pady=5)
            self.btn_atualizar = ctk.CTkButton(form, text="Atualizar", state="disabled")
            self.btn_atualizar.grid(row=0, column=7, padx=5, pady=5)
            self.btn_excluir = ctk.CTkButton(form, text="Excluir", state="disabled")
            self.btn_excluir.grid(row=1, column=6, padx=10, pady=5)
            self.btn_limpar = ctk.CTkButton(form, text="Limpar")
            self.btn_limpar.grid(row=1, column=7, padx=5, pady=5)

            colunas = ("id", "nome", "descricao", "preco", "quantidade")
            self.tree = ttk.Treeview(self, columns=colunas, show="headings")
            for coluna, titulo in zip(colunas, ("ID", "Nome", "Descrição", "Preço (R$)", "Qtd")):
                self.tree.heading(coluna, text=titulo)
            self.tree.column("id", width=50)
            self.tree.column("preco", width=100)
            self.tree.column("quantidade", width=80)
            self.tree.pack(fill="both", expand=True, padx=10, pady=10)

            scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
    ```

    ```python title="controllers/produto_controller.py — ProdutoController (métodos alterados)"
        def _ao_selecionar(self, event):
            selecionado = self.view.tree.selection()
            if not selecionado:
                self.limpar()
                return
            id_, nome, descricao, preco, qtd = self.view.tree.item(selecionado)["values"]
            self.id_edicao = id_
            for campo, valor in ((self.view.entry_nome, nome), (self.view.entry_descricao, descricao),
                                 (self.view.entry_preco, preco), (self.view.entry_quantidade, qtd)):
                campo.delete(0, "end")
                campo.insert(0, valor)
            self.view.btn_atualizar.configure(state="normal")
            self.view.btn_excluir.configure(state="normal")
            self.view.btn_adicionar.configure(state="disabled")

        def adicionar(self):
            try:
                nome, preco, qtd = self._validar_campos()
                descricao = self.view.entry_descricao.get().strip()
                Produto(nome=nome, descricao=descricao, preco=preco, quantidade=qtd).salvar()
                self._atualizar_lista()
                self.limpar()
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")
            except ValueError as e:
                messagebox.showerror("Erro de validação", str(e))
            except sqlite3.Error as e:
                messagebox.showerror("Erro no banco de dados", f"Não foi possível salvar.\n{e}")

        def atualizar(self):
            if not self.id_edicao:
                return
            try:
                nome, preco, qtd = self._validar_campos()
                descricao = self.view.entry_descricao.get().strip()
                Produto(id=self.id_edicao, nome=nome, descricao=descricao, preco=preco, quantidade=qtd).salvar()
                self._atualizar_lista()
                self.limpar()
                messagebox.showinfo("Sucesso", "Produto atualizado.")
            except ValueError as e:
                messagebox.showerror("Erro de validação", str(e))
            except sqlite3.Error as e:
                messagebox.showerror("Erro no banco de dados", str(e))

        def limpar(self):
            for campo in (self.view.entry_nome, self.view.entry_descricao,
                          self.view.entry_preco, self.view.entry_quantidade):
                campo.delete(0, "end")
            self.id_edicao = None
            self.view.btn_adicionar.configure(state="normal")
            self.view.btn_atualizar.configure(state="disabled")
            self.view.btn_excluir.configure(state="disabled")
            self.view.tree.selection_remove(self.view.tree.selection())

        def _atualizar_lista(self):
            self.view.tree.delete(*self.view.tree.get_children())
            for p in Produto.listar_todos():
                self.view.tree.insert("", "end", values=(p.id, p.nome, p.descricao or "",
                                                         f"{p.preco:.2f}", p.quantidade))
    ```


### Intermediário (aplicação)

1. Crie uma nova entidade `Categoria` com tabela `categorias` (id, nome). Relacione `produto` com `categoria` (chave estrangeira). Atualize a interface para selecionar a categoria em um `CTkOptionMenu`. Implemente as classes Model, View e Controller para Categoria.
2. Adicione uma funcionalidade de busca por nome na listagem de produtos: um campo de entrada e botão que filtram a Treeview usando `SELECT ... WHERE nome LIKE ?`. Lembre-se de recarregar a lista completa ao limpar a busca.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python title="models/database.py"
    import sqlite3
    from config import DB_PATH


    def obter_conexao():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn


    def inicializar_banco():
        with obter_conexao() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco REAL NOT NULL CHECK(preco >= 0),
                    quantidade INTEGER NOT NULL DEFAULT 0,
                    categoria_id INTEGER REFERENCES categorias(id)
                );
            """)
            # Banco criado antes desta versão? Acrescenta a coluna sem perder os produtos.
            colunas = [linha["name"] for linha in conn.execute("PRAGMA table_info(produtos)")]
            if "categoria_id" not in colunas:
                conn.execute("ALTER TABLE produtos ADD COLUMN categoria_id INTEGER REFERENCES categorias(id)")
    ```

    ```python title="models/categoria.py"
    from models.database import obter_conexao


    class Categoria:
        def __init__(self, id=None, nome=""):
            self.id = id
            self.nome = nome

        @classmethod
        def listar_todas(cls):
            with obter_conexao() as conn:
                return [cls(**dict(l)) for l in conn.execute("SELECT * FROM categorias ORDER BY nome")]

        @classmethod
        def buscar_por_nome(cls, nome):
            with obter_conexao() as conn:
                linha = conn.execute("SELECT * FROM categorias WHERE nome = ?", (nome,)).fetchone()
                return cls(**dict(linha)) if linha else None

        def salvar(self):
            with obter_conexao() as conn:
                self.id = conn.execute("INSERT INTO categorias (nome) VALUES (?)", (self.nome,)).lastrowid
    ```

    ```python title="models/produto.py"
    from models.database import obter_conexao


    class Produto:
        def __init__(self, id=None, nome="", descricao="", preco=0.0, quantidade=0,
                     categoria_id=None, categoria=None):
            self.id = id
            self.nome = nome
            self.descricao = descricao
            self.preco = preco
            self.quantidade = quantidade
            self.categoria_id = categoria_id
            self.categoria = categoria  # nome da categoria, vindo do JOIN

        _SELECT = """
            SELECT p.*, c.nome AS categoria
            FROM produtos p LEFT JOIN categorias c ON c.id = p.categoria_id
        """

        @classmethod
        def listar_todos(cls):
            with obter_conexao() as conn:
                return [cls(**dict(l)) for l in conn.execute(cls._SELECT + " ORDER BY p.nome")]

        @classmethod
        def buscar_por_nome(cls, termo):
            """(Exercício 2) Produtos cujo nome contém o termo."""
            with obter_conexao() as conn:
                return [cls(**dict(l)) for l in conn.execute(
                    cls._SELECT + " WHERE p.nome LIKE ? ORDER BY p.nome", (f"%{termo}%",))]

        def salvar(self):
            with obter_conexao() as conn:
                dados = (self.nome, self.descricao, self.preco, self.quantidade, self.categoria_id)
                if self.id:
                    conn.execute("UPDATE produtos SET nome=?, descricao=?, preco=?, quantidade=?, "
                                 "categoria_id=? WHERE id=?", dados + (self.id,))
                else:
                    self.id = conn.execute("INSERT INTO produtos (nome, descricao, preco, quantidade, "
                                           "categoria_id) VALUES (?, ?, ?, ?, ?)", dados).lastrowid

        def excluir(self):
            if self.id:
                with obter_conexao() as conn:
                    conn.execute("DELETE FROM produtos WHERE id = ?", (self.id,))
    ```

    ```python title="views/categoria_view.py"
    import customtkinter as ctk


    class CategoriaView(ctk.CTkToplevel):
        """Janela pequena para cadastrar categorias."""

        def __init__(self, master):
            super().__init__(master)
            self.title("Categorias")
            self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nova categoria", width=200)
            self.entry_nome.grid(row=0, column=0, padx=10, pady=10)
            self.btn_salvar = ctk.CTkButton(self, text="Salvar categoria", width=120)
            self.btn_salvar.grid(row=0, column=1, padx=(0, 10), pady=10)
            self.lista = ctk.CTkLabel(self, text="", justify="left")
            self.lista.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
    ```

    ```python title="controllers/categoria_controller.py"
    import sqlite3
    from tkinter import messagebox

    from models.categoria import Categoria
    from views.categoria_view import CategoriaView


    class CategoriaController:
        def __init__(self, master, ao_alterar):
            self.ao_alterar = ao_alterar  # avisa o ProdutoController para recarregar o menu
            self.view = CategoriaView(master)
            self.view.btn_salvar.configure(command=self.salvar)
            self._mostrar()

        def _mostrar(self):
            nomes = [c.nome for c in Categoria.listar_todas()]
            self.view.lista.configure(text="\n".join(f"• {n}" for n in nomes) or "Nenhuma categoria.")

        def salvar(self):
            nome = self.view.entry_nome.get().strip()
            if not nome:
                messagebox.showwarning("Categoria", "Digite o nome da categoria.")
                return
            try:
                Categoria(nome=nome).salvar()
            except sqlite3.IntegrityError:
                messagebox.showerror("Categoria", f"A categoria '{nome}' já existe.")
                return
            self.view.entry_nome.delete(0, "end")
            self._mostrar()
            self.ao_alterar()
    ```

    ```python title="views/main_view.py — MainView: categoria no formulário, busca e coluna nova"
        def _criar_widgets(self):
            busca = ctk.CTkFrame(self, fg_color="transparent")
            busca.pack(fill="x", padx=10, pady=(10, 0))
            self.entry_busca = ctk.CTkEntry(busca, placeholder_text="Buscar por nome...")
            self.entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 5))
            self.btn_buscar = ctk.CTkButton(busca, text="Buscar", width=80)
            self.btn_buscar.pack(side="left")

            form = ctk.CTkFrame(self)
            form.pack(fill="x", padx=10, pady=10)
            ctk.CTkLabel(form, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            self.entry_nome = ctk.CTkEntry(form, width=200)
            self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(form, text="Preço:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
            self.entry_preco = ctk.CTkEntry(form, width=100)
            self.entry_preco.grid(row=0, column=3, padx=5, pady=5)
            ctk.CTkLabel(form, text="Qtd:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
            self.entry_quantidade = ctk.CTkEntry(form, width=60)
            self.entry_quantidade.grid(row=0, column=5, padx=5, pady=5)
            ctk.CTkLabel(form, text="Categoria:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            self.menu_categoria = ctk.CTkOptionMenu(form, values=["(sem categoria)"])
            self.menu_categoria.grid(row=1, column=1, padx=5, pady=5, sticky="w")
            self.btn_categorias = ctk.CTkButton(form, text="Categorias...", width=110)
            self.btn_categorias.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="w")

            self.btn_adicionar = ctk.CTkButton(form, text="Adicionar")
            self.btn_adicionar.grid(row=0, column=6, padx=10, pady=5)
            self.btn_atualizar = ctk.CTkButton(form, text="Atualizar", state="disabled")
            self.btn_atualizar.grid(row=0, column=7, padx=5, pady=5)
            self.btn_excluir = ctk.CTkButton(form, text="Excluir", state="disabled")
            self.btn_excluir.grid(row=1, column=6, padx=10, pady=5)
            self.btn_limpar = ctk.CTkButton(form, text="Limpar")
            self.btn_limpar.grid(row=1, column=7, padx=5, pady=5)

            colunas = ("id", "nome", "categoria", "preco", "quantidade")
            self.tree = ttk.Treeview(self, columns=colunas, show="headings")
            for coluna, titulo in zip(colunas, ("ID", "Nome", "Categoria", "Preço (R$)", "Qtd")):
                self.tree.heading(coluna, text=titulo)
            self.tree.column("id", width=50)
            self.tree.pack(fill="both", expand=True, padx=10, pady=10)
    ```

    ```python title="controllers/produto_controller.py — ProdutoController (métodos novos e alterados)"
        def __init__(self):
            self.view = MainView()
            self.id_edicao = None
            self._conectar_eventos()
            self._recarregar_categorias()
            self._atualizar_lista()

        def _conectar_eventos(self):
            self.view.btn_adicionar.configure(command=self.adicionar)
            self.view.btn_atualizar.configure(command=self.atualizar)
            self.view.btn_excluir.configure(command=self.excluir)
            self.view.btn_limpar.configure(command=self.limpar)
            self.view.btn_buscar.configure(command=self.buscar)
            self.view.btn_categorias.configure(command=self.abrir_categorias)
            self.view.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

        def _recarregar_categorias(self):
            nomes = ["(sem categoria)"] + [c.nome for c in Categoria.listar_todas()]
            self.view.menu_categoria.configure(values=nomes)

        def abrir_categorias(self):
            CategoriaController(self.view, ao_alterar=self._recarregar_categorias)

        def _categoria_escolhida(self):
            categoria = Categoria.buscar_por_nome(self.view.menu_categoria.get())
            return categoria.id if categoria else None

        def _ao_selecionar(self, event):
            selecionado = self.view.tree.selection()
            if not selecionado:
                self.limpar()
                return
            id_, nome, categoria, preco, qtd = self.view.tree.item(selecionado)["values"]
            self.id_edicao = id_
            for campo, valor in ((self.view.entry_nome, nome), (self.view.entry_preco, preco),
                                 (self.view.entry_quantidade, qtd)):
                campo.delete(0, "end")
                campo.insert(0, valor)
            self.view.menu_categoria.set(categoria or "(sem categoria)")
            self.view.btn_atualizar.configure(state="normal")
            self.view.btn_excluir.configure(state="normal")
            self.view.btn_adicionar.configure(state="disabled")

        def adicionar(self):
            try:
                nome, preco, qtd = self._validar_campos()
                Produto(nome=nome, preco=preco, quantidade=qtd,
                        categoria_id=self._categoria_escolhida()).salvar()
                self._atualizar_lista()
                self.limpar()
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")
            except ValueError as e:
                messagebox.showerror("Erro de validação", str(e))
            except sqlite3.Error as e:
                messagebox.showerror("Erro no banco de dados", f"Não foi possível salvar.\n{e}")

        def atualizar(self):
            if not self.id_edicao:
                return
            try:
                nome, preco, qtd = self._validar_campos()
                Produto(id=self.id_edicao, nome=nome, preco=preco, quantidade=qtd,
                        categoria_id=self._categoria_escolhida()).salvar()
                self._atualizar_lista()
                self.limpar()
                messagebox.showinfo("Sucesso", "Produto atualizado.")
            except ValueError as e:
                messagebox.showerror("Erro de validação", str(e))
            except sqlite3.Error as e:
                messagebox.showerror("Erro no banco de dados", str(e))

        def buscar(self):
            termo = self.view.entry_busca.get().strip()
            self._atualizar_lista(Produto.buscar_por_nome(termo) if termo else None)  # vazio = todos

        def _atualizar_lista(self, produtos=None):
            self.view.tree.delete(*self.view.tree.get_children())
            for p in (produtos if produtos is not None else Produto.listar_todos()):
                self.view.tree.insert("", "end", values=(p.id, p.nome, p.categoria or "",
                                                         f"{p.preco:.2f}", p.quantidade))

    # No topo de controllers/produto_controller.py, acrescente os imports:
    #     from models.categoria import Categoria
    #     from controllers.categoria_controller import CategoriaController
    ```


### Avançado (desafio)

1. Empacote o projeto com PyInstaller. Teste o executável em outro computador (ou máquina virtual) sem Python instalado. Resolva eventuais problemas de dependências. Inclua a biblioteca `customtkinter` explicitamente se necessário.
2. Implemente um sistema de logs usando o módulo `logging` do Python. Configure-o via `.env` (nível de log, arquivo de saída). Substitua os `print` e adicione logs em pontos estratégicos (erros de banco, ações do usuário). Exiba as mensagens de log também em uma barra de status na interface.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Uma solução possível — compare com a sua. Outras formas também podem estar certas.

    ```python
    # ───────────── 1) Executável com PyInstaller (roteiro — não testado aqui) ─────────────
    # Este passo depende da sua máquina: siga e anote o que aconteceu em cada etapa.
    #
    #   pip install pyinstaller
    #   pyinstaller --onefile --windowed --name GerenciadorProdutos ^
    #               --collect-data customtkinter app.py
    #
    # --collect-data customtkinter  → leva junto os temas (.json) do CustomTkinter;
    #                                 sem ele o executável abre e fecha com "theme not found".
    # Depois:
    #   1. Copie dist/GerenciadorProdutos.exe para outro computador (ou VM) sem Python.
    #   2. Ao lado do .exe, coloque um .env (sem senhas reais) — o config.py da aula procura
    #      o .env na pasta do executável. Sem .env, valem os padrões do config.py.
    #   3. Abra, cadastre um produto, feche e abra de novo: o produtos.db fica na mesma pasta.
    #   4. Antivírus reclamou? É comum com --onefile; teste também sem essa opção (gera uma pasta).

    # ───────────── 2) Logs configuráveis pelo .env ─────────────
    # .env:
    #     LOG_NIVEL=INFO
    #     LOG_ARQUIVO=app.log
    ```

    ```python title="utils/log.py"
    import logging
    import os

    from dotenv import load_dotenv

    load_dotenv()


    class StatusBarHandler(logging.Handler):
        """Mostra a última mensagem de log em um rótulo da interface."""

        def __init__(self, rotulo):
            super().__init__()
            self.rotulo = rotulo

        def emit(self, registro):
            cores = {"ERROR": "#E57373", "WARNING": "#FFB74D"}
            self.rotulo.configure(text=self.format(registro), text_color=cores.get(registro.levelname, "gray"))


    def configurar_log():
        logger = logging.getLogger("gerenciador")
        logger.setLevel(os.getenv("LOG_NIVEL", "INFO").upper())
        if not logger.handlers:  # evita duplicar handlers se for chamado duas vezes
            arquivo = logging.FileHandler(os.getenv("LOG_ARQUIVO", "app.log"), encoding="utf-8")
            arquivo.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            logger.addHandler(arquivo)
        return logger


    def ligar_barra_de_status(logger, rotulo):
        handler = StatusBarHandler(rotulo)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    ```

    ```python title="views/main_view.py — MainView: barra de status no rodapé"
        def __init__(self):
            ctk.set_appearance_mode(TEMA)
            ctk.set_default_color_theme(COR_TEMA)
            super().__init__()
            self.title(TITULO_APP)
            self.geometry("800x500")
            self.status = ctk.CTkLabel(self, text="Pronto.", anchor="w")
            self.status.pack(side="bottom", fill="x", padx=10, pady=(0, 5))
            self._criar_widgets()
    ```

    ```python title="controllers/produto_controller.py — ProdutoController: logs no lugar de prints"
    #     No topo:  from utils.log import configurar_log, ligar_barra_de_status
        def __init__(self):
            self.log = configurar_log()
            self.view = MainView()
            ligar_barra_de_status(self.log, self.view.status)
            self.id_edicao = None
            self._conectar_eventos()
            self._atualizar_lista()
            self.log.info("Aplicação iniciada.")

        def adicionar(self):
            try:
                nome, preco, qtd = self._validar_campos()
                produto = Produto(nome=nome, preco=preco, quantidade=qtd)
                produto.salvar()
                self.log.info("Produto adicionado: %s (id %s)", nome, produto.id)
                self._atualizar_lista()
                self.limpar()
            except ValueError as e:
                self.log.warning("Validação: %s", e)
                messagebox.showerror("Erro de validação", str(e))
            except sqlite3.Error as e:
                self.log.error("Erro de banco ao adicionar: %s", e)
                messagebox.showerror("Erro no banco de dados", f"Não foi possível salvar.\n{e}")

        def excluir(self):
            if not self.id_edicao:
                return
            if messagebox.askyesno("Confirmar", "Excluir o produto selecionado?"):
                try:
                    Produto(id=self.id_edicao).excluir()
                    self.log.info("Produto excluído: id %s", self.id_edicao)
                    self._atualizar_lista()
                    self.limpar()
                except sqlite3.Error as e:
                    self.log.error("Erro de banco ao excluir: %s", e)
                    messagebox.showerror("Erro", str(e))
    ```


## Projeto Prático

### Sistema de Controle de Estoque com Arquitetura MVC

Vamos projetar um sistema completo de controle de estoque, aplicando tudo o que aprendemos. O escopo será:

- **Entidades**: Produto, Categoria, Movimentação (entrada/saída de estoque).
- **Funcionalidades**:
    - CRUD de produtos e categorias.
    - Registro de movimentações, com data e quantidade.
    - Tela de dashboard com resumo (total de produtos, valor em estoque, movimentações recentes).
    - Abas usando `CTkTabview`.
- **Arquitetura**: MVC rigorosa.
- **Persistência**: SQLite com chaves estrangeiras e integridade referencial.
- **Configuração**: `.env` para caminho do banco, tema e título.
- **Tratamento de erros**: validações na camada de modelo, exceções personalizadas.
- **Empacotamento**: executável final com PyInstaller, sem console, com teste em máquina limpa.

**Etapas:**

1. **Definição da estrutura:**
    ```text
    estoque_app/
    ├── app.py
    ├── config.py
    ├── .env
    ├── .env.example
    ├── models/
    │   ├── database.py
    │   ├── produto.py
    │   ├── categoria.py
    │   └── movimentacao.py
    ├── views/
    │   ├── main_view.py
    │   ├── produto_view.py
    │   ├── categoria_view.py
    │   └── dashboard_view.py
    ├── controllers/
    │   ├── produto_controller.py
    │   ├── categoria_controller.py
    │   └── dashboard_controller.py
    └── utils/
        ├── exceptions.py
        └── logger.py
    ```

2. **Modelos**:
    - `database.py`: conexão, inicialização de todas as tabelas com FOREIGN KEY.
    - `produto.py`: classe Produto com CRUD e método `valor_total_estoque()`.
    - `categoria.py`: classe Categoria.
    - `movimentacao.py`: classe Movimentacao com atributos id, produto_id, tipo (entrada/saída), quantidade, data.

3. **Views**:
    - `main_view.py`: janela principal com `CTkTabview` contendo abas "Dashboard", "Produtos", "Categorias", "Movimentações".
    - Cada aba é um frame (poderia ser uma classe separada) construído na própria view ou importado.
    - Uso de `CTkFrame`, `CTkEntry`, `CTkButton`, Treeview (dentro de frames específicos).

4. **Controllers**:
    - Um controller para cada entidade, responsável por ligar eventos da view correspondente e chamar métodos do modelo.
    - `DashboardController`: atualiza labels com resumo, consultando os modelos.

5. **Tratamento de erros**:
    - Exceções personalizadas como `EstoqueInsuficienteError`, `CategoriaNaoEncontradaError`.
    - Captura genérica nos controllers para exibir messagebox.

6. **Empacotamento**:
    - Após testes, rodar PyInstaller com `--add-data` para incluir a pasta models, views, etc., se necessário. Normalmente o `--onefile` já embute tudo.
    - Criar um instalador com NSIS ou Inno Setup (opcional, mas mencionado).

**Cronograma sugerido:** 2 a 3 dias de trabalho dedicado. O importante é a organização e a aplicação do padrão MVC.

Esse projeto será o seu cartão de visitas como desenvolvedor Python desktop. Capriche na documentação e nos comentários.

## Resumo

Neste capítulo, você concluiu a jornada de aprendizado integrando todos os pilares do desenvolvimento desktop com Python:

- **Arquitetura MVC**: separação clara entre dados (Model), interface (View) e controle (Controller), facilitando manutenção e escalabilidade.
- **CustomTkinter**: interface moderna com temas e widgets estilizados.
- **SQLite**: persistência robusta com modelo orientado a objetos, incluindo chaves estrangeiras e validações.
- **Variáveis de ambiente**: segurança e portabilidade com `.env` e `python-dotenv`.
- **Tratamento de erros**: feedback amigável ao usuário e estabilidade da aplicação.
- **Empacotamento com PyInstaller**: geração de executáveis para distribuição profissional.

Agora você detém o conhecimento necessário para projetar, implementar e distribuir aplicações desktop completas em Python. O céu é o limite!
