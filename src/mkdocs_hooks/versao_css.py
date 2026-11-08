"""
CourseForge — mkdocs_hooks/versao_css.py

Hook do MkDocs (ligado em src/config/config.yaml → mkdocs.hooks). Versiona o CSS e o JavaScript locais.

O GitHub Pages manda o navegador guardar o CSS por 10 minutos. Sem mudar
a URL, quem abre o site logo depois de um deploy continua vendo o estilo
antigo. Este hook acrescenta ao fim de cada CSS local de `extra_css` uma
versão tirada do próprio conteúdo do arquivo:

    stylesheets/custom.css  →  stylesheets/custom.css?v=1a2b3c4d

A versão só muda quando o arquivo muda, então o cache continua valendo
entre um deploy e outro sem mudança no estilo.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def versao_do_arquivo(path: Path) -> str:
    """Devolve os 8 primeiros caracteres do SHA-256 do arquivo."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def _versionar(caminho: str, docs_dir: Path) -> str:
    """Acrescenta ?v=<hash> a um arquivo local; externos, já versionados ou inexistentes ficam iguais."""
    local = docs_dir / caminho
    if "://" in caminho or "?" in caminho or not local.is_file():
        return caminho
    return f"{caminho}?v={versao_do_arquivo(local)}"


def on_config(config, **kwargs):
    docs_dir = Path(config["docs_dir"])
    config["extra_css"] = [_versionar(str(css), docs_dir) for css in config["extra_css"]]
    # O mesmo vale para os scripts (no MkDocs 1.6 cada item é um ExtraScriptValue com .path)
    for i, script in enumerate(config.get("extra_javascript", [])):
        if isinstance(script, str):
            config["extra_javascript"][i] = _versionar(script, docs_dir)
        elif hasattr(script, "path"):
            script.path = _versionar(str(script.path), docs_dir)
    return config
