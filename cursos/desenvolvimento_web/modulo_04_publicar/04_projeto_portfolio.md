# 04 — Projeto final: portfólio no ar

> **Curso:** Desenvolvimento Web  
> **Módulo:** 04 — Publicar  
> **Tempo estimado:** 3 h  

---

## Objetivos

Ao final deste projeto, você terá:

- Um **portfólio** com a sua apresentação e os projetos do curso.
- Uma seção que busca dados de uma **API** pública.
- Tudo **publicado** no GitHub Pages, com `README.md`.

## Pré-requisitos

- Aulas [01](01_fetch_e_apis.md) a [03](03_github_pages.md) deste módulo e os projetos dos Módulos 01 a 03.

---

## O que o portfólio deve ter

| Parte | Origem |
|---|---|
| Cabeçalho com nome e menu | Módulo 01 + Flexbox (Módulo 02) |
| Sobre mim | Página de apresentação (Módulo 01) |
| **Projetos**: um cartão para cada, com imagem, descrição e link | Grid (Módulo 02) |
| Os projetos em si, em subpastas: `cardapio/`, `tarefas/` | Módulos 02 e 03 |
| Um extra com API (busca de CEP, feriados nacionais da BrasilAPI…) | Aula 01 |
| Contato | Formulário (Módulo 01) ou só um `mailto:` |

### Estrutura sugerida

```text
seu-usuario.github.io/
├── index.html          ← o portfólio
├── README.md
├── css/style.css
├── js/script.js
├── imagens/
├── cardapio/           ← projeto do Módulo 02
│   ├── index.html
│   └── css/style.css
└── tarefas/            ← projeto do Módulo 03
    ├── index.html
    ├── style.css
    └── script.js
```

O cartão de cada projeto aponta para a subpasta:

```html
<article class="cartao">
  <img src="imagens/cardapio.png" alt="Cardápio da Lanchonete do Bairro no celular">
  <h3>Cardápio responsivo</h3>
  <p>HTML e CSS com Flexbox e Grid.</p>
  <a href="cardapio/">Ver projeto</a>
</article>
```

!!! tip "Imagem do projeto"
    Para a miniatura, tire um print da página no modo celular do `F12` (`Ctrl + Shift + M`; no menu ⋮ do painel há **Capturar captura de tela**). Salve em `imagens/` com nome minúsculo.

---

## Lista de conferência antes de publicar

- [ ] HTML válido no W3C em todas as páginas.
- [ ] Funciona no modo celular (`F12`).
- [ ] Todos os links e imagens funcionam (nenhum 404 na guia **Rede**).
- [ ] Nenhum erro vermelho no **Console**.
- [ ] Navegável só com o teclado.
- [ ] `README.md`, `description` e `og:` preenchidos.
- [ ] Só dados pessoais que você **quer** tornar públicos.

---

## Entrega (requisito do certificado)

1. O **link** do portfólio no ar (`https://seu-usuario.github.io`).
2. O **link** do repositório no GitHub.

### Critérios de avaliação

| Critério | O que se espera |
|---|---|
| No ar | O link abre e todos os projetos funcionam |
| Conteúdo | Apresentação + os três projetos do curso + um extra com API |
| Qualidade | HTML válido, responsivo, sem erros no Console, acessível pelo teclado |
| Organização | Pastas, nomes de arquivo e `README.md` caprichados |

---

## Exercícios extras

### Básico (fixação)

Acrescente ao portfólio um rodapé com o ano atual escrito pelo JavaScript.

<!-- gabarito -->
??? success "Gabarito — Básico"
    No HTML: `<footer><p>© <span id="ano"></span> Ana Souza</p></footer>`. No JS: `document.querySelector("#ano").textContent = new Date().getFullYear();`.

### Intermediário (aplicação)

Mostre no portfólio os **próximos feriados nacionais** buscando a BrasilAPI (`https://brasilapi.com.br/api/feriados/v1/2026`).

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    ```js
    async function mostrarFeriados() {
      const lista = document.querySelector("#feriados");
      try {
        const r = await fetch("https://brasilapi.com.br/api/feriados/v1/2026");
        if (!r.ok) throw new Error(r.status);
        const feriados = await r.json();
        const hoje = new Date().toISOString().slice(0, 10);
        feriados.filter((f) => f.date >= hoje).slice(0, 3).forEach((f) => {
          const li = document.createElement("li");
          li.textContent = `${f.date.split("-").reverse().join("/")} — ${f.name}`;
          lista.append(li);
        });
      } catch {
        lista.textContent = "Não foi possível carregar os feriados agora.";
      }
    }
    mostrarFeriados();
    ```
    As datas vêm no formato `AAAA-MM-DD`, por isso a comparação de texto com `hoje` funciona.

### Avançado (desafio)

Peça a dois colegas para abrirem o seu portfólio no celular e anotarem três coisas que melhorariam. Faça as mudanças e publique a nova versão.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    Não há resposta única: o objetivo é o ciclo **testar ➔ ouvir ➔ corrigir ➔ publicar**, o mesmo do trabalho profissional. Registre o que mudou na mensagem do commit (por exemplo, `"Aumenta a fonte dos cartões no celular"`).

---

## 💡 Resumo

- O portfólio reúne a apresentação e os projetos, cada um na sua subpasta.
- Confira validação, celular, links, Console e teclado antes de publicar.
- O link no ar é o seu cartão de visita como desenvolvedor.

## ➡️ Próximo passo

Parabéns, você terminou o curso de **Desenvolvimento Web**! Volte ao [índice do módulo](index.md) para conferir o checklist. O próximo passo da trilha é o curso de **[TypeScript](../../typescript/docs/index.md)**.
