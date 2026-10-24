"""
Testes: generators/gerar_catalogo.py e a navegação com vários cursos (Fase 3).
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from generators.atualizar_mkdocs import MkDocsUpdater
from generators.gerar_catalogo import CatalogGenerator, ARQUIVO_CATALOGO


def _criar_curso(fm, slug: str, meta: dict | None, modulo: bool = True) -> Path:
    """Cria cursos/<slug>/ com docs/index.md, um módulo opcional e a ficha opcional."""
    curso = fm.root / "cursos" / slug
    (curso / "docs").mkdir(parents=True)
    (curso / "docs" / "index.md").write_text(f"# {slug}\n", encoding="utf-8")
    if modulo:
        (curso / "modulo_01_inicio").mkdir()
        (curso / "modulo_01_inicio" / "index.md").write_text("# Início do curso\n", encoding="utf-8")
        (curso / "modulo_01_inicio" / "01_aula.md").write_text("# Primeira aula\n", encoding="utf-8")
    if meta is not None:
        fm.escrever_yaml(curso / ".courseforge.yaml", meta, sobrescrever=True)
    return curso


@pytest.fixture
def plataforma(fm_temp):
    """Três cursos fora da ordem alfabética + pastas de apoio que não são cursos."""
    _criar_curso(fm_temp, "python", {
        "nome": "Python", "descricao": "Programação do zero.", "autor": "Prof",
        "ordem": 1, "status": "disponivel",
        "ficha": {"icone": "material-language-python", "nivel": "Iniciante",
                  "carga_horaria": None, "certificado": "Projeto final",
                  "publico": "Iniciantes", "pre_requisitos": ["Usar o computador"],
                  "objetivos": ["Programar", "Criar janelas"]},
    })
    _criar_curso(fm_temp, "office", {
        "nome": "Pacote Office", "descricao": "Word e Excel.", "ordem": 2, "status": "em_breve",
    }, modulo=False)
    _criar_curso(fm_temp, "ia", {"nome": "IA", "descricao": "IA.", "ordem": 3, "status": "em_breve"},
                 modulo=False)
    (fm_temp.root / "cursos" / "stylesheets").mkdir()
    (fm_temp.root / "cursos" / "assets").mkdir()
    return fm_temp


class TestCatalogGenerator:

    def test_ordem_da_ficha_e_nao_alfabetica(self, plataforma):
        nomes = [d.name for d, _ in CatalogGenerator(plataforma).listar_cursos()]
        assert nomes == ["python", "office", "ia"]

    def test_pastas_de_apoio_nao_sao_cursos(self, plataforma):
        nomes = {d.name for d, _ in CatalogGenerator(plataforma).listar_cursos()}
        assert not {"stylesheets", "assets"} & nomes

    def test_curso_sem_ordem_vai_para_o_fim(self, plataforma):
        _criar_curso(plataforma, "aaa", {"nome": "AAA"})
        nomes = [d.name for d, _ in CatalogGenerator(plataforma).listar_cursos()]
        assert nomes[-1] == "aaa"

    def test_catalogo_so_com_cursos_que_tem_ficha(self, plataforma):
        _criar_curso(plataforma, "sem_ficha", None)
        gen = CatalogGenerator(plataforma)
        assert "sem_ficha" in {d.name for d, _ in gen.listar_cursos()}
        assert "sem_ficha" not in {d.name for d, _ in gen.listar_cursos(so_com_ficha=True)}

    def test_gera_catalogo_com_status_links_e_ficha(self, plataforma):
        caminho = CatalogGenerator(plataforma).gerar()
        assert caminho == plataforma.root / "cursos" / ARQUIVO_CATALOGO
        texto = caminho.read_text(encoding="utf-8")

        assert texto.startswith("---\ntitle: Catálogo de cursos")
        assert "Não edite à mão" in texto
        assert ":material-language-python:" in texto
        assert "__Python__" in texto and "__Pacote Office__" in texto
        assert '<span class="cf-tag cf-tag--ok">Disponível</span>' in texto
        assert '<span class="cf-tag">Em breve</span>' in texto
        assert "(python/docs/index.md)" in texto and "(office/docs/index.md)" in texto
        assert "Acessar o curso" in texto and "Ver a ementa" in texto
        assert "- Criar janelas" in texto and "- **Para quem é:** Iniciantes" in texto
        assert texto.index("__Python__") < texto.index("__Pacote Office__") < texto.index("__IA__")

    def test_campo_vazio_nao_aparece(self, plataforma):
        texto = CatalogGenerator(plataforma).gerar().read_text(encoding="utf-8")
        assert "Carga horária" not in texto  # carga_horaria: None

    def test_sem_cursos_nao_gera(self, fm_temp):
        (fm_temp.root / "cursos").mkdir()
        assert CatalogGenerator(fm_temp).gerar() is None
        assert not (fm_temp.root / "cursos" / ARQUIVO_CATALOGO).exists()


class TestNavegacaoMultiCurso:

    @pytest.fixture
    def nav(self, plataforma, config_padrao) -> list:
        (plataforma.root / "cursos" / "como_estudar.md").write_text("# Como estudar\n", encoding="utf-8")
        saida = MkDocsUpdater(plataforma, config_padrao).atualizar(silencioso=True)
        return yaml.safe_load(saida.read_text(encoding="utf-8"))["nav"]

    def test_estrutura_do_topo(self, nav):
        assert nav[0] == {"Início": "index.md"}
        assert nav[1] == {"Comece aqui": [
            {"Catálogo de cursos": "catalogo.md"},
            {"Como estudar": "como_estudar.md"},
        ]}

    def test_uma_aba_por_curso_na_ordem_da_ficha(self, nav):
        assert [list(item)[0] for item in nav[2:]] == ["Python", "Pacote Office", "IA"]

    def test_curso_em_breve_tem_so_a_apresentacao(self, nav):
        office = nav[3]["Pacote Office"]
        assert office == [{"Apresentação do curso": "office/docs/index.md"}]

    def test_curso_disponivel_tem_modulos(self, nav):
        python = nav[2]["Python"]
        assert python[0] == {"Apresentação do curso": "python/docs/index.md"}
        assert python[1] == {"Início do curso": [
            {"Visão Geral": "python/modulo_01_inicio/index.md"},
            {"Primeira aula": "python/modulo_01_inicio/01_aula.md"},
        ]}

    def test_sem_paginas_gerais_nao_cria_comece_aqui(self, fm_temp, config_padrao):
        (fm_temp.root / "cursos").mkdir()
        nav = MkDocsUpdater(fm_temp, config_padrao)._construir_nav()
        assert nav == [{"Início": "index.md"}]
