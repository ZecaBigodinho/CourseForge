"""Casos de teste dos gabaritos da aula 05 de Interfaces (Dashboard): aplicados sobre o código da aula."""

from extrair import blocos_python, gabarito
from patch_classe import aplicar

MODULO = "modulo_02_interfaces_graficas"


def G(aula, nivel):
    """Código do gabarito, lido da própria aula."""
    return gabarito(MODULO, aula, nivel)


# Código completo do Dashboard = maior bloco Python da aula (fora dos gabaritos)
DASHBOARD = max(blocos_python(MODULO, "05_projeto_pratico.md"), key=len)


def _teste(trecho: str, verificacoes: str) -> str:
    codigo = aplicar(DASHBOARD, "DashboardApp", trecho)
    return "import _gui\n" + codigo + "\n" + verificacoes


BASICO = G("05_projeto_pratico.md", "Básico")

INTERMEDIARIO = G("05_projeto_pratico.md", "Intermediário")

AVANCADO = G("05_projeto_pratico.md", "Avançado")

_HOJE = "from datetime import datetime as _dt\n_hoje = _dt.now().strftime('%Y-%m-%d')\n"

GABARITOS = [
("05_projeto_pratico.md", "Básico", BASICO, "", _teste(BASICO, _HOJE + '''
app.entry_desc.insert(0, "Teste"); app.entry_valor.insert(0, "0"); app.entry_data.insert(0, _hoje)
app.adicionar_transacao(); assert any("não pode ser zero" in m for m in _gui.MENSAGENS)
app.entry_valor.delete(0, "end"); app.entry_valor.insert(0, "50")
app.adicionar_transacao(); assert len(app.transacoes) == 1
import json; assert json.load(open("financas.json", encoding="utf-8"))[0]["valor"] == 50.0
print("zero recusado; transação válida salva em financas.json")
''')),
("05_projeto_pratico.md", "Intermediário", INTERMEDIARIO, "", _teste(INTERMEDIARIO, _HOJE + '''
app.transacoes = [
    {"id": 1, "descricao": "Mercado", "valor": -300.0, "categoria": "Alimentação", "data": _hoje},
    {"id": 2, "descricao": "Ônibus", "valor": -40.0, "categoria": "Transporte", "data": _hoje},
    {"id": 3, "descricao": "Salário", "valor": 2000.0, "categoria": "Salário", "data": _hoje},
]
app.entradas_limite["Alimentação"].insert(0, "250"); app.entradas_limite["Transporte"].insert(0, "100")
app.salvar_orcamento()
assert app.alertas["Alimentação"].cget("text").startswith("⚠"), app.alertas["Alimentação"].cget("text")
assert not app.alertas["Transporte"].cget("text").startswith("⚠")
import json; assert json.load(open("orcamento.json", encoding="utf-8")) == {"Alimentação": 250.0, "Transporte": 100.0}
app.filtro_categoria.set("Transporte"); app.atualizar_lista_transacoes()
assert [t["descricao"] for t in app.transacoes_filtradas()] == ["Ônibus"]
assert len(app.frame_lista.winfo_children()) == 1
print("alerta de orçamento, persistência dos limites e filtro funcionando")
''')),
("05_projeto_pratico.md", "Avançado", AVANCADO, "", _teste(AVANCADO, '''
app.entry_desc.insert(0, "Aluguel"); app.entry_valor.insert(0, "-800")
app.data_dia.set("31"); app.data_mes.set("02"); app.data_ano.set("2026")
app.adicionar_transacao(); assert any("não existe" in m for m in _gui.MENSAGENS) and not app.transacoes
app.data_dia.set("05"); app.data_mes.set("10"); app.adicionar_transacao()
assert app.transacoes[0]["data"] == "2026-10-05"
app.transacoes += [
    {"id": 2, "descricao": "Salário", "valor": 2000.0, "categoria": "Salário", "data": "2026-10-01"},
    {"id": 3, "descricao": "Lanche", "valor": -20.0, "categoria": "Alimentação", "data": "2026-10-05"},
]
assert app.saldo_acumulado() == [("2026-10-01", 2000.0), ("2026-10-05", 1180.0)], app.saldo_acumulado()
app.atualizar_relatorios()
assert len(app.frame_grafico.winfo_children()) == 1
print("data inválida recusada; saldo acumulado correto; gráfico desenhado")
''')),
]
