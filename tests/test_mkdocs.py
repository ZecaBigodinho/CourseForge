"""
Testes: generators/atualizar_mkdocs.py

Verifica a geração do mkdocs.yml com estruturas de curso simples e complexas.
"""
from __future__ import annotations

import yaml
from pathlib import Path

import pytest

from models.course import Course
from models.module import Module
from models.chapter import Chapter
from generators.gerar_curso import CourseGenerator
from generators.gerar_modulo import ModuleGenerator
from generators.gerar_capitulo import ChapterGenerator
from generators.atualizar_mkdocs import MkDocsUpdater
from utils.constants import MKDOCS_FILENAME


class TestMkDocsUpdater:
    """Testes para MkDocsUpdater."""

    @pytest.fixture
    def updater(self, fm_temp, config_padrao) -> MkDocsUpdater:
        """Retorna um MkDocsUpdater apontando para tmp_path."""
        return MkDocsUpdater(fm_temp, config_padrao)

    @pytest.fixture
    def estrutura_completa(self, fm_temp, te_real) -> Path:
        """
        Cria estrutura curso → módulo → capítulo em tmp_path.
        Retorna o diretório tmp_path.
        """
        cg = CourseGenerator(fm_temp, te_real)
        course = Course(nome="Python Básico", descricao="Desc", autor="Prof")
        cg.criar(course)

        mg = ModuleGenerator(fm_temp, te_real)
        module = Module(nome="Introducao", curso_slug="python_basico", numero=1)
        mg.criar(module)

        chg = ChapterGenerator(fm_temp, te_real)
        chapter = Chapter(
            nome="Variaveis",
            curso_slug="python_basico",
            modulo_dir="modulo_01_introducao",
            numero=1,
        )
        chg.criar(chapter)

        return fm_temp.root

    def test_gerar_cria_mkdocs_yml(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        assert output.exists()
        assert output.name == MKDOCS_FILENAME

    def test_mkdocs_yml_e_yaml_valido(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        conteudo = output.read_text(encoding="utf-8")
        parsed = yaml.safe_load(conteudo)
        assert isinstance(parsed, dict)

    def test_mkdocs_yml_contem_site_name(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        assert "site_name" in parsed

    def test_mkdocs_yml_contem_nav(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        assert "nav" in parsed
        assert isinstance(parsed["nav"], list)

    def test_nav_contem_home(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        nav = parsed["nav"]
        # Primeiro item deve ser Home
        assert nav[0] == {"Home": "index.md"}

    def test_nav_contem_curso(self, updater, estrutura_completa):
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        nav = parsed["nav"]
        # Deve ter pelo menos o Home + 1 curso
        assert len(nav) >= 2

    def test_nav_usa_nome_legivel_do_curso(self, updater, estrutura_completa):
        """O nav deve usar o nome do metadata, não o slug."""
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        nav = parsed["nav"]
        # O nome do curso no nav deve ser "Python Básico", não "python_basico"
        nav_keys = [list(item.keys())[0] for item in nav if isinstance(item, dict)]
        assert "Python Básico" in nav_keys

    def test_atualizar_silencioso_alias(self, updater, estrutura_completa):
        """atualizar_silencioso deve ser equivalente a atualizar(silencioso=True)."""
        output = updater.atualizar_silencioso()
        assert output.exists()

    def test_sem_cursos_nav_apenas_home(self, updater, fm_temp):
        """Sem cursos, nav deve ter apenas Home."""
        fm_temp.criar_diretorio(fm_temp.path("cursos"))
        output = updater.atualizar(silencioso=True)
        parsed = yaml.safe_load(output.read_text(encoding="utf-8"))
        assert parsed["nav"] == [{"Home": "index.md"}]


class TestTitulosDaNavegacao:
    """Títulos do menu lidos do Markdown (P1), com acentos e sem numeração."""

    @pytest.fixture
    def updater(self, fm_temp, config_padrao) -> MkDocsUpdater:
        return MkDocsUpdater(fm_temp, config_padrao)

    @pytest.fixture
    def modulo(self, fm_temp) -> Path:
        """Cria cursos/curso_x/modulo_01_introducao_ao_projeto/ vazio."""
        caminho = fm_temp.root / "cursos" / "curso_x" / "modulo_01_introducao_ao_projeto"
        caminho.mkdir(parents=True)
        return caminho

    @staticmethod
    def _nav_do_modulo(updater) -> tuple[str, list]:
        """Retorna (nome do módulo, entradas) do primeiro módulo do primeiro curso."""
        curso = updater._construir_nav()[1]
        entradas_curso = list(curso.values())[0]
        nome, entradas = next(iter(entradas_curso[0].items()))
        return nome, entradas

    def test_capitulo_usa_h1_sem_numeracao(self, updater, modulo):
        (modulo / "01_variaveis.md").write_text("# 01. Variáveis e Tipos\n\nTexto", encoding="utf-8")
        (modulo / "02_login.md").write_text("# 02 — Tela de Login\n", encoding="utf-8")
        _, entradas = self._nav_do_modulo(updater)
        assert [list(e)[0] for e in entradas] == ["Variáveis e Tipos", "Tela de Login"]

    def test_front_matter_title_tem_prioridade(self, updater, modulo):
        (modulo / "01_x.md").write_text(
            '---\ntitle: "Título do Front-matter"\n---\n\n# H1 Diferente\n', encoding="utf-8"
        )
        _, entradas = self._nav_do_modulo(updater)
        assert list(entradas[0]) == ["Título do Front-matter"]

    def test_remove_emoji_e_crases(self, updater, modulo):
        (modulo / "01_venv.md").write_text("# 🧠 Ambientes (`venv`) e **Terminal**\n", encoding="utf-8")
        _, entradas = self._nav_do_modulo(updater)
        assert list(entradas[0]) == ["Ambientes (venv) e Terminal"]

    def test_ignora_h1_dentro_de_bloco_de_codigo(self, updater, modulo):
        (modulo / "01_x.md").write_text(
            "Intro\n\n```python\n# comentario\n```\n\n# Título Real\n", encoding="utf-8"
        )
        _, entradas = self._nav_do_modulo(updater)
        assert list(entradas[0]) == ["Título Real"]

    def test_fallback_acentua_nome_do_arquivo(self, updater, modulo):
        (modulo / "03_introducao_as_funcoes.md").write_text("Sem título.\n", encoding="utf-8")
        _, entradas = self._nav_do_modulo(updater)
        assert list(entradas[0]) == ["Introdução as Funções"]

    def test_remove_prefixo_repetido_no_modulo(self, updater, modulo):
        (modulo / "01_a.md").write_text("# Revisão Visual: Funções\n", encoding="utf-8")
        (modulo / "02_b.md").write_text("# Revisão Visual: Strings\n", encoding="utf-8")
        _, entradas = self._nav_do_modulo(updater)
        assert [list(e)[0] for e in entradas] == ["Funções", "Strings"]

    def test_nao_remove_prefixo_de_um_capitulo_so(self, updater, modulo):
        (modulo / "01_a.md").write_text("# Projeto Prático: Dashboard\n", encoding="utf-8")
        _, entradas = self._nav_do_modulo(updater)
        assert list(entradas[0]) == ["Projeto Prático: Dashboard"]

    def test_modulo_usa_h1_do_index_com_icone(self, updater, modulo):
        (modulo / "index.md").write_text("# 🏗️ Módulo 01 — Introdução ao Projeto\n", encoding="utf-8")
        nome, entradas = self._nav_do_modulo(updater)
        assert nome == "🏗️ Introdução ao Projeto"
        assert entradas[0] == {"Visão Geral": "curso_x/modulo_01_introducao_ao_projeto/index.md"}

    def test_modulo_sem_index_usa_slug_acentuado(self, updater, modulo):
        (modulo / "01_a.md").write_text("# A\n", encoding="utf-8")
        nome, _ = self._nav_do_modulo(updater)
        assert nome == "🏗️ Introdução ao Projeto"

    def test_numero_que_faz_parte_do_titulo_e_mantido(self, updater, modulo):
        (modulo / "01_a.md").write_text("# 3 formas de usar listas\n", encoding="utf-8")
        _, entradas = self._nav_do_modulo(updater)
        assert list(entradas[0]) == ["3 formas de usar listas"]
