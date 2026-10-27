"""
Testes: mkdocs_hooks/versao_css.py

Verifica que o CSS local ganha ?v=<versão> tirada do conteúdo e que o
hook está ligado no config.yaml com um caminho que existe.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from mkdocs_hooks.versao_css import on_config, versao_do_arquivo

RAIZ = Path(__file__).resolve().parent.parent


def _config(docs_dir: Path, extra_css: list[str]) -> dict:
    return {"docs_dir": str(docs_dir), "extra_css": list(extra_css)}


def test_css_local_ganha_versao_do_conteudo(tmp_path):
    css = tmp_path / "stylesheets" / "custom.css"
    css.parent.mkdir()
    css.write_text("body { color: red; }", encoding="utf-8")

    cfg = on_config(_config(tmp_path, ["stylesheets/custom.css"]))

    assert cfg["extra_css"] == [f"stylesheets/custom.css?v={versao_do_arquivo(css)}"]
    assert len(versao_do_arquivo(css)) == 8


def test_versao_muda_quando_o_css_muda(tmp_path):
    css = tmp_path / "custom.css"
    css.write_text("a { color: red; }", encoding="utf-8")
    antes = versao_do_arquivo(css)
    css.write_text("a { color: blue; }", encoding="utf-8")
    assert versao_do_arquivo(css) != antes


def test_css_externo_ja_versionado_ou_inexistente_fica_igual(tmp_path):
    (tmp_path / "ja.css").write_text("", encoding="utf-8")
    originais = [
        "https://exemplo.com/estilo.css",
        "ja.css?v=123",
        "nao_existe.css",
    ]
    cfg = on_config(_config(tmp_path, originais))
    assert cfg["extra_css"] == originais


def test_hook_ligado_no_config_com_caminho_valido():
    config = yaml.safe_load((RAIZ / "src" / "config" / "config.yaml").read_text(encoding="utf-8"))
    hooks = config["mkdocs"]["hooks"]
    # O caminho é relativo à pasta do mkdocs.yml gerado (mkdocs/).
    assert all((RAIZ / "mkdocs" / h).resolve().is_file() for h in hooks)
    assert any(h.endswith("versao_css.py") for h in hooks)
