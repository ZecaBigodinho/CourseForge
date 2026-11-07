# 02 — Listas: filtrar, editar e remover

> **Curso:** React  
> **Módulo:** 02 — Listas, formulários e efeitos  
> **Tempo estimado:** 1 h 30 min  

---

## Objetivos

Ao final desta aula, você será capaz de:

- **Acrescentar**, **remover** e **editar** itens de uma lista no estado.
- **Filtrar** e **buscar** sem duplicar dados.
- Entender por que a `key` precisa ser estável.
- Mostrar uma mensagem quando a lista estiver vazia.

## Pré-requisitos

- [Aula 01](01_formularios_controlados.md) deste módulo.

---

## As três operações

```tsx
type Contato = { id: number; nome: string; favorito: boolean };

const [contatos, setContatos] = useState<Contato[]>([
  { id: 1, nome: "Ana Souza", favorito: true },
  { id: 2, nome: "Bruno Lima", favorito: false },
]);

// acrescentar
setContatos((atual) => [...atual, { id: Date.now(), nome: "Carla Dias", favorito: false }]);

// remover
setContatos((atual) => atual.filter((c) => c.id !== id));

// editar um item
setContatos((atual) => atual.map((c) => (c.id === id ? { ...c, favorito: !c.favorito } : c)));
```

As três devolvem um **array novo** (aula 04 do Módulo 01) e usam o **`id`** para achar o item certo, nunca a posição.

---

## Filtrar e buscar: dados calculados

O filtro e a busca **não** mudam a lista guardada. Eles são **calculados** a cada renderização:

```tsx
const [busca, setBusca] = useState("");
const [soFavoritos, setSoFavoritos] = useState(false);

const visiveis = contatos
  .filter((c) => !soFavoritos || c.favorito)
  .filter((c) => c.nome.toLowerCase().includes(busca.toLowerCase()));

return (
  <>
    <input value={busca} onChange={(e) => setBusca(e.target.value)} placeholder="Buscar" />
    <label>
      <input type="checkbox" checked={soFavoritos} onChange={(e) => setSoFavoritos(e.target.checked)} />
      Só favoritos
    </label>
    {visiveis.length === 0 ? (
      <p>Nenhum contato encontrado.</p>
    ) : (
      <ul>
        {visiveis.map((c) => (
          <li key={c.id}>{c.nome}</li>
        ))}
      </ul>
    )}
  </>
);
```

!!! warning "Não guarde a lista filtrada no estado"
    Um `useState` com a lista filtrada fica **desatualizado** quando a lista original muda. Guarde só o que a pessoa escolheu (o texto da busca, o filtro) e calcule o resto.

---

## Por que a `key` estável importa

Quando um item sai do meio da lista, o React usa a `key` para saber **qual** saiu. Com `key={indice}`, todos os itens depois dele “mudam de identidade”: um campo que estava sendo editado ou uma caixa marcada pode pular para o item errado. Com `key={c.id}`, cada item mantém a sua identidade.

---

## Exercícios

### Básico (fixação)

Monte a lista de contatos da aula com um botão **Remover** em cada item.

<!-- gabarito -->
??? success "Gabarito — Básico"
    ```tsx
    {contatos.map((c) => (
      <li key={c.id}>
        {c.nome}{" "}
        <button type="button" onClick={() => setContatos((a) => a.filter((x) => x.id !== c.id))}>
          Remover
        </button>
      </li>
    ))}
    ```

### Intermediário (aplicação)

Acrescente a **busca por nome** e o filtro **Só favoritos**, com a mensagem de lista vazia.

<!-- gabarito -->
??? success "Gabarito — Intermediário"
    É o código da seção “Filtrar e buscar”. Teste: digite um nome que não existe e veja “Nenhum contato encontrado.”; apague a busca e a lista volta inteira, porque nada foi removido do estado.

### Avançado (desafio)

Permita **editar o nome** de um contato: um botão **Editar** troca o texto por um campo; **Salvar** grava a mudança.

<!-- gabarito -->
??? success "Gabarito — Avançado"
    ```tsx
    const [editando, setEditando] = useState<number | null>(null);
    const [rascunho, setRascunho] = useState("");

    function salvar(id: number) {
      setContatos((a) => a.map((c) => (c.id === id ? { ...c, nome: rascunho.trim() || c.nome } : c)));
      setEditando(null);
    }
    // em cada item:
    {editando === c.id ? (
      <>
        <input value={rascunho} onChange={(e) => setRascunho(e.target.value)} />
        <button type="button" onClick={() => salvar(c.id)}>Salvar</button>
      </>
    ) : (
      <>
        {c.nome}{" "}
        <button type="button" onClick={() => { setEditando(c.id); setRascunho(c.nome); }}>Editar</button>
      </>
    )}
    ```
    Guarda-se **qual** item está em edição (o `id`) e o texto provisório; o nome só muda na lista ao salvar.

---

## 💡 Resumo

- Acrescentar `[...a, novo]`, remover `filter`, editar `map` com `{ ...item }`, sempre pelo `id`.
- Busca e filtros: guarde a escolha, **calcule** a lista visível.
- `key` estável (`id`) mantém a identidade dos itens.
- Lista vazia: mostre uma mensagem.

## ➡️ Próximo passo

Na **[aula 03](03_useeffect_e_localstorage.md)** os dados passam a ser guardados no navegador.
