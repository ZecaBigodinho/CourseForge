"""
CourseForge — generators/gerar_catalogo.py

Gera a página "Catálogo de cursos" (cursos/catalogo.md) a partir da ficha de
cada curso em cursos/<slug>/.courseforge.yaml.

Assim como o mkdocs.yml, catalogo.md é arquivo gerado: edite as fichas, não a página.

Campos da ficha (todos opcionais, exceto `nome`):
  nome, descricao, autor                    ← já existentes
  ordem: 1                                  ← posição no menu e no catálogo
  status: disponivel | em_andamento | em_breve
  ficha:
    icone: material-language-python         ← ícone do Material (sem os ':')
    nivel, carga_horaria, publico, certificado: texto
    pre_requisitos, objetivos: lista de textos
"""
from __future__ import annotations

from pathlib import Path

from utils.file_manager import FileManager
from utils.constants import DIR_CURSOS, CURSO_DOCS_SUBDIR, METADATA_FILENAME, MODULE_DIR_PREFIX
from utils.logger import get_logger

logger = get_logger(__name__)

ARQUIVO_CATALOGO = "catalogo.md"

STATUS_ROTULO: dict[str, tuple[str, str]] = {
    "disponivel": ("Disponível", "cf-tag cf-tag--ok"),
    "em_andamento": ("Em andamento", "cf-tag cf-tag--ok"),  # parte dos módulos já publicada
    "em_breve": ("Em breve", "cf-tag"),
}

_CABECALHO = """---
title: Catálogo de cursos
hide:
  - navigation
---

<!-- Página gerada por src/generators/gerar_catalogo.py a partir das fichas em
     cursos/<curso>/.courseforge.yaml. Não edite à mão: rode `python main.py publicar`. -->

# Catálogo de cursos

Todos os cursos são **gratuitos**, em português e pensados para a sala de aula.
Escolha um curso, leia a ficha e comece pela primeira aula.
"""


class CatalogGenerator:
    """Monta o catálogo de cursos e define a ordem dos cursos na plataforma."""

    def __init__(self, fm: FileManager) -> None:
        self.fm = fm

    # ------------------------------------------------------------------ #
    # Interface pública                                                    #
    # ------------------------------------------------------------------ #

    def listar_cursos(self, so_com_ficha: bool = False) -> list[tuple[Path, dict]]:
        """
        Cursos da plataforma, na ordem de exibição: `ordem` da ficha (ausente = fim) e nome.

        Um curso é uma pasta de cursos/ com .courseforge.yaml, docs/ ou módulos — o que
        deixa de fora pastas de apoio como stylesheets/ e assets/.

        Args:
            so_com_ficha: Se True, só os cursos com .courseforge.yaml (usado no catálogo).
        """
        cursos = []
        for curso_dir in self.fm.listar_subdiretorios(self.fm.path(DIR_CURSOS)):
            tem_ficha = (curso_dir / METADATA_FILENAME).exists()
            e_curso = tem_ficha or (curso_dir / CURSO_DOCS_SUBDIR).is_dir() or any(
                d.name.startswith(MODULE_DIR_PREFIX) for d in self.fm.listar_subdiretorios(curso_dir)
            )
            if e_curso and (tem_ficha or not so_com_ficha):
                cursos.append((curso_dir, self.fm.ler_metadados_curso(curso_dir) or {}))
        return sorted(cursos, key=lambda c: (c[1].get("ordem", 999), c[1].get("nome", c[0].name)))

    def gerar(self) -> Path | None:
        """
        Escreve cursos/catalogo.md. Retorna o caminho, ou None se não houver cursos.
        """
        cursos = self.listar_cursos(so_com_ficha=True)
        if not cursos:
            return None

        cards = "\n".join(self._card(d, m) for d, m in cursos)
        fichas = "\n".join(self._ficha(d, m) for d, m in cursos)
        conteudo = (
            f"{_CABECALHO}\n"
            f'<div class="grid cards cf-cursos" markdown>\n\n{cards}\n</div>\n\n'
            f"## Fichas dos cursos\n\n{fichas}"
        )

        destino = self.fm.path(DIR_CURSOS) / ARQUIVO_CATALOGO
        self.fm.escrever(destino, conteudo, sobrescrever=True)
        logger.info("Catálogo gerado: %s (%d cursos)", destino, len(cursos))
        return destino

    # ------------------------------------------------------------------ #
    # Blocos da página                                                     #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _link_curso(curso_dir: Path) -> str:
        return f"{curso_dir.name}/{CURSO_DOCS_SUBDIR}/index.md"

    @staticmethod
    def _status(meta: dict) -> tuple[str, str]:
        return STATUS_ROTULO.get(meta.get("status", "disponivel"), STATUS_ROTULO["disponivel"])

    def _card(self, curso_dir: Path, meta: dict) -> str:
        ficha = meta.get("ficha") or {}
        rotulo, classe = self._status(meta)
        icone = ficha.get("icone", "material-school-outline")
        disponivel = meta.get("status", "disponivel") in ("disponivel", "em_andamento")

        linhas = [
            f"-   :{icone}:{{ .lg .middle }} __{meta.get('nome', curso_dir.name)}__",
            "",
            f'    <span class="{classe}">{rotulo}</span>',
            "",
            "    ---",
            "",
            f"    {meta.get('descricao', '').strip()}",
            "",
        ]
        detalhes = [
            ("Nível", ficha.get("nivel")),
            ("Carga horária", ficha.get("carga_horaria")),
            ("Certificado", ficha.get("certificado")),
        ]
        for rotulo_campo, valor in detalhes:
            if valor:
                linhas.append(f"    **{rotulo_campo}:** {valor}  ")
        acao = "Acessar o curso" if disponivel else "Ver a ementa"
        linhas += ["", f"    [:octicons-arrow-right-24: {acao}]({self._link_curso(curso_dir)})", ""]
        return "\n".join(linhas)

    def _ficha(self, curso_dir: Path, meta: dict) -> str:
        ficha = meta.get("ficha") or {}
        rotulo, classe = self._status(meta)
        partes = [f'### {meta.get("nome", curso_dir.name)} <span class="{classe}">{rotulo}</span>', ""]

        tabela = [
            ("Nível", ficha.get("nivel")),
            ("Carga horária", ficha.get("carga_horaria")),
            ("Para quem é", ficha.get("publico")),
            ("Certificado", ficha.get("certificado")),
            ("Autor", meta.get("autor")),
        ]
        tabela = [(k, v) for k, v in tabela if v]
        if tabela:
            partes += [f"- **{k}:** {v}" for k, v in tabela] + [""]

        for titulo, chave in (("Pré-requisitos", "pre_requisitos"), ("Você vai aprender a", "objetivos")):
            itens = ficha.get(chave) or []
            if itens:
                partes += [f"**{titulo}:**", ""] + [f"- {i}" for i in itens] + [""]

        partes += [f"[Ir para o curso]({self._link_curso(curso_dir)})", ""]
        return "\n".join(partes)
