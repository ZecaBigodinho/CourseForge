"""
Testes: padrão de imagens das aulas (Fase 7) — ver ferramentas/midia/README.md.

Confere todas as imagens locais usadas em cursos/: texto alternativo, arquivo existente,
formato (WebP ou SVG), tamanho até 300 KB e carregamento preguiçoso.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
CURSOS = RAIZ / "cursos"
TAMANHO_MAXIMO = 300 * 1024

# ![alt](caminho "título opcional"){ atributos opcionais }
_RE_IMAGEM = re.compile(r'!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+"[^"]*")?\)(?P<attrs>\{[^}]*\})?')
_RE_CODIGO = re.compile(r"^(`{3,}|~{3,}).*?^\1", re.S | re.M)
_RE_COMENTARIO = re.compile(r"<!--.*?-->", re.S)


def imagens_locais(texto: str) -> list[dict]:
    """Imagens de um Markdown, fora de blocos de código e comentários, sem as externas (http)."""
    texto = _RE_COMENTARIO.sub("", _RE_CODIGO.sub("", texto))
    return [m.groupdict() for m in _RE_IMAGEM.finditer(texto) if not m["src"].startswith(("http://", "https://"))]


def _todas():
    for md in sorted(CURSOS.rglob("*.md")):
        if "site" in md.parts:
            continue
        for img in imagens_locais(md.read_text(encoding="utf-8")):
            yield md, img


CASOS = list(_todas())


class TestExtracao:
    def test_ignora_codigo_comentario_e_externas(self):
        texto = (
            "![a](assets/x.webp){ loading=lazy }\n"
            "```markdown\n![b](assets/y.webp)\n```\n"
            "<!-- ![c](assets/z.webp) -->\n"
            "![d](https://exemplo.com/e.png)\n"
        )
        assert [i["src"] for i in imagens_locais(texto)] == ["assets/x.webp"]

    def test_le_alt_e_atributos(self):
        img = imagens_locais("![Janela Parágrafo](assets/01_a.webp){ loading=lazy .sem-zoom }")[0]
        assert img["alt"] == "Janela Parágrafo" and "loading=lazy" in img["attrs"]


@pytest.mark.parametrize("md,img", CASOS, ids=[f"{m.relative_to(CURSOS)}:{i['src']}" for m, i in CASOS])
class TestImagensDasAulas:
    def test_tem_texto_alternativo(self, md, img):
        assert img["alt"].strip(), f"{md}: imagem {img['src']} sem texto alternativo"

    def test_arquivo_existe(self, md, img):
        assert (md.parent / img["src"]).is_file(), f"{md}: {img['src']} não encontrado"

    def test_formato_e_tamanho(self, md, img):
        arquivo = md.parent / img["src"]
        assert arquivo.suffix.lower() in (".webp", ".svg"), f"{img['src']}: use WebP ou SVG"
        assert arquivo.stat().st_size <= TAMANHO_MAXIMO, f"{img['src']}: passou de 300 KB"

    def test_carregamento_preguicoso(self, md, img):
        assert img["attrs"] and "loading=lazy" in img["attrs"], f"{md}: {img['src']} sem {{ loading=lazy }}"
