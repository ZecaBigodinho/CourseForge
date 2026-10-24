"""
CourseForge — generators/atualizar_mkdocs.py

Gerador automático do mkdocs.yml.
Nunca edite o mkdocs.yml manualmente — use esta classe.

Estratégia:
  - Percorre cursos/ → módulos/ → arquivos .md
  - Usa metadados .courseforge.yaml para nomes legíveis (em vez de converter slugs)
  - Títulos de módulos e capítulos vêm do próprio Markdown:
    `title:` do front-matter → primeiro `# H1` → nome do arquivo acentuado
  - Monta estrutura nav: hierárquica
  - Escreve mkdocs.yml via FileManager (não diretamente)
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from generators.gerar_catalogo import CatalogGenerator, ARQUIVO_CATALOGO
from utils.file_manager import FileManager
from utils.cli_ui import UI
from utils.constants import (
    DIR_CURSOS, DIR_MKDOCS, MKDOCS_FILENAME, MODULE_DIR_PREFIX,
    CURSO_DOCS_SUBDIR,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class MkDocsUpdater:
    """
    Gerador automático do mkdocs.yml.

    Responsabilidades:
    - Varrer estrutura de cursos/
    - Usar nomes legíveis dos metadados (não converter slugs)
    - Construir navegação hierárquica (curso → módulo → capítulo)
    - Gerar mkdocs.yml completo via FileManager
    """

    # O menu lateral é só texto: emojis ficam nos títulos das páginas e nos cards da home.

    # Páginas gerais da plataforma (em cursos/), agrupadas na aba "Comece aqui"
    # quando existem. O catálogo é gerado; as demais são escritas à mão.
    PAGINAS_GERAIS: tuple[tuple[str, str], ...] = (
        ("Catálogo de cursos", ARQUIVO_CATALOGO),
        ("Como estudar", "como_estudar.md"),
    )

    # Fallback quando o .md não tem título: palavras de slug → forma acentuada.
    ACENTOS: dict[str, str] = {
        "introducao": "introdução", "configuracao": "configuração",
        "instalacao": "instalação", "revisao": "revisão", "fixacao": "fixação",
        "repeticoes": "repetições", "funcoes": "funções", "colecoes": "coleções",
        "excecoes": "exceções", "variaveis": "variáveis", "graficas": "gráficas",
        "grafica": "gráfica", "pratico": "prático", "pratica": "prática",
        "integracao": "integração", "refatoracao": "refatoração",
        "multiplas": "múltiplas", "programacao": "programação",
        "orientacao": "orientação", "metodos": "métodos", "modulos": "módulos",
        "modulo": "módulo", "exercicio": "exercício", "exercicios": "exercícios",
        "logica": "lógica", "basico": "básico", "conteudo": "conteúdo",
        "manipulacao": "manipulação", "conexao": "conexão", "aplicacao": "aplicação",
    }

    # Palavras que ficam minúsculas no meio do título (fallback).
    MINUSCULAS: frozenset[str] = frozenset(
        {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no",
         "na", "nos", "nas", "com", "para", "por", "ao", "aos", "um", "uma"}
    )

    # "01. ", "02 — ", "1 - ", "Módulo 01 — ", "Capítulo 3: " no início do título.
    _RE_NUMERACAO = re.compile(
        r"^(?:(?:m[oó]dulo|cap[ií]tulo|aula)\s+)?\d+\s*[.:)\-–—]\s*",
        re.IGNORECASE,
    )

    def __init__(self, fm: FileManager, config_global: dict) -> None:
        """
        Args:
            fm: Gerenciador de arquivos da plataforma.
            config_global: Dicionário de configuração global (config.yaml).
        """
        self.fm = fm
        self.config = config_global

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def atualizar(self, silencioso: bool = False) -> Path:
        """
        Gera ou atualiza o mkdocs.yml com base na estrutura atual de cursos/.

        Args:
            silencioso: Se True, suprime mensagens de status no terminal.
                        Use True quando chamado automaticamente após criar curso/módulo/capítulo.

        Returns:
            Path do mkdocs.yml gerado.
        """
        if not silencioso:
            UI.secao("ATUALIZAR MKDOCS.YML")

        # O catálogo vem antes da nav: ele é uma das páginas que a nav referencia
        CatalogGenerator(self.fm).gerar()

        nav = self._construir_nav()
        mkdocs_cfg = self._construir_config(nav)
        output_path = self._salvar(mkdocs_cfg)

        cursos_count = sum(
            1 for item in nav
            if not ({"Início", "Comece aqui"} & item.keys())
        )
        if not silencioso:
            UI.sucesso(f"mkdocs.yml atualizado: {output_path.relative_to(self.fm.root)}")
            UI.muted(f"  {cursos_count} curso(s) na navegação.")

        logger.info("mkdocs.yml gerado em: %s (%d cursos)", output_path, cursos_count)
        return output_path

    # Mantido por compatibilidade retroativa — use atualizar(silencioso=True)
    def atualizar_silencioso(self) -> Path:
        """Alias para atualizar(silencioso=True). Mantido para retrocompatibilidade."""
        return self.atualizar(silencioso=True)

    # ------------------------------------------------------------------ #
    # Construção da navegação                                              #
    # ------------------------------------------------------------------ #

    def _construir_nav(self) -> list:
        """
        Constrói a estrutura nav: do MkDocs percorrendo cursos/.

        Usa metadados .courseforge.yaml para nomes legíveis.
        Formato resultante:
          - Início: index.md
          - Comece aqui:
            - Catálogo de cursos: catalogo.md
            - Como estudar: como_estudar.md
          - Python para Iniciantes:          ← cursos na ordem de `ordem` da ficha
            - Apresentação do curso: python_para_iniciantes/docs/index.md
            - Introdução ao Python:
              - Visão Geral: .../index.md
              - Variáveis e Tipos: .../01_variaveis.md
        """
        nav: list = [{"Início": "index.md"}]
        cursos_dir = self.fm.path(DIR_CURSOS)

        gerais = [{titulo: arq} for titulo, arq in self.PAGINAS_GERAIS if (cursos_dir / arq).exists()]
        if gerais:
            nav.append({"Comece aqui": gerais})

        for curso_dir, _meta in CatalogGenerator(self.fm).listar_cursos():
            entrada_curso = self._construir_entrada_curso(curso_dir, cursos_dir)
            if entrada_curso:
                nav.append(entrada_curso)

        return nav

    def _construir_entrada_curso(self, curso_dir: Path, cursos_dir: Path) -> dict | None:
        """Constrói a entrada de navegação de um curso."""
        meta = self.fm.ler_metadados_curso(curso_dir)
        # Usa nome do metadata para exibição — não converte o slug
        curso_nome = meta.get("nome", curso_dir.name) if meta else curso_dir.name

        curso_entries: list = []

        # Página de apresentação do curso
        index_curso = curso_dir / CURSO_DOCS_SUBDIR / "index.md"
        if index_curso.exists():
            rel = index_curso.relative_to(cursos_dir).as_posix()
            curso_entries.append({"Apresentação do curso": rel})

        modulos = [d for d in self.fm.listar_subdiretorios(curso_dir) if d.name.startswith(MODULE_DIR_PREFIX)]
        modulos = self._ordenar_modulos(modulos, (meta or {}).get("ordem_modulos"), curso_dir.name)

        for modulo_dir in modulos:
            entrada_modulo = self._construir_entrada_modulo(modulo_dir, cursos_dir)
            if entrada_modulo:
                curso_entries.append(entrada_modulo)

        if not curso_entries:
            return None

        return {curso_nome: curso_entries}

    @staticmethod
    def _ordenar_modulos(modulos: list[Path], ordem: list | None, curso_slug: str) -> list[Path]:
        """
        Ordena os módulos de um curso.

        Com `ordem_modulos` no .courseforge.yaml (lista de nomes de pasta), segue essa
        lista — a ordem pedagógica fica desacoplada do nome da pasta, e as URLs não mudam.
        Módulos fora da lista vêm depois, pela regra padrão: 01 em diante e modulo_00 no fim.
        """
        def padrao(d: Path) -> tuple:
            return (1 if d.name.startswith("modulo_00") else 0, d.name)

        if not ordem:
            return sorted(modulos, key=padrao)

        posicao = {nome: i for i, nome in enumerate(ordem)}
        existentes = {d.name for d in modulos}
        for nome in ordem:
            if nome not in existentes:
                logger.warning("ordem_modulos de '%s' cita módulo inexistente: %s", curso_slug, nome)

        listados = sorted((d for d in modulos if d.name in posicao), key=lambda d: posicao[d.name])
        restantes = sorted((d for d in modulos if d.name not in posicao), key=padrao)
        return listados + restantes

    def _construir_entrada_modulo(self, modulo_dir: Path, cursos_dir: Path) -> dict | None:
        """Constrói a entrada de navegação de um módulo."""
        # Slug sem o prefixo "modulo_01_" — fallback do nome quando não há index.md com título
        nome_sem_numero = "_".join(modulo_dir.name.split("_")[2:]) or modulo_dir.name

        index_mod = modulo_dir / "index.md"
        titulo_index = self._titulo_do_markdown(index_mod) if index_mod.exists() else None
        modulo_nome = titulo_index or self._humanizar_slug(nome_sem_numero)

        modulo_entries: list = []

        # Índice do módulo
        if index_mod.exists():
            rel = index_mod.relative_to(cursos_dir).as_posix()
            modulo_entries.append({"Visão Geral": rel})

        # Capítulos
        capitulos = [c for c in self.fm.listar_arquivos(modulo_dir, "md") if c.name != "index.md"]
        titulos = [self._titulo_do_markdown(c) or self._nome_capitulo_legivel(c.stem) for c in capitulos]
        titulos = self._remover_prefixo_comum(titulos)
        for cap, cap_nome in zip(capitulos, titulos):
            rel = cap.relative_to(cursos_dir).as_posix()
            modulo_entries.append({cap_nome: rel})

        if not modulo_entries:
            return None

        return {modulo_nome: modulo_entries}

    # ------------------------------------------------------------------ #
    # Construção da configuração completa                                  #
    # ------------------------------------------------------------------ #

    def _construir_config(self, nav: list) -> dict:
        """Monta o dicionário completo do mkdocs.yml."""
        mkdocs_cfg = self.config.get("mkdocs", {}).copy()
        mkdocs_cfg["nav"] = nav
        mkdocs_cfg["docs_dir"] = "../cursos"
        return mkdocs_cfg

    # ------------------------------------------------------------------ #
    # Persistência via FileManager                                         #
    # ------------------------------------------------------------------ #

    def _salvar(self, cfg: dict) -> Path:
        """
        Salva o mkdocs.yml usando FileManager.

        Após a escrita YAML padrão, injeta a extensão pymdownx.emoji
        com tags !!python/name: que o yaml.dump não consegue serializar.
        """
        output_dir = self.fm.path(DIR_MKDOCS)
        self.fm.criar_diretorio(output_dir)
        output_path = output_dir / MKDOCS_FILENAME
        # Usa escrever_yaml do FileManager — única via de escrita YAML no projeto
        self.fm.escrever_yaml(output_path, cfg, sobrescrever=True)

        # Injetar pymdownx.emoji com tags !!python/name (incompatíveis com yaml.dump)
        self._injetar_emoji_extension(output_path)

        return output_path

    @staticmethod
    def _injetar_emoji_extension(path: Path) -> None:
        """
        Adiciona a extensão pymdownx.emoji ao mkdocs.yml após a serialização YAML.

        Os tags !!python/name: são necessários para o MkDocs Material mas não são
        suportados por yaml.safe_load/dump, então são injetados como texto raw.
        """
        emoji_block = (
            "- pymdownx.emoji:\n"
            "    emoji_index: !!python/name:material.extensions.emoji.twemoji\n"
            "    emoji_generator: !!python/name:material.extensions.emoji.to_svg\n"
        )

        content = path.read_text(encoding="utf-8")

        # Inserir antes da linha "- attr_list" nas markdown_extensions
        marker = "- attr_list"
        if marker in content and "pymdownx.emoji" not in content:
            # Detectar a indentação do marker
            for line in content.splitlines():
                if marker in line:
                    indent = line[: len(line) - len(line.lstrip())]
                    emoji_indented = "".join(
                        f"{indent}{ln}\n" if ln.strip() else "\n"
                        for ln in emoji_block.splitlines()
                    )
                    content = content.replace(
                        f"{indent}{marker}",
                        f"{emoji_indented}{indent}{marker}",
                    )
                    break

            path.write_text(content, encoding="utf-8")

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _titulo_do_markdown(self, path: Path) -> str | None:
        """
        Lê o título de um .md: `title:` do front-matter ou, na falta, o primeiro `# H1`.
        Retorna o título já limpo para o menu, ou None se não houver título.
        """
        try:
            texto = self.fm.ler(path)
        except (OSError, UnicodeDecodeError):
            logger.warning("Não foi possível ler o título de %s", path)
            return None

        linhas = texto.splitlines()
        inicio = 0
        if linhas and linhas[0].strip() == "---":
            for i, linha in enumerate(linhas[1:], start=1):
                if linha.strip() == "---":
                    inicio = i + 1
                    break
                m = re.match(r"^title:\s*(.+?)\s*$", linha)
                if m:
                    return self._limpar_titulo(m.group(1).strip("\"'")) or None

        em_bloco_codigo = False
        for linha in linhas[inicio:]:
            if linha.lstrip().startswith(("```", "~~~")):
                em_bloco_codigo = not em_bloco_codigo
                continue
            if not em_bloco_codigo and linha.startswith("# "):
                return self._limpar_titulo(linha[2:]) or None
        return None

    @classmethod
    def _limpar_titulo(cls, titulo: str) -> str:
        """
        Prepara um título para o menu lateral.
        Ex: '🛠️ Módulo 06 — Configuração do VS Code' → 'Configuração do VS Code'
            '02. Ambientes Virtuais (`venv`)'         → 'Ambientes Virtuais (venv)'
        """
        t = titulo.replace("`", "").replace("**", "").strip()
        # Remove emojis/símbolos iniciais: o menu lateral é só texto
        while t and not (t[0].isalnum() or t[0] in "(\"'¿¡"):
            t = t[1:].lstrip()
        # A numeração fica de fora: a ordem já vem do nome do arquivo
        t = cls._RE_NUMERACAO.sub("", t, count=1)
        t = re.sub(r"\s{2,}", " ", t).strip()
        return t

    @staticmethod
    def _remover_prefixo_comum(titulos: list[str]) -> list[str]:
        """
        Remove um rótulo repetido em todos os capítulos do módulo.
        Ex: ['Revisão Visual: Funções', 'Revisão Visual: Strings'] → ['Funções', 'Strings']
        Só age com 2+ capítulos e quando o prefixo termina em ':'.
        """
        if len(titulos) < 2:
            return titulos
        prefixo = os.path.commonprefix(titulos)
        corte = prefixo.rfind(":")
        if corte <= 0:
            return titulos
        restantes = [t[corte + 1:].strip() for t in titulos]
        return restantes if all(restantes) else titulos

    @classmethod
    def _humanizar_slug(cls, slug: str) -> str:
        """
        Fallback: 'introducao_ao_projeto' → 'Introdução ao Projeto'.
        """
        partes = [p for p in slug.split("_") if p]
        palavras = []
        for i, p in enumerate(partes):
            p = cls.ACENTOS.get(p.lower(), p.lower())
            palavras.append(p if i > 0 and p in cls.MINUSCULAS else p[:1].upper() + p[1:])
        return " ".join(palavras) if palavras else slug

    @classmethod
    def _nome_capitulo_legivel(cls, stem: str) -> str:
        """
        Converte stem de capítulo para nome legível (fallback quando o .md não tem título).
        Ex: '01_variaveis_e_tipos' → 'Variáveis e Tipos'
        Remove o número inicial e humaniza o slug.
        """
        partes = stem.split("_")
        # Pular o número inicial (ex: "01")
        if partes and partes[0].isdigit():
            partes = partes[1:]
        return cls._humanizar_slug("_".join(partes)) if partes else stem
