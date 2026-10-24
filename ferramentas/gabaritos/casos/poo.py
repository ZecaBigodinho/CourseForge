"""Casos de teste dos gabaritos de POO (Módulo 02). O código vem das aulas."""

from extrair import blocos_python, gabarito

MODULO = "modulo_07_poo"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


# Classes da aula 03 (Passos 1–3): os gabaritos Básico e Intermediário rodam sobre elas
_CLASSES = "\n".join(b for b in blocos_python(MODULO, "03_desenvolvimento_pratico_poo.md")
                     if b.startswith("class "))

GABARITOS = [
("01_paradigma_poo.md", "Básico", G('01_paradigma_poo.md', 'Básico'), ""),
("01_paradigma_poo.md", "Intermediário", G('01_paradigma_poo.md', 'Intermediário'), ""),
("01_paradigma_poo.md", "Avançado", G('01_paradigma_poo.md', 'Avançado'), ""),
("02_metodos_e_propriedades.md", "Básico", G('02_metodos_e_propriedades.md', 'Básico'), ""),
("02_metodos_e_propriedades.md", "Intermediário", G('02_metodos_e_propriedades.md', 'Intermediário'), ""),
("02_metodos_e_propriedades.md", "Avançado", G('02_metodos_e_propriedades.md', 'Avançado'), ""),
("03_desenvolvimento_pratico_poo.md", "Básico", G('03_desenvolvimento_pratico_poo.md', 'Básico'), "", "# === gabarito ===\n"),
("03_desenvolvimento_pratico_poo.md", "Intermediário", G('03_desenvolvimento_pratico_poo.md', 'Intermediário'), "", '''\
# === gabarito ===
'''),
("03_desenvolvimento_pratico_poo.md", "Avançado", G('03_desenvolvimento_pratico_poo.md', 'Avançado'), ""),
]

# Os gabaritos da aula 03 (Básico e Intermediário) rodam sobre as classes da aula
_BASICO_03, _INTER_03 = GABARITOS[6], GABARITOS[7]
GABARITOS[6] = _BASICO_03[:4] + (_CLASSES + "\n" + _BASICO_03[4],)
_metodos = "\n".join(l for l in _INTER_03[2].splitlines() if not l.startswith("# Acrescente"))
GABARITOS[7] = _INTER_03[:4] + (_CLASSES + "\n" + _metodos.replace("\n", "\n", 1) + '''

pedido = Pedido("Teste")
p = Produto(9, "Fone", 50.0, 10)
pedido.adicionar_item(p, 3)
print("Unidades:", pedido.quantidade_itens, "| estoque:", p.estoque)   # 3 | 7
pedido.remover_item(9)
print("Unidades:", pedido.quantidade_itens, "| estoque:", p.estoque)   # 0 | 10
for codigo in (9, 99):
    try:
        pedido.remover_item(codigo)
    except ValueError as erro:
        print("❌", erro)
pedido.adicionar_item(p, 1)
pedido.finalizar_pedido()
try:
    pedido.remover_item(9)
except ValueError as erro:
    print("❌", erro)
''',)
