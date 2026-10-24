"""Casos de teste dos gabaritos das aulas 01–05 de Fundamentos. O código vem das aulas."""

from extrair import gabarito

MODULO = "modulo_01_fundamentos"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


GABARITOS = [
# ---------------------------------------------------------------- 01 variáveis
("01_variaveis.md", "Básico", G('01_variaveis.md', 'Básico'), ""),
("01_variaveis.md", "Intermediário", G('01_variaveis.md', 'Intermediário'), "150\n"),
("01_variaveis.md", "Avançado", G('01_variaveis.md', 'Avançado'), "Ana\n19\n1.68\ns\n"),
# ---------------------------------------------------------------- 02 operadores
("02_operadores.md", "Básico", G('02_operadores.md', 'Básico'), "2008\n2026\n"),
("02_operadores.md", "Intermediário", G('02_operadores.md', 'Intermediário'), "120\nsim\n"),
("02_operadores.md", "Avançado", G('02_operadores.md', 'Avançado'), "15\n7\n22\n"),
# ---------------------------------------------------------------- 03 if/else
("03_if_else.md", "Básico", G('03_if_else.md', 'Básico'), "7\n17\n-3\n"),
("03_if_else.md", "Intermediário", G('03_if_else.md', 'Intermediário'), "250\n"),
("03_if_else.md", "Avançado", G('03_if_else.md', 'Avançado'), "8\n3.5\n6.5\n"),
# ---------------------------------------------------------------- 04 repetições
("04_repeticoes.md", "Básico", G('04_repeticoes.md', 'Básico'), "a\nb\nx\n"),
("04_repeticoes.md", "Intermediário", G('04_repeticoes.md', 'Intermediário'), "39.90\n-5\n60\n0\n"),
("04_repeticoes.md", "Avançado", G('04_repeticoes.md', 'Avançado'), "1\n200\n2\n5000\n2\n300\n3\n4\n"),
# ---------------------------------------------------------------- 05 funções
("05_funcoes.md", "Básico", G('05_funcoes.md', 'Básico'), ""),
("05_funcoes.md", "Intermediário", G('05_funcoes.md', 'Intermediário'), "6\n5.5\n7\n"),
("05_funcoes.md", "Avançado", G('05_funcoes.md', 'Avançado'), ""),
]
