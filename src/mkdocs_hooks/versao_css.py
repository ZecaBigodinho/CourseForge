"""
CourseForge — mkdocs_hooks/versao_css.py

Hook do MkDocs (ligado em src/config/config.yaml → mkdocs.hooks).

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


def on_config(config, **kwargs):
    docs_dir = Path(config["docs_dir"])
    versionados = []
    for css in config["extra_css"]:
        caminho = str(css)
        local = docs_dir / caminho
        # CSS externo (https://...), já versionado (?v=) ou inexistente fica como está.
        if "://" in caminho or "?" in caminho or not local.is_file():
            versionados.append(css)
            continue
        versionados.append(f"{caminho}?v={versao_do_arquivo(local)}")
    config["extra_css"] = versionados
    return config
